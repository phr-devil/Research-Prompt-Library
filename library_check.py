#!/usr/bin/env python3
"""Offline repository checks: local links, index entries and evaluation references."""
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent
LINK = re.compile(r"(?<!!)\[[^\]\n]+\]\(([^)]+)\)")
PROMPT = re.compile(r"^## 可直接复制的 Prompt\s*$", re.M)
FENCE = re.compile(r"`{3}text\s*\n([\s\S]*?)\n`{3}")


def invalid_markdown_destination(raw):
    """Bare GFM link destinations cannot contain unescaped spaces."""
    value = raw.strip()
    if value.startswith("<"):
        return False
    value = re.sub(r'\s+"[^"]*"$', "", value)
    return bool(re.search(r"\s", value))


def local_target(source, raw):
    url = raw.strip().split(" \"", 1)[0].strip("<>")
    if not url or url.startswith("#") or url.startswith("//"):
        return None
    parts = urlsplit(url)
    if parts.scheme or parts.netloc:
        return None
    return (source.parent / unquote(parts.path)).resolve()


def markdown_links(path):
    fenced = False
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.lstrip().startswith(("```", "~~~")):
            fenced = not fenced
            continue
        if fenced:
            continue
        for match in LINK.finditer(line):
            yield lineno, match.group(1)


def validate(root=ROOT):
    errors = []
    index = json.loads((root / "LIBRARY_INDEX.json").read_text(encoding="utf-8"))
    fixture = json.loads((root / "EVAL_CASES.json").read_text(encoding="utf-8"))
    entries = {}
    for item in index:
        key, relative = item["id"], item["file"]
        if key in entries:
            errors.append(f"duplicate index id: {key}")
        target = (root / relative).resolve()
        if not target.is_relative_to(root.resolve()) or not target.is_file():
            errors.append(f"invalid index target: {key} -> {relative}")
        entries[key] = target
    for case in fixture["cases"]:
        key = case["prompt_id"]
        target = entries.get(key)
        if not target or not target.is_file():
            errors.append(f"{case['id']}: missing prompt: {key}")
            continue
        data = target.read_text(encoding="utf-8")
        if len(PROMPT.findall(data)) != 1 or not FENCE.search(data.split("## 可直接复制的 Prompt", 1)[-1]):
            errors.append(f"{case['id']}: prompt extractor cannot locate fenced prompt in {key}")

    # S01 is a compatibility entry with exactly two separately copyable prompts.
    s01 = entries.get("S01")
    if s01 and s01.is_file():
        doc = s01.read_text(encoding="utf-8")
        sections = re.findall(
            r"(?ms)^### ([AB]) ·[^\n]*\n(.*?)(?=^### [AB] ·|^## 使用及维护说明|\Z)",
            doc,
        )
        if [label for label, _ in sections] != ["A", "B"]:
            errors.append("S01 must provide distinct A (funding) and B (general) sections")
        else:
            blocks = [FENCE.findall(body) for _, body in sections]
            if any(len(block) != 1 or len(block[0].strip()) < 200 for block in blocks):
                errors.append("S01 A/B must each contain one substantive text prompt")
            elif blocks[0][0].strip() == blocks[1][0].strip():
                errors.append("S01 A/B prompts must be different")
            elif FENCE.search(doc.split("## 可直接复制的 Prompt", 1)[-1]).group(1) != blocks[0][0]:
                errors.append("S01 legacy extractor must select the funding prompt first")

    checked = 0
    for source in root.rglob("*.md"):
        if ".git" in source.parts or ".eval_runs" in source.parts:
            continue
        for lineno, raw in markdown_links(source):
            if invalid_markdown_destination(raw):
                errors.append(f"{source.relative_to(root)}:{lineno} unescaped space in GFM destination: {raw}")
            target = local_target(source, raw)
            if target is None:
                continue
            checked += 1
            if not target.is_relative_to(root.resolve()) or not target.is_file():
                errors.append(f"{source.relative_to(root)}:{lineno} broken link: {raw}")

    skill = root / "08_算法检验与优化/高水平计算机论文工作流/SKILL.md"
    data = skill.read_text(encoding="utf-8")
    if not re.match(r"^---\n(?:(?!\n---).)*\n---\n", data, re.S):
        errors.append("workflow SKILL.md: missing frontmatter")
    else:
        frontmatter = data.split("---", 2)[1]
        if not all(re.search(rf"^{key}:\s*\S+", frontmatter, re.M) for key in ("name", "description")):
            errors.append("workflow SKILL.md: missing name or description")

    nine = root / "09_失败算法项目挽救与转向"
    landing, workflow, gate = (nine / "README.md", nine / "WORKFLOW.md", nine / "salvage_gate.py")
    if not all(p.is_file() for p in (landing, workflow, gate)):
        errors.append("Independent 09 workflow or selection gate missing")
    else:
        body = workflow.read_text(encoding="utf-8")
        for token in ("### STEP 05", "### STEP 06", "P1", "P2", "P3",
                      "WAITING_FOR_USER_SELECTION", "05_USER_SELECTION.json",
                      "不得执行 Step 06", "真实用户消息"):
            if token not in body:
                errors.append("Missing mandatory 09 contract: " + token)
        if body.find("### STEP 05") >= body.find("### STEP 06"):
            errors.append("Step 05 must precede Step 06")
        if entries.get("V09") != landing.resolve():
            errors.append("V09 must be indexed as standalone 09/README.md")

    return errors, len(index), len(fixture["cases"]), checked


if __name__ == "__main__":
    issues, indexed, cases, links = validate()
    for issue in issues:
        print("LIBRARY_CHECK_ERROR:", issue)
    if issues:
        raise SystemExit(1)
    print(f"LIBRARY_CHECK_PASS: {indexed} index entries, {cases} cases, {links} relative links")

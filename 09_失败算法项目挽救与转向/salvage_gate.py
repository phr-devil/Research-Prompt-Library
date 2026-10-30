#!/usr/bin/env python3
"""Read-only structural guard for salvage Step 05 -> Step 06.

A JSON record cannot authenticate human approval: always check the actual,
post-proposal user message; project selection is NOT experiment authorization.
Exit 0 = structurally valid (human provenance still required);
exit 2 = awaiting selection; exit 3 = blocked/invalid.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

IDS = ("P1", "P2", "P3")
NEEDED = ("title", "claim", "dataset_truth", "closest_work",
          "baseline", "test", "cost", "risk")


def inspect_candidates(path):
    raw = Path(path).read_bytes()
    data = json.loads(raw.decode("utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Candidate root must be a JSON object")
    items = data.get("candidates")
    if not isinstance(items, list) or not 1 <= len(items) <= 3:
        raise ValueError("Need one to three candidate projects")
    if len(items) < 3:
        why = data.get("shortfall_reason")
        if not isinstance(why, str) or len(why.strip()) < 8:
            raise ValueError("Partial shortlist needs a substantive shortfall_reason")
    if any(not isinstance(x, dict) for x in items) or [x.get("id") for x in items] != list(IDS[:len(items)]):
        raise ValueError("Require ordered, distinct P1/P2/P3 available IDs")
    for item in items:
        if any(not isinstance(item.get(k), str) or not item[k].strip() for k in NEEDED):
            raise ValueError("Missing candidate scientific fields")
        refs = item.get("evidence_ids")
        if not isinstance(refs, list) or not refs or any(not isinstance(x, str) or not x.strip() for x in refs):
            raise ValueError("Missing evidence_ids")
    if len({x["title"].strip().casefold() for x in items}) != len(items):
        raise ValueError("Candidate titles are duplicated")
    return hashlib.sha256(raw).hexdigest()


def inspect_selection(candidates, selection=None):
    digest = inspect_candidates(candidates)
    if selection is None or not Path(selection).is_file():
        return "WAITING_FOR_USER_SELECTION", digest
    record = json.loads(Path(selection).read_text(encoding="utf-8"))
    if not isinstance(record, dict):
        raise ValueError("Selection root must be a JSON object")
    chosen = record.get("selected_id")
    if chosen not in IDS:
        raise ValueError("User must choose exactly one P1/P2/P3")
    offered = [item["id"] for item in json.loads(Path(candidates).read_text(encoding="utf-8"))["candidates"]]
    if chosen not in offered:
        raise ValueError("Selected project was not offered in the shortlist")
    if record.get("candidate_sha256") != digest:
        raise ValueError("Stale selection: candidate file hash changed")
    for key in ("user_message", "user_message_reference"):
        if not isinstance(record.get(key), str) or not record[key].strip():
            raise ValueError("Missing user message and provenance reference")
    message = record["user_message"].strip()
    # Accept explicit IDs or a small conservative set of unequivocal Chinese ordinals.
    # This is only a syntactic consistency check, not authentication of a human message.
    aliases = {
        "P1": r"(?:(?<![A-Za-z0-9])P1(?![A-Za-z0-9])|第[一1]个(?:项目|课题|方案)|第[一1]项|方案一)",
        "P2": r"(?:(?<![A-Za-z0-9])P2(?![A-Za-z0-9])|第[二2]个(?:项目|课题|方案)|第[二2]项|方案二)",
        "P3": r"(?:(?<![A-Za-z0-9])P3(?![A-Za-z0-9])|第[三3]个(?:项目|课题|方案)|第[三3]项|方案三)",
    }
    if not re.search(aliases[chosen], message, flags=re.IGNORECASE):
        raise ValueError("Selected ID not clearly expressed by user message")
    bare_choice = r"(?:P[123]|第[一二三123]个(?:项目|课题|方案)?|第[一二三123]项|方案[一二三])"
    if re.fullmatch(bare_choice,message,flags=re.IGNORECASE):
        return "STRUCTURE_PASS_HUMAN_MESSAGE_MUST_BE_VERIFIED", digest

    # Recognize the explicitly *chosen* option, not just any ID mentioned
    # near a verb. In particular, "我不选择P2，我选P1" must never pass for P2.
    choice_prefix = re.compile(
        r"(?:我(?:最终)?(?:决定)?|最终|现在)?\s*(?:选(?:择|定|了)?|决定(?:选|选择)?|采用|确定(?:选|选择)?|pick|choose|chosen)\s*$",
        flags=re.IGNORECASE)
    negated = re.compile(
        r"(?:不|没|未|别|拒绝|放弃)\s*(?:想)?\s*(?:选(?:择|定|了)?|采用|确定|考虑)\s*$")
    explicit = []
    for option, pattern in aliases.items():
        for mention in re.finditer(pattern,message,flags=re.IGNORECASE):
            prefix=message[max(0,mention.start()-20):mention.start()]
            if negated.search(prefix):
                continue
            if choice_prefix.search(prefix):
                explicit.append((option,mention))
    if not explicit or {option for option,_ in explicit}!={chosen}:
        raise ValueError("Selection intent is ambiguous or contradicts selected ID")
    for option,mention in explicit:
        tail=message[mention.end():]
        if re.match(r"\s*(?:和|或|与|以及|还是|、|/)\s*(?:P[123]|第[一二三123]个|方案[一二三])",tail,flags=re.IGNORECASE):
            raise ValueError("Multiple candidate projects in one selection")
    return "STRUCTURE_PASS_HUMAN_MESSAGE_MUST_BE_VERIFIED", digest


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--candidates", required=True, type=Path)
    ap.add_argument("--selection", type=Path)
    args = ap.parse_args()
    try:
        state, digest = inspect_selection(args.candidates, args.selection)
    except (ValueError, OSError, TypeError, KeyError) as exc:
        print("BLOCKED_INVALID_SELECTION:", exc, file=sys.stderr)
        return 3
    print(state)
    print("CANDIDATES_SHA256=" + digest)
    if state == "WAITING_FOR_USER_SELECTION":
        return 2
    print("Verify the original human message after P1/P2/P3, then separately authorize experiments.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

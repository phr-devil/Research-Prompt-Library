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
    if not isinstance(items, list) or len(items) != 3:
        raise ValueError("Need exactly three candidate projects")
    if any(not isinstance(x, dict) for x in items) or [x.get("id") for x in items] != list(IDS):
        raise ValueError("Require ordered, distinct P1/P2/P3")
    for item in items:
        if any(not isinstance(item.get(k), str) or not item[k].strip() for k in NEEDED):
            raise ValueError("Missing candidate scientific fields")
        refs = item.get("evidence_ids")
        if not isinstance(refs, list) or not refs or any(not isinstance(x, str) or not x.strip() for x in refs):
            raise ValueError("Missing evidence_ids")
    if len({x["title"].strip().casefold() for x in items}) != 3:
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
    intent = r"(?:选择|选了|选定|我选|决定|采用|确定|pick|choose|chosen)"
    bare_choice = r"(?:P[123]|第[一二三123]个(?:项目|课题|方案)?|第[一二三123]项|方案[一二三])"
    if not re.search(intent, message, flags=re.IGNORECASE) and not re.fullmatch(
            bare_choice, message, flags=re.IGNORECASE):
        raise ValueError("Selection intent not explicit in user message")
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

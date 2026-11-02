"""PD-RW replay output preflight: structural checks only, no science grading."""
import argparse
import json
from pathlib import Path

REQUIRED = ("case_id", "route", "evidence_used", "next_action", "auth",
            "decision_scope", "claim_boundary", "cost_cap", "expected_decision_change")
SCOPES = {"RUN", "MECHANISM", "TASK", "AREA_DATA", "EVIDENCE"}

def audit_responses(responses, cases):
    expected = {c["id"]: c for c in cases}
    results = []
    for row in responses:
        if not isinstance(row, dict):
            results.append({"case_id": None, "status": "INVALID", "issues": ["not an object"]})
            continue
        errors = []
        cid = row.get("case_id")
        case = expected.get(cid)
        if not case:
            errors.append("unknown case_id")
        for field in REQUIRED:
            value = row.get(field)
            if value is None or value == "" or value == []:
                errors.append("missing " + field)
        if row.get("decision_scope") not in SCOPES:
            errors.append("invalid decision_scope")
        if case:
            for field, expected_field in (("route", "expected_route"), ("decision_scope", "decision_scope")):
                if case.get(expected_field) and row.get(field) != case[expected_field]:
                    errors.append(field + " mismatch")
        results.append({"case_id": cid, "status": "CONTRACT_OK" if not errors else "INVALID",
                        "issues": errors, "human_safety": "NOT_REVIEWED"})
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("responses", help="JSON list of blind Agent decisions")
    parser.add_argument("--scenarios", default=str(Path(__file__).resolve().parent / "SCENARIOS.json"))
    args = parser.parse_args()
    cases = json.loads(Path(args.scenarios).read_text(encoding="utf-8"))["cases"]
    decisions = json.loads(Path(args.responses).read_text(encoding="utf-8"))
    if not isinstance(decisions, list):
        parser.error("responses must be a JSON array")
    print(json.dumps(audit_responses(decisions, cases), ensure_ascii=False, indent=2))

#!/usr/bin/env python3
"""Read-only source audit for numeric research runs and reported claim numbers.

Verifies numeric provenance only: SOURCE_MATCH never means SCIENTIFICALLY_SUPPORTED.
No third-party packages, remote calls, training, or automatic authorization.
"""
import argparse
import csv
import json
import math
import sys
from pathlib import Path

REQUIRED = {"run_id", "metric", "value", "status", "evidence_path"}
NON_EVIDENCE = {"INVALID", "CRASH", "PENDING", "NOT_RUN", "HOLD", "INCONCLUSIVE"}
ACCEPTED_SOURCE_STATES = {"KEEP", "DISCARD", "VALID", "PASS", "COMPLETE", "EXPLORATORY"}
IDENTITY = ("data_version", "split", "seed", "protocol_sha", "config_sha",
            "n_units", "statistical_unit", "metric_unit")


def inside(root, candidate, *, must_exist=True):
    """Reject absolute paths, traversal, escaping symlinks and non-files."""
    if not isinstance(candidate, str) or not candidate.strip():
        raise ValueError("empty or non-string path")
    relative = Path(candidate)
    if relative.is_absolute() or ".." in relative.parts or "\\" in candidate:
        raise ValueError("absolute or traversing path")
    dest = (root / relative).resolve()
    if not dest.is_relative_to(root):
        raise ValueError("path escapes project root")
    if must_exist and not dest.is_file():
        raise ValueError("source is not a regular existing file")
    return dest


def number(value):
    if isinstance(value, bool):
        raise ValueError("boolean is not a numeric metric")
    v = float(value)
    if not math.isfinite(v):
        raise ValueError("non-finite metric")
    return v


def read_source(path, run_id, metric):
    """Only named JSON metrics or unambiguous tabular rows count as evidence."""
    if path.stat().st_size > 8 * 1024 * 1024:
        raise ValueError("source exceeds 8 MiB; use a bounded metric summary")
    if path.suffix.lower() == ".json":
        doc = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(doc, dict):
            raise ValueError("JSON source must be an object")
        data = doc.get("metrics", doc)
        if not isinstance(data, dict):
            raise ValueError("metrics must be an object")
        if metric in data:
            metric_value = data[metric]
        elif doc.get("metric") == metric and "value" in doc:
            metric_value = doc["value"]
        else:
            raise ValueError("named metric absent (unrelated numbers do not count)")
        metadata = doc
    elif path.suffix.lower() in (".csv", ".tsv"):
        with path.open(encoding="utf-8-sig", newline="") as stream:
            rows = list(csv.DictReader(stream, delimiter="\t" if path.suffix.lower() == ".tsv" else ","))
        if not rows:
            raise ValueError("no rows")
        if "run_id" in rows[0]:
            rows = [r for r in rows if r.get("run_id") == run_id]
        if len(rows) != 1:
            raise ValueError("table source must identify exactly one run")
        metadata = rows[0]
        if metric in metadata:
            metric_value = metadata[metric]
        elif metadata.get("metric") == metric and "value" in metadata:
            metric_value = metadata["value"]
        else:
            raise ValueError("named metric absent")
    else:
        raise ValueError("unsupported source type; expected JSON/CSV/TSV")
    if "run_id" in metadata and str(metadata["run_id"]) != run_id:
        raise ValueError("source run_id mismatch")
    return number(metric_value), metadata


def audit(root, runs_path, claims_path=None, *, atol=1e-8, require_identity=False):
    if atol < 0 or not math.isfinite(atol):
        raise ValueError("invalid numeric tolerance")
    runs_file = inside(root, runs_path)
    if runs_file.suffix.lower() != ".tsv":
        raise ValueError("RUNS input must be a TSV")
    with runs_file.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        if not reader.fieldnames or not REQUIRED.issubset(reader.fieldnames):
            raise ValueError("RUNS missing required columns")
        rows = list(reader)
    if not rows:
        raise ValueError("RUNS has no experiment records; no evidence to audit")
    results = []
    by_id = {}
    for row_index, row in enumerate(rows, 2):
        run_id = (row.get("run_id") or "").strip()
        if not run_id or run_id in by_id:
            results.append({"run_id": run_id or f"line-{row_index}", "status": "UNVERIFIED",
                            "reason": "missing or duplicate run_id"})
            continue
        by_id[run_id] = row
        status = (row.get("status") or "").strip().upper()
        if status in NON_EVIDENCE:
            results.append({"run_id": run_id, "status": "HISTORICAL_NOT_ELIGIBLE",
                            "reason": "recorded as " + status})
            continue
        if status not in ACCEPTED_SOURCE_STATES:
            results.append({"run_id": run_id, "status": "UNVERIFIED",
                            "reason": "unknown or missing run status"})
            continue
        try:
            metric = (row.get("metric") or "").strip()
            if not metric:
                raise ValueError("empty metric name")
            expected = number(row.get("value"))
            source = inside(root, row.get("evidence_path"))
            actual, metadata = read_source(source, run_id, metric)
            if not math.isclose(actual, expected, rel_tol=1e-9, abs_tol=atol):
                raise ValueError(f"metric value mismatch: TSV={expected}, source={actual}")
            checked = []
            absent = []
            for field in IDENTITY:
                if row.get(field) not in (None, ""):
                    if field not in metadata:
                        absent.append(field)
                    elif str(metadata[field]) != str(row[field]):
                        raise ValueError(f"provenance mismatch for {field}")
                    else:
                        checked.append(field)
            if require_identity and absent:
                raise ValueError("incomplete identity provenance: " + ",".join(absent))
            results.append({"run_id": run_id, "status": "SOURCE_MATCH",
                            "metric": metric, "value": actual,
                            "identity_scope": "PARTIAL" if absent else "COMPLETE",
                            "identity_checked": checked, "identity_not_embedded": absent})
        except (OSError, ValueError, TypeError, json.JSONDecodeError, UnicodeError) as exc:
            results.append({"run_id": run_id, "status": "UNVERIFIED", "reason": str(exc)})
    by_result = {r["run_id"]: r for r in results if r["run_id"] in by_id}
    claim_results = []
    if claims_path:
        obj = json.loads(inside(root, claims_path).read_text(encoding="utf-8"))
        if not isinstance(obj, dict) or not isinstance(obj.get("claims"), list):
            raise ValueError("claims input requires a claims array")
        for index, claim in enumerate(obj["claims"]):
            claim_id = claim.get("claim_id", f"claim-{index}") if isinstance(claim, dict) else f"claim-{index}"
            try:
                if not isinstance(claim, dict):
                    raise ValueError("claim must be an object")
                run_id = claim["run_id"]
                metric = claim["metric"]
                expected = number(claim["reported_value"])
                if run_id not in by_id or by_result.get(run_id, {}).get("status") != "SOURCE_MATCH":
                    raise ValueError("run not verified or ineligible as claim evidence")
                source_result = by_result[run_id]
                if metric != source_result["metric"]:
                    raise ValueError("claim metric differs from run metric")
                if not math.isclose(expected, source_result["value"], rel_tol=1e-9, abs_tol=atol):
                    raise ValueError("claim value differs from verified source")
                claim_results.append({"claim_id": claim_id, "run_id": run_id,
                                      "status": "SOURCE_MATCH_NOT_SCIENCE_REVIEW"})
            except (KeyError, ValueError, TypeError) as exc:
                claim_results.append({"claim_id": claim_id, "status": "UNVERIFIED",
                                      "reason": str(exc)})
    hard_errors = [r for r in results if r["status"] == "UNVERIFIED"]
    hard_errors += [c for c in claim_results if c["status"] == "UNVERIFIED"]
    matches = [r for r in results if r["status"] == "SOURCE_MATCH"]
    if not matches:
        hard_errors.append({"reason": "no active matching source; historical ineligible runs do not count"})
    return {"verdict": "UNVERIFIED" if hard_errors else "SOURCE_CHECK_COMPLETE",
            "scope": "NUMERIC_PROVENANCE_ONLY_NOT_SCIENTIFIC_VALIDITY",
            "runs": results, "claims": claim_results,
            "summary": {"runs_seen": len(rows), "run_source_matches": sum(r["status"] == "SOURCE_MATCH" for r in results),
                        "historical_not_eligible": sum(r["status"] == "HISTORICAL_NOT_ELIGIBLE" for r in results),
                        "claims_checked": len(claim_results), "failures": len(hard_errors)}}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", required=True, help="local project root, never accesses network")
    ap.add_argument("--runs", required=True, help="RUNS.tsv path relative to root")
    ap.add_argument("--claims", help="optional claims_audit.json path relative to root")
    ap.add_argument("--output", help="optional NEW audit report file relative to root")
    ap.add_argument("--atol", type=float, default=1e-8)
    ap.add_argument("--require-identity", action="store_true",
                    help="for claims requiring complete run/data/protocol provenance, fail if any identity field recorded in RUNS is missing from source")
    args = ap.parse_args(argv)
    try:
        root = Path(args.root).resolve(strict=True)
        if not root.is_dir():
            raise ValueError("root must be a local directory")
        report = audit(root, args.runs, args.claims, atol=args.atol,
                       require_identity=args.require_identity)
        rendered = json.dumps(report, ensure_ascii=False, indent=2)
        if args.output:
            target = inside(root, args.output, must_exist=False)
            with target.open("x", encoding="utf-8") as stream:
                stream.write(rendered + "\n")
        print(rendered)
        return 0 if report["verdict"] == "SOURCE_CHECK_COMPLETE" else 1
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(json.dumps({"verdict": "UNVERIFIED", "error": str(exc)}, ensure_ascii=False),
              file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())

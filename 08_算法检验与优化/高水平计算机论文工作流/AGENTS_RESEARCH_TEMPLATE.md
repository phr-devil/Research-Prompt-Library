# Research rules — template for AGENTS.md (merge; do not blindly overwrite)

- Primary target: valid, reproducible scientific contributions competitive for high-level computer-science journals/conferences; engineering PASS is not scientific success.
- Sources of truth: use the repository's verified state/evidence paths, not chat recollection; claim evidence as OBSERVED/EXPLORATORY/CONFIRMED/INVALID/UNKNOWN.
- Do the smallest discriminating scientific check first. Strong and fair baselines, negative controls, independent labels/splits, causal temporal alignment, correct statistical units, and untouched confirmation test take precedence over added complexity.
- Tasks: batch related work into one bounded, independently testable unit; within explicit permissions self-fix ordinary issues. Only inspect changed/impacted files and relevant test cases; preserve existing PASS proof when still valid.
- No implied GPU/cloud-cost/privacy-sensitive upload, release, frozen-protocol changes, test-set tuning, or change of research hypothesis. Ask approval only for these or major scientific forks. Stop when evidence sufficiently answers the task, access is blocked, or budget is exhausted.
- Default to the existing project's verified research/STATE.md and research/RUNS.tsv; short filenames always resolve to the configured state directory, never create duplicate ledgers. Map any pre-existing equivalent paths in STATE.
- Keep the original user research request or verifiable message reference and constraints; preserve provenance when pivoting.
- Recover only verified, still-authorized incomplete work after interruption; never rerun completed, valid experiments by default.
- Record run/commit/config/data split/metric/seed/negative results/cost and raw evidence location. Do not cherry-pick seeds or hide invalidated runs.
- Output at most 7 status lines by default: STATUS; CLAIM_DELTA; EVIDENCE; INVALIDATED; COST; BLOCKERS; NEXT_DECISION. Full logs only to files.
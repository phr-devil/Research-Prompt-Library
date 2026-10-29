# Research STATE (single source of truth)

- USER_INTENT_SOURCE: <verbatim research goal or link to the user's original message; not an inferred rewrite>
- RESEARCH_CLAIM: <one falsifiable sentence>
- STAGE/DECISION: <stage, GO/PIVOT/STOP/HOLD, approver/date>
- NOVELTY_VS_CLOSEST: <nearest paper + exact difference>
- EVIDENCE: <run IDs and raw paths; separate exploratory and confirmatory>
- DATA/SPLIT: <identity, groups, frozen set, leakage controls>
- AUTHORIZED: <explicit user approval reference, CPU/GPU budget, permitted and forbidden operations; blank means no approval>
- PATH_MAP: <existing STATE/RUNS/CLAIMS/REVIEW locations; default research/>
- LAST_VERIFIED_PROGRESS: <latest valid run IDs and checkpoint; pending/blocked IDs>
- RISKS/NEXT: <highest-value next test / blocker>

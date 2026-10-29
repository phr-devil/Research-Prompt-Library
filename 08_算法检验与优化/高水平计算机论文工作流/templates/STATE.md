# Research STATE (single source of truth)

## v5.0 Guided Router Checkpoint（增量补充，避免重复文件）
- WORKFLOW_SOURCE/COMMIT: <prompt library URL / real commit SHA or UNPINNED>
- ROUTE/STATUS: <e.g. 01-B / COMPLETE|PARTIAL|INVALID|BLOCKED>
- COMPLETED_ROUTES: <route IDs with evidence IDs, not merely read>
- PENDING_DECISION: <actual displayed options and message locator; none otherwise>
- USER_DECISION: <real user reply AFTER menu and applicable scope; none otherwise>
- AUTH_SCOPE: <specific authorized resource, budget, stop criteria and real user message; none otherwise>
- NEXT: <next route or WAITING_FOR_USER_DECISION>

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

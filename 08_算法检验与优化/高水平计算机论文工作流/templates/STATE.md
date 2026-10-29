# Research STATE (single source of truth)

## v5.4 Guided Router Checkpoint（增量补充，避免重复文件）
- WORKFLOW_SOURCE/COMMIT: <prompt library URL / real commit SHA or UNPINNED>
- ROUTE_READINESS: <e.g. 01-B / VERIFIED|READY_WITH_LIMITATIONS|BLOCKED_CRITICAL|PARTIAL>
- RUN_STATUS: <COMPLETE|PARTIAL|INVALID|CRASH|BLOCKED|NOT_RUN; separate from scientific readiness>
- COMPLETED_ROUTES: <route IDs with evidence IDs, not merely read>
- PENDING_DECISION: <DECISION_ID + displayed options + message locator + target scope; none otherwise>
- USER_DECISION: <real user reply AFTER menu and applicable scope; none otherwise>
- AUTH_SCOPE: <specific authorized resource, budget, stop criteria and real user message; none otherwise>
- NEXT: <next route or WAITING_FOR_USER_DECISION>
- INCIDENT: <failure route/type, original evidence, root-cause hypothesis, attempts, minimal repair, recheck, invalidated Claim/Run, remaining authorized budget>
- DEFECT_TRIAGE: <ISSUE_ID / CRITICAL|REPAIRABLE|MINOR / affected target action / evidence / limitations / revisit_before>
- RISK_DECISION_CACHE: <decision_id / issue_id / claim_id / claim_fingerprint / data_fingerprint / protocol_fingerprint / source_commit / action_intent / allowed_scope / revisit_before / menu_message_reference / verified later user_message_reference / choice=CONTINUE_LIMITED; reuse only if actual later message independently checked, review not due, no new override>
- ROUTE_READINESS: <VERIFIED | READY_WITH_LIMITATIONS | BLOCKED_CRITICAL (scoped) | PARTIAL>

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

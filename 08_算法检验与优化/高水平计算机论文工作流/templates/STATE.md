# Research STATE｜简明研究断点（v6.0，可选模板）

> **复用现有可信项目状态，不强制新建或迁移**。此处只写持续研究所需的差量证据。

- USER_GOAL: <原始目标或真实用户消息指针>
- CLAIM/HYPOTHESIS: <一个可证伪问题；监督用独立真值，理论/无监督用可核证明/外部验证；近邻增量>
- BEST_VALID_RUN: <run_id / commit / 数据分组版本 / 指标 / 原始证据位置；没有就 NONE>
- CURRENT_FINDING: <本轮真实发现、可信负结果、未验证的科学解释>
- RESEARCH_VALUE: <可选：成功后独立贡献、下一实验能否改变决策；低投入价值不等于假设被证伪>
- NEXT_HYPOTHESIS/TASK: <下一项最有信息量且在授权范围内的工作>
- AUTH/BUDGET: <实际用户授权、上限、余额和来源；明确禁止训练时CPU/GPU均不训练；无则 UNAUTHORIZED>
- BLOCKER/USER_DECISION: <仅重大分叉/真实权限问题需要询问，记录真实用户后续选择；没有则 NONE>
- PATH_MAP: <已有RUNS/CLAIMS/REVIEW/数据的路径，不重复建账>
- WORKFLOW_SOURCE/COMMIT: <真实的源仓 SHA 或 UNPINNED>

按需补充（不默认展开）：

- EVENT: <按当前用户意图选新题/续做/转向，不由旧文件存在与否自动决定；当前研究事件；典型为 DATA_AUDIT / MODEL_DESIGN / IMPLEMENTATION / EXPERIMENT / TRAINING_FAILURE / BASELINE_REPRO_FAIL / EVIDENCE_AUDIT / CONFIRMATION / RESUME / HOLD；合法值以 ROUTES.json 为准>
- USER_AUTH_PROVENANCE: <实际用户后续消息所在会话ID/时间或可由运行环境核实的定位；状态文本本身不构成授权>
- DECISION_REUSE_KEYS: <仅当需要复用REPAIRABLE带限制继续时记 decision_id, issue_id, claim_id, claim_fingerprint, data_fingerprint, protocol_fingerprint, action_intent, allowed_scope, revisit_before, source_commit, menu_message_reference, user_message_reference, choice=CONTINUE_LIMITED；另由可信调用者核对 review_due=False, permission_revoked=False, new_user_override=False，不自动推断>

- NEXT_TASK_ACCEPTANCE: <可选：本轮一个科学任务的可核验交付物、测试命令或实验判据；验证未执行则 NOT_RUN>
- EVIDENCE_SCOPE: <可选：ENGINEERING_VALID / EXPERIMENT_VALID / MECHANISM_SUPPORTED / TASK_VALUE_SUPPORTED；不得互相替代>
- PAPER_READINESS: <可选：NO_INDEPENDENT_CLAIM | CLAIM_WITH_EVIDENCE_GAPS | DRAFTABLE | SUBMISSION_CANDIDATE；可信负结果/理论发现也可构成贡献；SUBMISSION_CANDIDATE不等于已独立审核或获准投稿>
- HOLDOUT_ACCESS: <可选：未接触/开发中已使用/污染/UNKNOWN；不得用STATE文字证明隔离真实有效>
- RUN_STATUS: <COMPLETE|PARTIAL|INVALID|CRASH|BLOCKED|NOT_RUN，指程序运行>
- ROUTE_READINESS: <VERIFIED|READY_WITH_LIMITATIONS|BLOCKED_CRITICAL|PARTIAL，指科学证据>
- RISK_DECISION_CACHE: <仅按上述真实来源与字段记录；缺失则重新检查，不因此停掉无关的安全工作>
- INCIDENT: <仅故障出现时的根因、受影响Run/Claim、修复/验证和剩余预算>
- COMPLETED_ROUTES: <可选历史场景；**不要求凑齐24条**>

**判决轴隔离**：选题`RECOMMEND/EXPLORE/NOT_READY`、实验证据`KEEP/DISCARD/INCONCLUSIVE/INVALID`、动作可行/授权、`PAPER_READINESS`分别记录；HOLD/STOP/PIVOT的项目级建议不能替用户选方向。

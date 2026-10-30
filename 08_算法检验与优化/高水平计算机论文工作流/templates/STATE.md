# Research STATE｜简明研究断点（v6.0，可选模板）

> **复用现有可信项目状态，不强制新建或迁移**。此处只写持续研究所需的差量证据。

- USER_GOAL: <原始目标或真实用户消息指针>
- CLAIM/HYPOTHESIS: <一个可证伪问题；当前相对近邻的潜在学术价值>
- BEST_VALID_RUN: <run_id / commit / 数据分组版本 / 指标 / 原始证据位置；没有就 NONE>
- CURRENT_FINDING: <本轮真实发现、可信负结果、未验证的科学解释>
- NEXT_HYPOTHESIS/TASK: <下一项最有信息量且在授权范围内的工作>
- AUTH/BUDGET: <单独真实用户授权的动作、上限、剩余额度、停止条件及来源；无则 UNAUTHORIZED>
- BLOCKER/USER_DECISION: <仅重大分叉/真实权限问题需要询问，记录真实用户后续选择；没有则 NONE>
- PATH_MAP: <已有RUNS/CLAIMS/REVIEW/数据的路径，不重复建账>
- WORKFLOW_SOURCE/COMMIT: <真实的源仓 SHA 或 UNPINNED>

按需补充（不默认展开）：
- RUN_STATUS: <COMPLETE|PARTIAL|INVALID|CRASH|BLOCKED|NOT_RUN，指程序运行>
- ROUTE_READINESS: <VERIFIED|READY_WITH_LIMITATIONS|BLOCKED_CRITICAL|PARTIAL，指科学证据>
- RISK_DECISION_CACHE: <可信后续用户选择 + 同一主张/数据/协议/许可范围 + 未过期回访节点；无法核实则不可复用>
- INCIDENT: <仅故障出现时的根因、受影响Run/Claim、修复/验证和剩余预算>
- COMPLETED_ROUTES: <可选历史场景；**不要求凑齐24条**>

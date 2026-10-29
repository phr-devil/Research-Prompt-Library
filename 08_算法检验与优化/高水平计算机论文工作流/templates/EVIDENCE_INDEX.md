# 证据/意图索引（按需建立，不重复旧的台账）

- USER_INTENT_VERBATIM_OR_REF: 用户原话或消息引用（若无法追溯写 UNKNOWN，不由 Agent 编造）
- CURRENT_SCIENTIFIC_QUESTION: 当前问题及与原始目标的偏差原因
- PATH_MAP: STATE/RUNS/CLAIMS/REVIEW 的真实路径（已有等价文件则只引用）
- CLOSEST_WORK_CACHE: 论文 DOI/链接、被核对的具体断言、检索日期、未证实处
- KEY_EVIDENCE: Claim ID | Run ID | 版本 | 独立性 | 状态 | 原始路径
- HANDOFF: 只传本轮变动的 Claim/Run/证据文件和 blocker

文献/实验证据只在明确过期、出现新问题或源材料变更时重新检查。每次获取按最小充分范围读取，不用抄录论文全文。

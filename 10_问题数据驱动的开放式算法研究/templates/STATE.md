# PD-RW｜项目最小续做状态（可选模板）

> 若项目已有 STATE、RUNS、CLAIMS 或 data manifest，直接复用并记录路径，不迁移或重复建立。这里是示例占位，不是权限授予、已运行的证据或必填审批表。

- WORKFLOW: CHAPTER_10 / PD-RW v1.0（用户明确选择）
- AREA_DATA: <大科学问题、用户真实选择消息或来源；未选标 WAITING_FOR_USER_SELECTION>
- SCIENTIFIC_VALUE: <成功后可能新增何种独立知识/真实任务能力；不明确 VALUE_UNVERIFIED>
- DATA_MANIFEST: <官方URL/版本/许可/清单/文件指纹/实际路径；未下载为 NOT_RUN>
- DATA_READINESS: <FULL_VERIFIED | PARTIAL_DATA | WAITING_FOR_AUTH | WAITING_FOR_DATA | UNKNOWN | NOT_APPLICABLE>
- HOLDOUT: <独立分组/封存证据及权限；UNTOUCHED | CONTAMINATED | UNKNOWN | NOT_APPLICABLE>
- OBSERVATIONS: <开发集 OBSERVED / HYPOTHESIZED / PROXY_ONLY，原始证据路径>
- TASK_CANDIDATES: <task_id, 来源, 有效观察, 可反驳价值, 任务选择史指针>
- ACTIVE_TASK: <当前科研任务；可以为 UNDECIDED，不阻止合法数据观察>
- BEST_VALID_RUN: <原始可信Run、commit、数据/协议版本、指标及路径；NONE>
- CLAIM_CANDIDATE: <主Claim及具名近邻、强基线差额、证据缺口；UNVERIFIED>
- AUTH/BUDGET: <真实用户授权的来源与作用范围、GPU/CPU拟合/下载/正式确认/费用边界；UNAUTHORIZED>
- NEXT: <唯一信息价值最高的合法动作、验收、停止条件或需要真实用户批准的事项>
- PATH_MAP: <项目现有RUNS/CLAIMS/代码/数据清单映射，别重复复制>

**判定对象必须分开**：RUN/MECHANISM、TASK、AREA_DATA、EVIDENCE、AUTH、PAPER_READINESS；单次负Pilot不能写成整个问题—数据组合 STOP。只更新本轮发生变化的字段，不在空项目初始阶段填满全部模板。
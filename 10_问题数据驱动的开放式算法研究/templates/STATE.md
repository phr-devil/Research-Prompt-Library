# PD-RW｜项目最小续做状态（可选模板）

> 若项目已有 STATE、RUNS、CLAIMS 或 data manifest，直接复用并记录路径，不迁移或重复建立。这里是示例占位，不是权限授予、已运行的证据或必填审批表。

- WORKFLOW: CHAPTER_10 / PD-RW v1.3（用户明确选择）
- AREA_DATA: <大科学问题、用户真实选择消息或来源；未选标 WAITING_FOR_USER_SELECTION>
- DIRECTION_CARD: <下载前宽研究方向、变化轴、任务族、部署可见信息与真值假设；方向未确定为UNDECIDED>
- DATA_PORTFOLIO: <D1开发＋D2独立复现＋可选D3压力测试；每库官方来源/版本/许可、标签语义、独立组、角色；未就绪SECOND_DATASET_GAP>
- DATA_CHOICE: <如适用：PREFERRED / WHY_THIS_OVER_ALTERNATIVE / MOST_DANGEROUS_UNKNOWN / NEXT_LOW_COST_CHECK；已选组合不强制重做筛选>
- SCIENTIFIC_VALUE: <成功后可能新增何种独立知识/真实任务能力；不明确 VALUE_UNVERIFIED>
- PRE_DOWNLOAD_PLAN: <每库所需文件/总存储/下载顺序/官方许可、train-dev-封存角色及真实授权；未授权为WAITING_FOR_AUTH>
- DATA_MANIFEST: <按dataset_id分别记录官方URL/版本/许可/清单/文件指纹/角色/实际路径；未下载为 NOT_RUN>
- DATA_READINESS: <FULL_VERIFIED | PARTIAL_DATA | WAITING_FOR_AUTH | WAITING_FOR_DATA | UNKNOWN | NOT_APPLICABLE>
- HOLDOUT: <独立分组/封存证据、与当前TASK/CLAIM适配性及权限；UNTOUCHED | CONTAMINATED | UNKNOWN | NOT_APPLICABLE>
- OBSERVATIONS: <开发集 OBSERVED / HYPOTHESIZED / PROXY_ONLY，原始证据路径>
- TASK_CANDIDATES: <task_id, 来源, 有效观察, 可反驳价值, 任务选择史指针；未知记 UNKNOWN，不凭事后记忆造预注册>
- TASK_LADDER: <可选：ROOT_PROBLEM / PRIMARY_LEVEL(L0–L3) / LEVEL_CLAIMS与合法K及部署信息 / SHARED_ASSETS / PIVOT_CONDITION / CONFIRMATION；没有有效阶梯写 NOT_APPLICABLE，不强制填四层>
- ACTIVE_TASK: <当前科研任务及允许的标定K/部署前输入；可以为 UNDECIDED，不阻止合法数据观察>
- IMPLEMENTATION: <可选：Input/Output、保护的资产、实际行为测试PASS/NOT_RUN；仅编码时填写>
- BEST_VALID_RUN: <原始可信Run、commit、数据/协议版本、指标及路径；NONE；性能比较注明当前Champion、K单位、可见信息与公平预算>
- CLAIM_CANDIDATE: <主Claim及具名近邻、强基线差额、证据缺口；UNVERIFIED>
- AUTH/BUDGET: <真实用户授权的来源与作用范围、GPU/CPU拟合/下载/正式确认/费用边界；UNAUTHORIZED>
- NEXT: <唯一信息价值最高的合法动作、可区分结果与可能决策；按证据上探UP/下探DOWN/收窄NARROW/横向LATERAL/HOLD（仅当适用），验收、成本上限/停止条件或所需真实授权>
- PATH_MAP: <项目现有RUNS/CLAIMS/代码/数据清单映射，别重复复制>

**判定对象必须分开**：RUN/MECHANISM、TASK、AREA_DATA、EVIDENCE、AUTH、PAPER_READINESS；单次负Pilot不能写成整个问题—数据组合 STOP。只更新本轮发生变化的字段，不在空项目初始阶段填满全部模板。
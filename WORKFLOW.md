# PD-RW v1.3｜PD-RW唯一决策总控（ChatGPT / WorkBuddy / Codex）

**目标**：**本轮研究学科/方向完全以用户当次指令为准**，只有明确「方向不限」时才跨学科；不默认传感器或具身智能。随后在给定范围内选择可信数据/评估基准（或理论证明），获授权后完成实证。**仅用户明确选择PD-RW时启用**；第八章具体命题研究和第九章挽救工作不被自动覆盖或迁移。

## 1. 三个决策循环（六项活动，不是六道审批门）

- **外循环 A｜研究机会**：01 在本轮`USER_SCOPE`内按[SEARCH_DISCOVERY.md](SEARCH_DISCOVERY.md)自适应广搜/深查热点与空白、核最强近邻，明确「方向不限」才跨学科推荐1–3个AREA_DATA组合；**每组合默认3–4库，支持同时开发、备用转题和独立确认**，核跨库标签/科学命题可比性，**第一步确定方向后AI立即自主筛库，不等用户再选数据库** → 完成PRE_DOWNLOAD_PLAN及DOWNLOAD_READY_NOTICE通知用户下载 → 02 收到数据/获授权后按[DATA_INSIGHT.md](DATA_INSIGHT.md)在开发池核真实现象与假象 → 03 接[TASK_EXPLORATION.md](TASK_EXPLORATION.md)选具体可检验TASK与最廉价判别，按需构建L0–L3任务阶梯。一个有依据的机会就可开展有界实验；**不要求完整方法假说**、穷尽任务、复现所有强基线或先证明算法增益。[DATA_DISCOVERY.md](DATA_DISCOVERY.md) / [TASK_EXPLORATION.md](TASK_EXPLORATION.md) / [TASK_LADDER.md](TASK_LADDER.md)。
- **内循环 B｜算法实证**：04 并行考虑`RELIABLE_TRACK`（稳妥性能/现象）和`NOVELTY_TRACK`（机制/规律探索），在已授权范围内按证据动态投入，**不要求双模型同时训练**；新机制先有可区分假设，按症状修复与学习负结果。首次负Pilot不自动STOP，不为GPU占用率扩大无信息实验。[EXPERIMENT_LOOP.md](EXPERIMENT_LOOP.md)。
- **外循环 C｜科研价值**：05 与04并行更新`CLAIM_EVIDENCE_MAP`，区分稳健性能、能力/机制/规律三类独立贡献候选及证据缺口；有最低可信论文路线再按信息价值科学升级；可继续当前层级、`UP`挑战更难信息条件、`DOWN`使用更现实的合法标定、`NARROW`收窄主张，或`LATERAL`比较备用科研任务。06 只有冻结 Claim/方法/协议并获授权后才严格独立确认。层级切换必须更新Claim与公平评价，**L0/L1没有天然论文保底**。[TASK_LADDER.md](TASK_LADDER.md) / [CONFIRMATION.md](CONFIRMATION.md)。

**单次循环可跳转**：已有 STATE/Run 直接续做；低门槛 EXPLORE、中门槛追加投入、高门槛正式确认。**当前最优选择并不由L2的名称决定**：L1若科学价值更明确可先研究L1；L3若有廉价关键正控可先尝试L3。初始 UNKNOWN 不自动否决；论文确认仍核独立真值、时间因果、公平强基线、独立组、效应不确定性与直接近邻。

## 2. 单入口事件路由（一次只读必要的一份专题）

| 当前最主要阻碍 | 读哪个文件 | 下一项有效交付 |
|---|---|---|
| 新课题待搜索、热点/空白和近邻未明 | [SEARCH_DISCOVERY.md](SEARCH_DISCOVERY.md) | SEARCH_HANDOFF：范围/覆盖/首选与最强近邻 |
| 方向已定、数据或评估资源待选 | [DATA_DISCOVERY.md](DATA_DISCOVERY.md) | DIRECTION_CARD→数据/基准→通知用户下载 |
| 数据已可读，需观察真实现象/排除数据假象 | [DATA_INSIGHT.md](DATA_INSIGHT.md) | DATA_INSIGHT_CARD、证据与关键混杂；无现象可标NO_RELIABLE_INSIGHT_YET |
| 数据或文献已提供机会，但具体TASK未定 | [TASK_EXPLORATION.md](TASK_EXPLORATION.md) | 主TASK、必要备选、性能空间/信息条件的最小探针 |
| 同一问题可用不同标签预算/部署条件完成分层任务，或考虑上探/下探 | [TASK_LADDER.md](TASK_LADDER.md) | 一项主层级与L0共享资产、层级间公平协议、切换判据 |
| 有 TASK/基线/负 Pilot/普通代码故障 | [EXPERIMENT_LOOP.md](EXPERIMENT_LOOP.md)；写代码才读 [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md) | 有效 Run、定向修复或 NEXT_PROBE |
| 有可信结果、需要收敛论文贡献或判断创新价值 | [PAPER_FIRST.md](PAPER_FIRST.md)；确需转任务才读[TASK_EXPLORATION.md](TASK_EXPLORATION.md) | CLAIM_EVIDENCE_MAP、具名近邻差额与下一必要实验 |
| 正式科学确认、公开主张、投稿 | [CONFIRMATION.md](CONFIRMATION.md) | 预冻结协议、独立证据或 CONFIRMATION_UNAVAILABLE |
| 用户改变研究范围/权限/预算 | 本文件＋最新 STATE | 影响范围与真实用户决策 |

已有项目先核STATE/有效Run的索引，再按阻碍只读一份专题与受影响证据；无需每轮重读全章、旧Prompt、历史失败和完整训练日志。规则/协议或证据变化时才重读相关内容。ChatGPT 优先公开资料与科学论证，WorkBuddy/Codex 在用户实际授权范围内核本地资产并执行。状态缓存与现场不符时以原始证据和最新授权为准。

## 2.5 各阶段的最短交接（不是每轮填写全部字段）

- **01**：`SEARCH_HANDOFF → DIRECTION_CARD → WHY_THIS_OVER_ALTERNATIVE → DATA_PORTFOLIO → PRE_DOWNLOAD_PLAN → DOWNLOAD_READY_NOTICE`；用户未授权不得下载。
- **02–03**：按需`DATA_INSIGHT_CARD → PRIMARY_TASK / VALUE_HYPOTHESIS / MINIMUM_PROBE`；无真实现象可从合法需求/文献提出可检验任务，不冒充已观察。
- **04↔05**：公平Champion–Challenger和`ALGORITHM_HYPOTHESIS → 有效Run → CLAIM_EVIDENCE_MAP → NEXT_PROBE`，按需读[PAPER_FIRST.md](PAPER_FIRST.md)；`PERFORMANCE_FLOOR/PAPER_PATH_CANDIDATE/SCIENCE_UPGRADE`不是强制阶段。
- **06**：冻结当前Task/Claim/方法/协议及选择史，按[CONFIRMATION.md](CONFIRMATION.md)核独立证据。级间转换按[TASK_LADDER.md](TASK_LADDER.md)更新合法信息、评估和Claim。

每次只交当前阻碍所需的最少字段；授权、证据、机制/任务/区域级止损仍由本文件统一决定。

## 3. 唯一下一行动算法（不机械全跑检查表）

依当前决定的影响顺序选择：
1. **真实性/权限**：证实泄漏、伪真值、确认集污染、越权或必要平台阻断 → 仅隔离受影响动作和 Claim；UNKNOWN 只核当前最危险且廉价可验的事实。
2. **实验能力**：数据、评价、同步、平台或训练链缺失 → `ENABLEMENT`，局部修复与定向验证；工程 PASS 不等于科研发现。
3. **机会与实验**：无 TASK → `DISCOVERY`；有 TASK → `LOW_COST_PROBE`，优先最便宜且可能改变判断的真实实验；正控、双规模、完整强基线只在相关时触发。
4. **主张与任务比较**：可信新发现或有不同失败前提的更好备用机会 → `CLAIM_REVIEW`，比较可行性、独立价值和续投成本。若同问题有可靠层级转化路径，按 [TASK_LADDER.md](TASK_LADDER.md) 选择 `UP / DOWN / NARROW / LATERAL / HOLD`，不需要先把当前方法“彻底判死”；但任何切换都**不得跨级继承不合法的标签/未来信息**，也不能把同一失败前提包装成新Task。
5. **确认**：匹配、未污染确认资源可用且 Claim/协议冻结、获用户确认性实验授权 → `CONFIRMATION`；不满足则限缩 Claim 或记 CONFIRMATION_UNAVAILABLE。

**每轮最小合同**：`CURRENT_EVIDENCE | BLOCKER_OR_UNKNOWN | NEXT_PROBE | POSSIBLE_OUTCOMES_AND_DECISION | AUTH/BUDGET | DELIVERABLE`。NEXT_PROBE 可以产生观察、能力或判别信息，不要求每次提高分数。优先单一主实验，原授权内连续完成关联修复和验证；无新增信息/能力且成本不值得才 HOLD 对应分支，不无限循环。

## 4. 止损层级和状态分账

| 决策范围 | 可继续的条件 | 何时暂停/转向 |
|---|---|---|
| **RUN/机制** | 欠训练、评价问题或有不同预测的机制机会仍可廉价辨别 | 公平负证据或成本失衡 → DISCARD/HOLD 本机制 |
| **TASK** | 可在相同问题下改变合法信息/标定约束、尝试不同物理解释或备用机会；记录各层级证据 | 共同失败前提已否定、真值不可达、无新信息 → 当前TASK或L层级HOLD；必要时DOWN/NARROW/LATERAL |
| **AREA_DATA** | 数据仍支持合法、可评价的其他研究任务 | 关键前提不可达且成本不值得 → 建议更换组合；由用户决定 |

**科研证据 ≠ 运行状态 ≠ 投资决定 ≠ AUTH**。`RUN_STATUS=COMPLETE`、`KEEP` 或 GPU 小时不等于 `CONFIRMED`。缺资源/未验证标 UNKNOWN 或 `WAITING_FOR_AUTH`，不写科学 REFUTED。项目级 HOLD/STOP、核心研究方向/数据库变化须用户决定；不能靠换 Backbone 名称重复预算和同一失败前提。普通 Bug 不强制多轮询问。

## 5. 边界、可复现证据与交付

- 用户选择**宽研究方向或多数据库研究组合**不代表授权下载、安装、外传、CPU Ridge等拟合、GPU训练、付费、正式确认或投稿。下载前需`DIRECTION_CARD`＋AI已选`DATA_PORTFOLIO`＋逐库`PRE_DOWNLOAD_PLAN`并通知用户；获授权后才可下载，第二库缺失时写`SECOND_DATASET_GAP`且不冒充跨库确认。逐项以真实用户消息为准。无权限/工具写 NOT_RUN。实质更改科研目标、资源、冻结确认协议须再次批准。
- 保护原始数据血缘、训练/开发隔离、train-only 预处理、合法分组/评价器与封存确认集。`task_id/protocol_id/eligible_holdout` 必须支持当前新任务：提前封存不代表任何任务都能用；任务搜索或确认集污染不可靠换 seed、重划分洗白。
- 复用 `research/STATE.md`、`RUNS.tsv`、`CLAIMS.md` 等资产，不新建空目录；保存 `BEST_VALID_RUN`、任务选择史、失败原始 Run、源码和数据/评价版本。协议更改只重算受影响证据。
- **EVIDENCE_FIRST_OUTPUT（01–06统一）**：默认仅`NEW_EVIDENCE+PATH | DECISION_CHANGE/UNCERTAINTY | NEXT_PROBE(+不同结果如何改变决定) | AUTH/COST`；无新证据只报阻碍/下一动作。日志、代码、图、失败Run完整**落盘但不回显全文**；Agent只读/报相关diff、关键指标和必要报错尾部。避免重复总结、长报告、无效多Agent审核。用户要完整文档时再展开。**单次负Pilot** ≠ 整个 AREA_DATA 失败。
- **图片三档**：01–05默认纯文本和紧凑表格；不自动生成装饰图、论文级美图、PPT/PDF、仪表盘、未实测成功曲线。仅当能判别假设/错误或支持必要科研证据时制作**简单可复现诊断图**（Loss、残差、group对照等）；复用旧图与脚本，不反复美化。活动05只形成证据草图，正式论文图片排版延至活动06**证据可靠且用户确需交付**时。必要统计图不可为省Token省略。
- **上下文与执行**：复用STATE、manifest、缓存、有效Run；只在新信息可能改变结论时重查/复跑/绘图。已授权的关联修复连续完成，局部回归按影响执行；关键科学验证与合并CI不删。比较Token、GPU、人工总成本，不牺牲可复现性。

## 6. 评测与来源（非 Agent 必走关卡）

`SCENARIOS.json` 和 `tests/test_contract.py` 仅测试设计/结构，不证明科研效能。实际需按 [REPLAY_PROTOCOL.md](REPLAY_PROTOCOL.md) 在相同信息/授权/预算下做**历史盲回放**（遮蔽后续结局）及**前瞻性跟踪**，比较首个真实有效结果、任务价值、过早停止、无效实验、科研确认与 GPU/Token/人工总成本；未运行标 NOT_MEASURED。



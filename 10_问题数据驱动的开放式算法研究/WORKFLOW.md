# PD-RW v1.1｜第十章唯一决策总控（ChatGPT / WorkBuddy / Codex）

**目标**：从大问题＋可靠数据（或理论证明路径）出发，尽早获得最小可信实证，逐步发现 TASK、方法和独立科学贡献。**仅用户明确选择第十章时启用**；第八章具体命题研究和第九章挽救工作不被自动覆盖或迁移。

## 1. 三个决策循环（六项活动，不是六道审批门）

- **外循环 A｜研究机会**：01 问题—数据轻筛 → 02 真实开发数据观察 → 03 发现可检验 TASK。一个有依据的机会就可开展有界实验；**不要求完整方法假说**、穷尽任务、复现所有强基线或先证明算法增益。[DATA_DISCOVERY.md](DATA_DISCOVERY.md) / [TASK_EXPLORATION.md](TASK_EXPLORATION.md)。
- **内循环 B｜算法实证**：04 保留可信基线，按症状选择简单优化、正控、残差/可学性探针、新机制或工程恢复；在已授权预算内试验并记录真实正负结果。首次负Pilot不自动STOP，不为 GPU 占用率扩大无信息实验。[EXPERIMENT_LOOP.md](EXPERIMENT_LOOP.md)。
- **外循环 C｜科研价值**：05 用真实收益/规律、具名近邻和简单竞争解释评价独立贡献；可以继续、调整方法，或**主动**对比备用 TASK 而非等到彻底失败。06 只有冻结 Claim/方法/协议并获授权后才严格独立确认。[TASK_EXPLORATION.md](TASK_EXPLORATION.md) / [CONFIRMATION.md](CONFIRMATION.md)。

**单次循环可跳转**：已有 STATE/Run 直接续做；低门槛 EXPLORE、中门槛追加投入、高门槛正式确认。初始 UNKNOWN 不自动否决；论文确认仍核独立真值、时间因果、公平强基线、独立组、效应不确定性与直接近邻。

## 2. 单入口事件路由（一次只读必要的一份专题）

| 当前最主要阻碍 | 读哪个文件 | 下一项有效交付 |
|---|---|---|
| 未选组合、数据/标签/封存状态不明 | [DATA_DISCOVERY.md](DATA_DISCOVERY.md) | AREA_DATA_CARD、DATA_MANIFEST 或真实开发观察 |
| 数据可用，但 TASK 未明或出现更好的科学机会 | [TASK_EXPLORATION.md](TASK_EXPLORATION.md) | 一个主 TASK、可选一个不同失败前提的备选、最小判别 |
| 有 TASK/基线/负 Pilot/普通代码故障 | [EXPERIMENT_LOOP.md](EXPERIMENT_LOOP.md) | 有效 Run、定向修复或 NEXT_PROBE |
| 有可信结果、需要论文主张或比较任务价值 | [TASK_EXPLORATION.md](TASK_EXPLORATION.md) | CLAIM_CANDIDATE、近邻差额、证据缺口 |
| 正式科学确认、公开主张、投稿 | [CONFIRMATION.md](CONFIRMATION.md) | 预冻结协议、独立证据或 CONFIRMATION_UNAVAILABLE |
| 用户改变研究范围/权限/预算 | 本文件＋最新 STATE | 影响范围与真实用户决策 |

先读 [START.md](START.md)、最新可核 STATE/有效 Run，再按阻碍只读一份专题；不预读 24 旧 Prompt、全部失败史或重复检查已验证数据。ChatGPT 优先公开资料与科学论证，WorkBuddy/Codex 在用户实际授权范围内核本地资产并执行。状态缓存与现场不符时以原始证据和最新授权为准。

## 3. 唯一下一行动算法（不机械全跑检查表）

依当前决定的影响顺序选择：
1. **真实性/权限**：证实泄漏、伪真值、确认集污染、越权或必要平台阻断 → 仅隔离受影响动作和 Claim；UNKNOWN 只核当前最危险且廉价可验的事实。
2. **实验能力**：数据、评价、同步、平台或训练链缺失 → `ENABLEMENT`，局部修复与定向验证；工程 PASS 不等于科研发现。
3. **机会与实验**：无 TASK → `DISCOVERY`；有 TASK → `LOW_COST_PROBE`，优先最便宜且可能改变判断的真实实验；正控、双规模、完整强基线只在相关时触发。
4. **主张与任务比较**：可信新发现或有不同失败前提的更好备用机会 → `CLAIM_REVIEW`，比较可行性、独立价值和续投成本；不因一次正/负 Pilot 就认定科研成功/失败。
5. **确认**：匹配、未污染确认资源可用且 Claim/协议冻结、获用户确认性实验授权 → `CONFIRMATION`；不满足则限缩 Claim 或记 CONFIRMATION_UNAVAILABLE。

**每轮最小合同**：`CURRENT_EVIDENCE | BLOCKER_OR_UNKNOWN | NEXT_PROBE | POSSIBLE_OUTCOMES_AND_DECISION | AUTH/BUDGET | DELIVERABLE`。NEXT_PROBE 可以产生观察、能力或判别信息，不要求每次提高分数。优先单一主实验，原授权内连续完成关联修复和验证；无新增信息/能力且成本不值得才 HOLD 对应分支，不无限循环。

## 4. 止损层级和状态分账

| 决策范围 | 可继续的条件 | 何时暂停/转向 |
|---|---|---|
| **RUN/机制** | 欠训练、评价问题或有不同预测的机制机会仍可廉价辨别 | 公平负证据或成本失衡 → DISCARD/HOLD 本机制 |
| **TASK** | 有独立可观测信息、可纠正性、不同科学问题或备用机会 | 共同失败前提已否定、真值不可达、无新信息 → TASK HOLD/PIVOT |
| **AREA_DATA** | 数据仍支持合法、可评价的其他研究任务 | 关键前提不可达且成本不值得 → 建议更换组合；由用户决定 |

**科研证据 ≠ 运行状态 ≠ 投资决定 ≠ AUTH**。`RUN_STATUS=COMPLETE`、`KEEP` 或 GPU 小时不等于 `CONFIRMED`。缺资源/未验证标 UNKNOWN 或 `WAITING_FOR_AUTH`，不写科学 REFUTED。项目级 HOLD/STOP、核心研究方向/数据库变化须用户决定；不能靠换 Backbone 名称重复预算和同一失败前提。普通 Bug 不强制多轮询问。

## 5. 边界、可复现证据与交付

- 用户选择**研究组合**不代表授权下载、安装、外传、CPU Ridge 等拟合、GPU 训练、付费、正式确认或投稿；逐项以真实用户消息为准。无权限/工具写 NOT_RUN。实质更改科研目标、资源、冻结确认协议须再次批准。
- 保护原始数据血缘、训练/开发隔离、train-only 预处理、合法分组/评价器与封存确认集。`task_id/protocol_id/eligible_holdout` 必须支持当前新任务：提前封存不代表任何任务都能用；任务搜索或确认集污染不可靠换 seed、重划分洗白。
- 复用 `research/STATE.md`、`RUNS.tsv`、`CLAIMS.md` 等资产，不新建空目录；保存 `BEST_VALID_RUN`、任务选择史、失败原始 Run、源码和数据/评价版本。协议更改只重算受影响证据。
- 默认汇报：当前问题—数据/TASK、真实新证据及边界、保留/修复/暂停理由、一个最有信息价值的下一步与成本授权缺口；不要流水账。**单次负Pilot** ≠ 整个 AREA_DATA 失败。

## 6. 评测与来源（非 Agent 必走关卡）

`SCENARIOS.json` 和 `test_chapter10.py` 仅测试设计/结构，不证明科研效能。实际需在相同信息/授权/预算下做**历史盲回放**（遮蔽后续结局）及**前瞻性跟踪**，比较首个真实有效结果、任务价值、过早停止、无效实验、科研确认与 GPU/Token/人工总成本；未运行标 NOT_MEASURED。不能承诺论文接收或成功率；方法借鉴见 [REFERENCES.md](REFERENCES.md)。

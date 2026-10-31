# 选题后研究执行引擎｜Post-Selection Research Engine v1

> **面向直接读取 GitHub 仓库的 AI Agent，而非要求用户复制 Prompt。** 本文件是第八项 v6.1 在选题确定之后的默认技术索引；总控仍是 [ORCHESTRATOR.md](ORCHESTRATOR.md)。不增加新审批阶段，不改变第09章 Step05/05-R 人工选题门禁。

## 一句话用法

用户已选定课题（或项目已有结果）时：**先读 ORCHESTRATOR.md + 本文件 + 当前项目的最新有效状态；按当前任务仅加载下面一份最相关的 playbook**。ChatGPT 负责研究主张/实验设计/重要决策，WorkBuddy/Codex 负责可访问的代码、真实数据和获授权实验。已有证据直接复用，不为“流程齐全”重跑。

**默认内循环**：科学问题与反向论文审查 → 真实数据/强基线及性能空间诊断 → 少量竞争机制与最小实现 → 有界且必要时充分的 GPU/CPU 实验 → KEEP/DISCARD/INCONCLUSIVE/INVALID → 在足够证据下确认论文主张。顺序可按项目状态跳跃、合并；可将一次综合任务连续完成，不逐文件征询。

## 按“下一项需要解决什么”加载一份技术手册

| 真实事件/需要 | 先读哪份 | 具体产物 | 不该做的事 |
|---|---|---|---|
| 新课题可行性、数据/标签/评价不确定 | [01 数据与可信基线](playbooks/01_DATA_BASELINE.md) | 数据契约 + 评价入口 + 公平基线结果或明确阻断 | 先造大网络；将代理标签当真值 |
| 首次开发、修复梯度/数值/接口问题 | [02 算法实现与验证](playbooks/02_BUILD_DEBUG.md) | 真实输入输出运行链路 + 相关自动化测试 + 变更证据 | 对所有代码强制重构、无因调参 |
| 有有效基线，准备提升/诊断无增益 | [03 科学实验迭代](playbooks/03_EXPERIMENT_LOOP.md) | 预期有区分力的实验、全结果与下一假设 | 无限实验；最好 seed；多次调确认集 |
| 有可信初步结果，准备正式论文主张 | [04 机制证据与确认](playbooks/04_EVIDENCE_CONFIRM.md) | Claim→Run→独立效应/统计→图表的证据矩阵 | 工程 PASS 冒充任务/机制贡献 |
| 传感器何时启动等多模态控制题 | [完整实例：触觉门控](playbooks/EXAMPLE_SENSOR_GATE.md) | 可映射到实际数据的实验合同示例 | 直接宣称离线代理指标等于控制收益 |

**技术参考按需加载**：算法骨架不明确时读 [结构选择卡](playbooks/ALGORITHM_DESIGN_REFERENCE.md)；实现/审查新算子时将 [正确性测试模板](templates/test_algorithm_contract.py) 按 [接入说明](templates/ALGORITHM_TEST_USAGE.md) 适配目标算法；存在时间戳/异步多模态/动态传感器风险时读 [专项诊断](playbooks/SENSOR_DIAGNOSTICS.md)。这些都不是新的强制阶段；模板未适配不能生成算法 PASS。

**科学贡献导向（已有课题直接执行）**：以「具体新知识/实际任务收益 → 必需论文证据 → 最简公平基线 → 必要创新机制 → 判别实验」决定研发路线，而不是先堆Backbone/Loss。先在已有Run/只读信息中查最强剩余误差与机制所需的部署可见信号；若仅特权Oracle或自生成代理能获益，缩窄主张，不声称可部署增益。取得合法证据后再扩展复杂结构；无可靠支持时仍可在有界许可内探索。

**选题后的证据优先决策（不是第五阶段之外的新流程）**：只有宽泛方向时用 [IDEA_FUNNEL.md](IDEA_FUNNEL.md) 的 F4 反向论文审查；用户选题后先在 [01 数据手册](playbooks/01_DATA_BASELINE.md) 复用强基线、检查诊断 Oracle 的信息边界和分条件误差，得到 `B_strong/O_reference/gap/UNKNOWN` 与一个最便宜的判别实验。有科研空间时按 [架构参考](playbooks/ALGORITHM_DESIGN_REFERENCE.md) 竞争少量机制；按 [03 实验迭代](playbooks/03_EXPERIMENT_LOOP.md) 在真实用户已批预算内依据收敛曲线和科学不确定性调整 GPU 训练；最后用 [04 科学审查](playbooks/04_EVIDENCE_CONFIRM.md) 将结果映射至论文 Claim。缺真值、离线不可识别或无法比较时缩窄主张/记录 HOLD，不以追加 GPU 掩盖。

**一轮只交付一条决策记录**（复用 `STATE/RUNS/CLAIMS`）：`Claim | B_strong及诊断参考的证据等级 | 最大未解的竞争解释 | 下一有区分力的实验 | 已批准的预算/停止条件 | KEEP/DISCARD/INCONCLUSIVE/INVALID`。原始指标、失败和代码/数据版本仍保存在旧 Run 中；空缺填 UNKNOWN，不编数字。


**论文证据草图（按事件触发，不是新阶段）**：首次取得可核实的有效科学结果，或主要 Claim/强基线发生实质变化时，在现有 `CLAIMS/STATE` **增量记录一行**：`一句独立贡献 | 具名最近邻差额 | 支撑的Run/主图候选 | 最危险证据缺口 | 主张边界 | PAPER_READINESS`。尚无独立贡献则记 `NO_INDEPENDENT_CLAIM`，不为了写论文补造结果；只有用户要求写稿时才进入 [05-A](05_论文撰写与投稿.md) 的详细大纲。写作草图不授权GPU、正式确认、投稿或改研究方向。

异常先按 [TRIAGE.md](TRIAGE.md) 判断影响范围，再按需读 [RECOVERY.md](RECOVERY.md) 的对应症状；关键科研风险出现时才启动 [04_独立科学验证.md](04_独立科学验证.md)。旧24个 Prompt 和 ROUTES.json 保留兼容，非阶段通关表。

### 候选推荐与研究结论分账

继承F4/第09章Step05的`RECOMMEND/EXPLORE/NOT_READY`及尚未核实前提；这是**研发准入判断**，绝非模型性能证据。选题后首先解决剩余未知、复用已核近邻与数据资料，不在05-R重复从头查新。实验结果按`KEEP/DISCARD/INCONCLUSIVE/INVALID`另行定级，并显式给出`DECISION_SCOPE=RUN|MECHANISM|CLAIM|PROJECT`。例如融合模块不如简单基线通常先是MECHANISM级负结果，不自动视为整个研究问题失败。只有证据范围和预期继续成本支持时才建议项目级HOLD/STOP。

## 最小“实验—证据”工作合同（已有等价文件只引用，不复制）

- **QUESTION / VALUE**：一句可证伪的中心主张；即使内部指标全部提高，仍新增什么可验证的任务、机制或理论价值？
- **DATA & TRUTH**：原始字段、物理单位/采样频率/时序、部署时可用信息、标签来源、独立统计单位和分组；缺关键真值不得夸大主张。
- **COMPARISON**：至少一个简单可信对照 + 最接近的可行强基线，统一输入信息/训练预算/预测视野/评估脚本；注明不可比条件。
- **DISCRIMINATION**：预先说明竞争解释 X/Y 对哪一个负对照或干预会给出不同预测；主指标与代理指标分别报告。
- **TEST & BUDGET**：开发/确认集隔离；明确本轮影响决策的最小实验、有效证据、计算/时间/尝试上限；缺用户真实 GPU/付费/正式实验授权不运行。
- **RESULT & NEXT**：原始预测/日志路径 + 数据/配置/代码指纹 + 全 seed/失败条件 + 真实统计单位 + KEEP/DISCARD/INCONCLUSIVE/INVALID；下一项有信息价值的实验或研究决定。

优先使用项目既有 `research/STATE.md`、`RUNS.tsv`、`CLAIMS.md`、`REVIEW.md`（或映射路径）。记录**差量**即可，不建立一套竞争性的日志系统。只有实际结果才能支持模型增益、科研机制和资源消耗等陈述。

## 事件路由（可选 CLI，不需要安装额外依赖）

在提示词库目录中执行 `python workflow_route.py --event DATA_AUDIT`、`--event IMPLEMENTATION`、`--event EXPERIMENT`、`--event EVIDENCE_AUDIT` 可读取一项操作建议与 `OPTIONAL_PLAYBOOK` 路径；恢复项目用 `RESUME`，强基线反超用 `BASELINE_STRONGER`，正式确认用 `CONFIRMATION`。路由只提供建议，不读取科研项目真值、不自动调用Agent、GPU或批准任何操作。直接访问 GitHub 的 AI 不必运行 CLI，按表选择对应文件即可。

## AI 自主执行规则（选题后默认启用，不是新阶段）

**任务选择不是等待用户逐项发 Prompt**。从当前项目最可信的 `STATE / Run / 原始代码 / 数据 / 实际用户授权` 出发，判断**此时最可能改变科研决定**的一个事件。通过 [ROUTES.json](ROUTES.json) 的 `event_advice` 读取 `action / playbook / deliverable / verify / boundary`，或直接从下表选相同动作。用户未要求每步审查时，**在已授权范围内连续完成有依赖的一组研发任务**，只在关键资源、科学主张或冻结方案变化时请求决定。

| 当前真实状态 | AI 下一项实际工作 | 本次任务交付/验证 |
|---|---|---|
| 课题刚确定、尚无可信对照 | `DATA_AUDIT` → 明确数据/真值/评估与简单强基线 | 能用真实数据重算最小基线；缺关键依赖如实阻断 |
| 已有数据与基线、准备写方法 | `MODEL_DESIGN` → `IMPLEMENTATION` | 模块/损失/推理接口、真实batch及关键行为测试 |
| 官方基线无法复现 | `BASELINE_REPRO_FAIL` | 同一目标/时域/评估的复现差异证据，不能弱化基线 |
| Loss、梯度、接口或资源异常 | `TRAINING_FAILURE` | 最小复现→诊断根因→最小修复→受影响回归 |
| 有有效结果，但无增益或消融有混杂 | `EXPERIMENT` / `ABLATION_CONFOUND` | 竞争解释及其不同预测、受控负对照、全Run结果 |
| 有效结果不足以支持稳健判断 | `STATISTICAL_INCONCLUSIVE` | 独立样本单位、效应区间、可检测性及下一证据 |
| 主张数字不可信或开始正式报告 | `CLAIM_EVIDENCE_MISMATCH` / `EVIDENCE_AUDIT` | 来源数值和版本审计；科学支持另做独立判断 |
| 发现确认集曾用于模型选择 | `CONFIRMATION_LEAK` | 隔离受影响主张与Run；不得重命名测试集继续冒充确认 |

**一次连续任务的操作周期**（不按固定阶段/批次执行）：
1. **定位**：只读必要的当前证据和文件，列最可能阻碍科学价值的风险，确定本轮交付物/实际可执行验证/授权与预算；已有工作可直接复用。AI 不得从状态文件自动推定真实用户授权。
2. **执行**：若信息足够，直接在同一个授权范围内完成相关模块/基线/测试/有界实验；已知行为可先写失败测试，未知科学假设用能区分解释的真实实验。只在处理下一个*不同*问题时再读对应 playbook，不加载全部技能。
3. **判决**：工程检查、评价合法性、机制支持、任务/论文贡献**分别定级**；`KEEP` 需要同协议有效收益，`DISCARD` 是可信无增益，`INCONCLUSIVE` 是证据不足，`INVALID` 是受影响证据不合法。任何 `PASS` 不自动升级科学结论。
4. **续做或停止**：增量更新既有 `STATE / RUNS / CLAIMS` 和原始证据路径，注明下一项最有信息价值的实验；当无科学信息增量、重大外部依赖阻断或预算用尽时建议 HOLD/收窄/向用户请求**一个具体决定**，不反复修外围工程、不静默改研究方向。

**任务粒度**：以“可以给出独立证据的研发结果”为单位，而不是以文件或每条终端命令为单位；分支有意义时可同次连续处理 2–3 项互相关联的问题，但在测试集污染、关键真值错误、GPU/费用超预算或确认性协议变更时停受影响操作。不要自动无限运行，也不要无价值的多 Agent 轮审。

## 四份精简技术手册的执行约定（非新阶段）

**按问题只读一份**，不重复加载所有手册：01 核真实数据/强基线与共同评价；02 从科学差额设计模块/损失并测试行为、梯度与异常；03 用竞争解释与 scientific/nuisance/fixed 超参设计有界实验；04 对照 Claim–Run–真值与确认集隔离审查论文主张。每份都写明「触发→操作→验收/失败分支」，复用已有 `STATE/RUNS/CLAIMS`。

数字审查可用 [audit_evidence.py](../../research_tools/audit_evidence.py)（[用法](../../research_tools/README.md)）。`SOURCE_MATCH` 不等于科学成立，`--require-identity` 用于要求来源包含已记录的版本字段；GPU、付费、正式确认和外传仍需单独授权。

## 一次综合任务如何验收

**工程**：必要接口、数值/梯度、不变量和可用输入真实通过；**实验**：真值、split、时间因果、train-only 预处理和公平评价合法；**科学**：排除至少一个关键竞争解释，并说明是否有可信增量；**论文**：独立价值、效应/不确定性、强基线和确认性证据对应主张。四层分别记录，不要求早期一次全通过。

- 无真实数据/GPU：完成本轮合法只读/CPU检查，给出单一阻断和最小授权请求；不反复使用合成数据替代真实评价。
- 首次 Pilot 无收益：先查强基线/评价/容量/关键机制的判别实验；不因一个负结果自动 STOP，也不在原假设上无界重训。
- 仅内部代理指标提升：记 `VALUE_UNVERIFIED`；低成本补真实任务或机制证据，补不到则收窄主张。
- 关键环节阻断：停**受影响的实验**，不自动撤销已有可信代码/数据/结果。

## 设计来源与适用边界

- [Superpowers](https://github.com/obra/superpowers)：行为测试、最小复现、根因诊断、完成前新证据；科研探索不僵化要求所有原型先TDD。
- [Autoresearch](https://github.com/karpathy/autoresearch)：固定评价、分支/版本、实验表、保留/回退与简单性优先；**不继承无限循环**，GPU必须获批。
- [ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep)：Idea/Experiment/Claim关联、独立Reviewer与失败经验；**不默认并行多 Agent**。
- [AI-Scientist-v2](https://github.com/SakanaAI/AI-Scientist-v2)：竞争假设与自适应探索；只借鉴有界分支搜索，不运行其自动生成代码/环境。
- [BMAD](https://github.com/bmad-code-org/BMAD-METHOD)：依据任务风险增减计划深度。
- [DVC](https://github.com/treeverse/dvc)、[MLflow](https://github.com/mlflow/mlflow)、[K-Dense](https://github.com/K-Dense-AI/scientific-agent-skills)：证据谱系与领域工具按需选用；不是必须安装新环境。

这是一套**过程规范，不是已经在真实新算法上验证有效的自动科研系统**。测量实际首次可信结果耗时、用户中断次数、无效实验、Token与最终科学证据后才可声称收益。

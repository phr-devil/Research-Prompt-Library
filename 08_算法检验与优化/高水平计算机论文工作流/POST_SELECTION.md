# 选题后研究执行引擎｜Post-Selection Research Engine v1

> **面向直接读取 GitHub 仓库的 AI Agent，而非要求用户复制 Prompt。** 本文件是第八项 v6.1 在选题确定之后的默认技术索引；总控仍是 [ORCHESTRATOR.md](ORCHESTRATOR.md)。不增加新审批阶段，不改变第09章 Step05/05-R 人工选题门禁。

## 一句话用法

用户已选定课题（或项目已有结果）时：**先读 ORCHESTRATOR.md + 本文件 + 当前项目的最新有效状态；按当前任务仅加载下面一份最相关的 playbook**。ChatGPT 负责研究主张/实验设计/重要决策，WorkBuddy/Codex 负责可访问的代码、真实数据和获授权实验。已有证据直接复用，不为“流程齐全”重跑。

**默认内循环**：科学问题/关键风险 → 真实数据与最简单可信对照 → 最小可运行算法 → 区分竞争解释的实验 → 有界修改 → KEEP/DISCARD/INCONCLUSIVE/INVALID → 在足够证据下确认论文主张。顺序可按项目状态跳跃、合并；可将一次综合任务连续完成，不逐文件征询。

## 按“下一项需要解决什么”加载一份技术手册

| 真实事件/需要 | 先读哪份 | 具体产物 | 不该做的事 |
|---|---|---|---|
| 新课题可行性、数据/标签/评价不确定 | [01 数据与可信基线](playbooks/01_DATA_BASELINE.md) | 数据契约 + 评价入口 + 公平基线结果或明确阻断 | 先造大网络；将代理标签当真值 |
| 首次开发、修复梯度/数值/接口问题 | [02 算法实现与验证](playbooks/02_BUILD_DEBUG.md) | 真实输入输出运行链路 + 相关自动化测试 + 变更证据 | 对所有代码强制重构、无因调参 |
| 有有效基线，准备提升/诊断无增益 | [03 科学实验迭代](playbooks/03_EXPERIMENT_LOOP.md) | 预期有区分力的实验、全结果与下一假设 | 无限实验；最好 seed；多次调确认集 |
| 有可信初步结果，准备正式论文主张 | [04 机制证据与确认](playbooks/04_EVIDENCE_CONFIRM.md) | Claim→Run→独立效应/统计→图表的证据矩阵 | 工程 PASS 冒充任务/机制贡献 |
| 传感器何时启动等多模态控制题 | [完整实例：触觉门控](playbooks/EXAMPLE_SENSOR_GATE.md) | 可映射到实际数据的实验合同示例 | 直接宣称离线代理指标等于控制收益 |

异常先按 [TRIAGE.md](TRIAGE.md) 判断影响范围，再按需读 [RECOVERY.md](RECOVERY.md) 的对应症状；关键科研风险出现时才启动 [04_独立科学验证.md](04_独立科学验证.md)。旧24个 Prompt 和 ROUTES.json 保留兼容，非阶段通关表。

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

## P0 技术执行规则（按触发条件加载，而非新的阶段）

四份手册已增加明确的**模块接口/Loss/复杂度合同、强基线复现、训练诊断树、信息价值实验选择、独立样本统计与封闭确认评价**。发生这些实际任务时，直接读相应手册的新增章节，不要求重新按顺序走完四份；已有等价验证只需引用证据。

报告关键论文数字或发现 Run 指标可疑时，按 [轻量数字证据核验说明](../../research_tools/README.md) 使用零额外依赖的 [audit_evidence.py](../../research_tools/audit_evidence.py)。它只检查来源数值与身份，不取代科学独立判断。确认集一旦参与开发选择，只能降为探索性证据。

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

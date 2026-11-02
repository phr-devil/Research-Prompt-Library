# Problem–Data Research Workflow | PD-RW v1.3

> **独立科研工作流仓库**。不依赖原提示词库或其他章的文件。目标是从“有价值的大问题＋可信数据（或理论证据路径）”开始，在真实观察和有限实验中逐渐发现具体科研任务、算法与论文主张。更自由的探索**不等于放宽最终论文证据**，也不承诺发表或算法增益。

## 唯一入口与最短路径

- **AI 首次进入**：只读 [START.md](START.md)，再按用户意图读 [WORKFLOW.md](WORKFLOW.md) 的对应活动；只在需要时读一份专题。已有项目优先读其最新 STATE、原始 Run/数据版本；**无需预读所有章节、24条旧Prompt或全部来源**。
- **每次用户会指定研究方向**（如视觉、NLP、机器人、传感器或明确「方向不限」）：AI仅在本轮范围内筛1–3个问题—资源组合；**每个组合默认规划3–4个互补数据库**（可多库同时开发，保留转题资源和独立确认），标明标签/分组兼容性与来源。**第一步方向确定后直接完成数据库选择、下载清单并通知用户下载；无需再让用户选择一次数据库**；不要求提前决定具体算法或先证明增益。
- **用户已有具体研究机制或旧项目**：可以直接进入对应活动（通常03/04），复用真实 STATE 和 Run；不强制重新选题，不未经确认迁移旧项目。

## 六项研究活动（可跳跃，不是六道审批门）

| 编号 | 任务与入口 | 最小交付 | 主要执行环境 |
|---|---|---|---|
| 01 | 自适应科研机会搜索并自动选库：[SEARCH_DISCOVERY.md](SEARCH_DISCOVERY.md) / [DATA_DISCOVERY.md](DATA_DISCOVERY.md) | SEARCH_HANDOFF→DIRECTION_CARD→DATA_PORTFOLIO或PROOF_PATH→下载通知 |
| 02 | 获数据/授权后核数据审计与科研现象：[DATA_DISCOVERY.md](DATA_DISCOVERY.md) / [DATA_INSIGHT.md](DATA_INSIGHT.md) | DATA_MANIFEST＋DATA_INSIGHT_CARD（可无可信现象）；封存确认资源 | 获授权的 WorkBuddy/Codex/本地环境 |
| 03 | 从现象/文献生成、比较任务并按需分层：[TASK_EXPLORATION.md](TASK_EXPLORATION.md) / [TASK_LADDER.md](TASK_LADDER.md) | PRIMARY_TASK＋NEXT_DISCRIMINATING_PROBE、备选任务按需，不提前承诺增益 | ChatGPT＋可访问真实数据的 Agent |
| 04 | 双轨算法开发：可信性能＋有依据的机制探索：[EXPERIMENT_LOOP.md](EXPERIMENT_LOOP.md) | 有效Run、ALGORITHM_HYPOTHESIS及下一最有价值实验 | 获授权的代码/实验 Agent |
| 05 | 与活动04并行收敛独立贡献：[PAPER_FIRST.md](PAPER_FIRST.md) / [TASK_EXPLORATION.md](TASK_EXPLORATION.md) | CLAIM_EVIDENCE_MAP：可信贡献候选、最强替代及实验缺口 | ChatGPT＋代码 Agent |
| 06 | 严格科学确认：[CONFIRMATION.md](CONFIRMATION.md) | 有效独立证据或 CONFIRMATION_UNAVAILABLE，论文声明边界 | 独立核验与获授权正式实验 |

**唯一主线：三个决策循环贯穿六项活动**——A 研究机会（先定宽方向→多数据库角色配置→授权后真实观察→任务）→ B 算法实证（可信L0基线、判别探针→有效 Run）→ C 科研价值（L1/L2/L3上探、下探、收窄或横向备用→严格确认）。阶段可以跳转，**不是六道强制关卡**。Task Ladder 是按数据条件启用的研究机会结构，非四级必做、非难度越高论文价值必高；L0/L1也不自动构成保底论文。下探换标签预算/部署信息时更换TASK和协议，封存holdout仍须重新核任务适配。科学止损统一见 [WORKFLOW.md](WORKFLOW.md)。

## 五条不可放宽的边界

1. **确定研究方向/多库组合 ≠ 授权下载/安装 ≠ 授权CPU拟合或GPU训练 ≠ 授权正式确认/付费/外传/投稿**；只有可核实的真实用户授权及既有已批准范围才能执行对应动作。理论分析、只读检索不自动扩展权限。
2. **可以下载完整原始数据，不等于可以开放使用确认集内容**。独立确认数据在任务发现、切片筛选、调参、机制选择阶段应保持封存。不能以反复切分同一已选测试集重新制造独立确认。
3. **算法可运行 ≠ 任务可学 ≠ 科学增量 ≠ 可发表论文**。代理目标、合成正控、内部重采样须注明支持的主张范围。
4. **早期只排已证实的关键不可替代阻断**；未知机制/未运行强基线不自动拒绝探索。正式论文确认必须严格核真值、独立单位、时间因果、公平基线、置信区间/效应和具名最近邻。
5. **输出证据优先**：默认短文本/指标/路径；图表只为判别科学问题或验证证据，01–05不自动做精美图片、长报告或PPT/PDF。避免重复读取、无效多Agent与重绘；不为省Token跳过科学验证。见[WORKFLOW.md](WORKFLOW.md) §5。

## 相关材料

- [WORKFLOW.md](WORKFLOW.md)：总控、状态路由、权限和跨活动续做
- [SEARCH_DISCOVERY.md](SEARCH_DISCOVERY.md)：按本轮范围动态扩缩、多源检索、热点/研究空白与反向近邻检查
- [DATA_DISCOVERY.md](DATA_DISCOVERY.md)：数据/基准组合、独立评价、下载与封存合同
- [DATA_INSIGHT.md](DATA_INSIGHT.md)：活动02开发池画像、数据类型分析、混杂与现象验证、DATA_INSIGHT_CARD
- [TASK_EXPLORATION.md](TASK_EXPLORATION.md)：任务科学价值×可行性比较、主/备选任务与 Claim 收敛
- [PAPER_FIRST.md](PAPER_FIRST.md)：可信性能、独立贡献与增强科学性分账，活动04↔05按需反馈
- [TASK_LADDER.md](TASK_LADDER.md)：L0–L3任务阶梯、共享资产、UP/DOWN/NARROW/LATERAL/HOLD与两类传感器示例
- [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)：任务到代码、基线、测试不变量与训练诊断（编码时按需读）
- [EXPERIMENT_LOOP.md](EXPERIMENT_LOOP.md)：真实实验、按症状探针、分层公平对照、可复现 Run 与修复；故障按需参考本库 [IMPLEMENTATION_GUIDE](IMPLEMENTATION_GUIDE.md) 的定位与恢复流程
- [CONFIRMATION.md](CONFIRMATION.md)：从开放探索到严格论文确认
- [EXAMPLE_SENSOR.md](EXAMPLE_SENSOR.md)：传感器跨平台迁移的假想执行实例（明确非实测）
- [templates/STATE.md](templates/STATE.md)：可选、极简的项目断点
- [REFERENCES.md](REFERENCES.md)：高星 GitHub 项目的具体借鉴点、限制与原始链接
- [REPLAY_PROTOCOL.md](REPLAY_PROTOCOL.md)：真实项目冻结点的盲回放和人工配对评审
- [SCENARIOS.json](SCENARIOS.json)：57个PD-RW专属的**合成**反例/风险场景；CI只校验结构和关键词，不调用模型

**工作流质量评价**：结构回归并非科研成功率。[WORKFLOW.md 的评测协议](WORKFLOW.md) 要求使用信息隔离的历史盲回放和前瞻性项目审计，在相同预算下比较任务发现、有效科研证据、过早止损、无效循环与总资源成本；**目前尚未运行真实模型对照，效果未测量**。评测按需开展，不成为每个科研项目的强制阶段。

**状态以真实项目文件和工具运行结果为准**；本文只提供指导，不能自动访问本地数据或替用户训练。

## 独立项目说明

此仓库是从 [Research-Prompt-Library](https://github.com/phr-devil/Research-Prompt-Library) 的原第十章整理的独立版本：工作流文档在仓库根目录，配有最短 AI 入口 `AGENTS.md`、结构回归测试及盲回放检查脚本。无需载入旧仓库的 08/09 章，也不绑定第三方算法 Agent。实验、运行记录及数据应放在各自项目目录，勿提交敏感数据或大型原始数据。

**离线验证**：`python -m unittest discover -s tests -v`；`python -m json.tool SCENARIOS.json > /dev/null`；盲回放：`python chapter10_replay.py responses.json`（仅校验结构，不代替科研盲审）。

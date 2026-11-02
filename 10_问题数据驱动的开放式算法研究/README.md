# 第十章｜问题—数据驱动的开放式算法研究（PD-RW v1.0）

> **独立路线，不覆盖第八章或第九章**。目标是从“有价值的大问题＋可信数据（或理论证据路径）”开始，在真实观察和有限实验中逐渐发现具体科研任务、算法与论文主张。更自由的探索**不等于放宽最终论文证据**，也不承诺发表或算法增益。

## 唯一入口与最短路径

- **AI 首次进入**：只读 [START.md](START.md)，再按用户意图读 [WORKFLOW.md](WORKFLOW.md) 的对应活动；只在需要时读一份专题。已有项目优先读其最新 STATE、原始 Run/数据版本；**无需预读所有章节、24条旧Prompt或全部来源**。
- **用户只说“传感器/具身智能，想找好数据库和研究问题”**：优先由 ChatGPT 完成问题与数据轻筛，输出 1–3 个 **问题—数据组合**（数量不强制），给出来源/许可/验证路径/关键未知，等待用户选择**组合**。还不要求完整算法命题、强基线增益或现成数据下载。
- **已选问题—数据组合**：复用或在已获许可与资源授权后准备核心真实数据；真实观察 → 具体任务候选 → 实验 → 逐步收敛；已有成果不重跑。
- **用户已给出具体科学机制并要求验证**：更适合 [第八章](../08_算法检验与优化/高水平计算机论文工作流/START.md)；失败成果挽救另走 [第九章](../09_失败算法项目挽救与转向/README.md)。不得未经用户确认自动迁移旧项目。

## 六项研究活动（可跳跃，不是六道审批门）

| 编号 | 任务与入口 | 最小交付 | 主要执行环境 |
|---|---|---|---|
| 01 | 选择问题范围及可信数据：[DATA_DISCOVERY.md](DATA_DISCOVERY.md) | AREA_DATA_CARD：问题、数据、适配、验证路径、一个最大风险 | ChatGPT（检索/论文/判断） |
| 02 | 数据准备及开放式观察：[DATA_DISCOVERY.md](DATA_DISCOVERY.md) | DATA_MANIFEST＋OBSERVATIONS；合法开发数据，不碰封存确认集 | 获授权的 WorkBuddy/Codex/本地环境 |
| 03 | 从观察发现任务：[TASK_EXPLORATION.md](TASK_EXPLORATION.md) | TASK_CANDIDATES：候选任务与最小判别 | ChatGPT＋可访问真实数据的 Agent |
| 04 | 有界算法探索：[EXPERIMENT_LOOP.md](EXPERIMENT_LOOP.md) | 可复核 Run、最佳有效版本、失败解释与下一探针 | 获授权的代码/实验 Agent |
| 05 | 选定论文主张：[TASK_EXPLORATION.md](TASK_EXPLORATION.md) | CLAIM_CANDIDATE：明确独立价值、竞争解释与证据缺口 | ChatGPT＋代码 Agent |
| 06 | 严格科学确认：[CONFIRMATION.md](CONFIRMATION.md) | 有效独立证据或 CONFIRMATION_UNAVAILABLE，论文声明边界 | 独立核验与获授权正式实验 |

**实验内循环**：真实发现 → 候选任务/方法 → 最小公正比较 → KEEP / IMPROVE / REPAIR / INCONCLUSIVE / DISCARD（只针对具体 Run/机制）→ 新观察。**研究外循环**：确认该任务还值得做、同一问题—数据组合仍有价值，还是应该向用户提出重大转向；详见 [WORKFLOW.md](WORKFLOW.md)。

## 五条不可放宽的边界

1. **选择课题 ≠ 授权下载/安装 ≠ 授权CPU拟合或GPU训练 ≠ 授权正式确认/付费/外传/投稿**；只有可核实的真实用户授权及既有已批准范围才能执行对应动作。理论分析、只读检索不自动扩展权限。
2. **可以下载完整原始数据，不等于可以开放使用确认集内容**。独立确认数据在任务发现、切片筛选、调参、机制选择阶段应保持封存。不能以反复切分同一已选测试集重新制造独立确认。
3. **算法可运行 ≠ 任务可学 ≠ 科学增量 ≠ 可发表论文**。代理目标、合成正控、内部重采样须注明支持的主张范围。
4. **早期只排已证实的关键不可替代阻断**；未知机制/未运行强基线不自动拒绝探索。正式论文确认必须严格核真值、独立单位、时间因果、公平基线、置信区间/效应和具名最近邻。
5. **有限预算、证据复用与精简输出**：按信息价值选下一步，已授权范围内连续处理相关任务；不默认多 Agent、无限实验、重复下载/审核或空白长报告。不可因 Token 省略必要科学验证。

## 相关材料

- [WORKFLOW.md](WORKFLOW.md)：总控、状态路由、权限和跨活动续做
- [DATA_DISCOVERY.md](DATA_DISCOVERY.md)：研究问题＋数据的筛选与完整性/封存合同
- [TASK_EXPLORATION.md](TASK_EXPLORATION.md)：任务产生、比较、收敛与止损
- [EXPERIMENT_LOOP.md](EXPERIMENT_LOOP.md)：实际 Agent 研发指令、实验循环、分支和排错
- [CONFIRMATION.md](CONFIRMATION.md)：从开放探索到严格论文确认
- [EXAMPLE_SENSOR.md](EXAMPLE_SENSOR.md)：传感器跨平台迁移的假想执行实例（明确非实测）
- [templates/STATE.md](templates/STATE.md)：可选、极简的项目断点
- [REFERENCES.md](REFERENCES.md)：高星 GitHub 项目的具体借鉴点、限制与原始链接

**状态以真实项目文件和工具运行结果为准**；本文只提供指导，不能自动访问本地数据或替用户训练。
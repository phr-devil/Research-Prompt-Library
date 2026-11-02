# 第十章｜问题—数据驱动的开放式算法研究（PD-RW v1.3）

> **独立路线，不覆盖第八章或第九章**。目标是从“有价值的大问题＋可信数据（或理论证据路径）”开始，在真实观察和有限实验中逐渐发现具体科研任务、算法与论文主张。更自由的探索**不等于放宽最终论文证据**，也不承诺发表或算法增益。

## 唯一入口与最短路径

- **AI 首次进入**：只读 [START.md](START.md)，再按用户意图读 [WORKFLOW.md](WORKFLOW.md) 的对应活动；只在需要时读一份专题。已有项目优先读其最新 STATE、原始 Run/数据版本；**无需预读所有章节、24条旧Prompt或全部来源**。
- **用户只说“传感器/具身智能，想找好数据库和研究问题”**：先明确**宽研究方向＋任务族**，再由ChatGPT只读筛出1–3个研究组合；**每个组合默认含2–3个独立且互补的数据库**（D1开发、D2外部复现、可选D3压力测试），标明标签/分组兼容性与来源。等用户选方向和组合后才规划下载；不要求提前决定具体算法或先证明增益。
- **已选方向与多数据库组合**：先给每库必要文件、许可、分组封存和下载顺序的PRE_DOWNLOAD_PLAN；只有获得各项实际下载权限后才分批准备数据。真实观察 → 具体TASK → 实验 → 外部独立复现；已有资产不重下。第二库暂不可得时可单库有界探索，但标SECOND_DATASET_GAP，不宣称跨数据库证据。
- **用户已给出具体科学机制并要求验证**：更适合 [第八章](../08_算法检验与优化/高水平计算机论文工作流/START.md)；失败成果挽救另走 [第九章](../09_失败算法项目挽救与转向/README.md)。不得未经用户确认自动迁移旧项目。

## 六项研究活动（可跳跃，不是六道审批门）

| 编号 | 任务与入口 | 最小交付 | 主要执行环境 |
|---|---|---|---|
| 01 | 先选研究方向，再设计多数据库组合：[DATA_DISCOVERY.md](DATA_DISCOVERY.md) | DIRECTION_CARD＋DATA_PORTFOLIO：D1/D2及可选D3的来源、角色、兼容性及风险 | ChatGPT（检索/论文/判断） |
| 02 | 多库下载计划、获授权的数据准备及开放观察：[DATA_DISCOVERY.md](DATA_DISCOVERY.md) | PRE_DOWNLOAD_PLAN＋每库DATA_MANIFEST＋OBSERVATIONS；开发/外部确认隔离 | 获授权的 WorkBuddy/Codex/本地环境 |
| 03 | 发现任务并按需设计多层Task Ladder：[TASK_EXPLORATION.md](TASK_EXPLORATION.md) / [TASK_LADDER.md](TASK_LADDER.md) | PRIMARY_TASK、L0–L3可行层级与科学主张、最小判别 | ChatGPT＋可访问真实数据的 Agent |
| 04 | 自适应有界算法探索：[EXPERIMENT_LOOP.md](EXPERIMENT_LOOP.md) | 可复核 Run、按症状诊断、下一探针与机制级止损 | 获授权的代码/实验 Agent |
| 05 | 选定论文主张：[TASK_EXPLORATION.md](TASK_EXPLORATION.md) | CLAIM_CANDIDATE：明确独立价值、竞争解释与证据缺口 | ChatGPT＋代码 Agent |
| 06 | 严格科学确认：[CONFIRMATION.md](CONFIRMATION.md) | 有效独立证据或 CONFIRMATION_UNAVAILABLE，论文声明边界 | 独立核验与获授权正式实验 |

**唯一主线：三个决策循环贯穿六项活动**——A 研究机会（先定宽方向→多数据库角色配置→授权后真实观察→任务）→ B 算法实证（可信L0基线、判别探针→有效 Run）→ C 科研价值（L1/L2/L3上探、下探、收窄或横向备用→严格确认）。阶段可以跳转，**不是六道强制关卡**。Task Ladder 是按数据条件启用的研究机会结构，非四级必做、非难度越高论文价值必高；L0/L1也不自动构成保底论文。下探换标签预算/部署信息时更换TASK和协议，封存holdout仍须重新核任务适配。科学止损统一见 [WORKFLOW.md](WORKFLOW.md)。

## 五条不可放宽的边界

1. **确定研究方向/多库组合 ≠ 授权下载/安装 ≠ 授权CPU拟合或GPU训练 ≠ 授权正式确认/付费/外传/投稿**；只有可核实的真实用户授权及既有已批准范围才能执行对应动作。理论分析、只读检索不自动扩展权限。
2. **可以下载完整原始数据，不等于可以开放使用确认集内容**。独立确认数据在任务发现、切片筛选、调参、机制选择阶段应保持封存。不能以反复切分同一已选测试集重新制造独立确认。
3. **算法可运行 ≠ 任务可学 ≠ 科学增量 ≠ 可发表论文**。代理目标、合成正控、内部重采样须注明支持的主张范围。
4. **早期只排已证实的关键不可替代阻断**；未知机制/未运行强基线不自动拒绝探索。正式论文确认必须严格核真值、独立单位、时间因果、公平基线、置信区间/效应和具名最近邻。
5. **有限预算、证据复用与精简输出**：按信息价值选下一步，已授权范围内连续处理相关任务；不默认多 Agent、无限实验、重复下载/审核或空白长报告。不可因 Token 省略必要科学验证。

## 相关材料

- [WORKFLOW.md](WORKFLOW.md)：总控、状态路由、权限和跨活动续做
- [DATA_DISCOVERY.md](DATA_DISCOVERY.md)：研究大方向搜索、数据库选择理由、研究问题/数据适配与封存合同
- [TASK_EXPLORATION.md](TASK_EXPLORATION.md)：任务科学价值×可行性比较、主/备选任务与 Claim 收敛
- [TASK_LADDER.md](TASK_LADDER.md)：L0–L3任务阶梯、共享资产、UP/DOWN/NARROW/LATERAL/HOLD与两类传感器示例
- [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)：任务到代码、基线、测试不变量与训练诊断（编码时按需读）
- [EXPERIMENT_LOOP.md](EXPERIMENT_LOOP.md)：真实实验、按症状探针、分层公平对照、可复现 Run 与修复；故障按需复用第八章 [TRIAGE](../08_算法检验与优化/高水平计算机论文工作流/TRIAGE.md) / [RECOVERY](../08_算法检验与优化/高水平计算机论文工作流/RECOVERY.md)
- [CONFIRMATION.md](CONFIRMATION.md)：从开放探索到严格论文确认
- [EXAMPLE_SENSOR.md](EXAMPLE_SENSOR.md)：传感器跨平台迁移的假想执行实例（明确非实测）
- [templates/STATE.md](templates/STATE.md)：可选、极简的项目断点
- [REFERENCES.md](REFERENCES.md)：高星 GitHub 项目的具体借鉴点、限制与原始链接
- [REPLAY_PROTOCOL.md](REPLAY_PROTOCOL.md)：真实项目冻结点的盲回放和人工配对评审
- [SCENARIOS.json](SCENARIOS.json)：24个第十章专属的**合成**反例/风险场景；CI只校验结构和关键词，不调用模型

**工作流质量评价**：结构回归并非科研成功率。[WORKFLOW.md 的评测协议](WORKFLOW.md) 要求使用信息隔离的历史盲回放和前瞻性项目审计，在相同预算下比较任务发现、有效科研证据、过早止损、无效循环与总资源成本；**目前尚未运行真实模型对照，效果未测量**。评测按需开展，不成为每个科研项目的强制阶段。

**状态以真实项目文件和工具运行结果为准**；本文只提供指导，不能自动访问本地数据或替用户训练。
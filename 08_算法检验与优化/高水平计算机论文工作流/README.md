# Research Workflow v6.1｜原型优先，按需复杂

**默认只做：问题 → 最小可信算法/基线 → 实验迭代 → 需要时才做科学深入审核。**

**面向 AI 自主读取的选题后技术入口**：[POST_SELECTION.md](POST_SELECTION.md)。 已选课题研发的细化版增加模块/Loss 合同、基线复现、训练诊断、统计设计和 [数值来源核验工具](../../research_tools/README.md)（只读、不等于独立科学验收）。其按需手册覆盖 [数据/强基线](playbooks/01_DATA_BASELINE.md)、[算法实现/排错](playbooks/02_BUILD_DEBUG.md)、[有界实验迭代](playbooks/03_EXPERIMENT_LOOP.md)、[正式科学证据](playbooks/04_EVIDENCE_CONFIRM.md)，并有 [传感器门控实例](playbooks/EXAMPLE_SENSOR_GATE.md)。已选题或续做科研项目时，AI 在读完总控后只读所需手册；这些文件提供**操作方法与具体验收**，不要求用户粘贴完整 Prompt。

**第①类「科学选题」默认全程在 ChatGPT 完成**（01-A～01-D：候选题、文献/创新性碰撞、可证伪命题、算法骨架、方向判断）。未明确命题可按需使用[科研机会漏斗F1–F5](IDEA_FUNNEL.md)，内部广泛探索与渐进收敛后等用户选题；不为分工而切换到 WorkBuddy/Codex。需要实际读取/运行本地代码或数据才按授权移交执行平台；关键独立反证才另用隔离模型/审查者。五类仍按需使用，不新增选题门禁。详见 [①科学选题](01_科学选题与跨AI审核.md)。

**[从 START.md 启动](START.md)**：一次提供科研目标、已有项目/数据以及实际授权。运行 Agent 平时只需要 [ORCHESTRATOR.md](ORCHESTRATOR.md) 和现有科研项目证据，**不预先加载24条历史Prompt、全部48条故障、全套Skills和多模型审查**。有结果的项目直接恢复继续开发；首次结果没有提升也不自动判STOP。

## 最短使用路径

**按事件建议（非自动执行）**：选题用 `python workflow_route.py --event TOPIC_EXPLORATION`；已明确目标才用 `--event NEW_PROJECT`，其他如 `RESUME` / `BASELINE_STRONGER`。只读取一个处理建议和可选专题；真正的Agent必须自行核实运行结果与授权，不能把本脚本当作后台科研执行器。

| 何时 | 默认动作 | 需要时才读 |
|---|---|---|
| 仍在探索选题 | **ChatGPT** 使用可选F1–F4漏斗（机会→多命题→轻筛→定向收敛），F5交用户选择；不强制跨AI审核 | [IDEA_FUNNEL.md](IDEA_FUNNEL.md)、`01-A/B/C/D` |
| 已有明确目标、准备开发 | 一句话科学假设 + 成功价值反推；最小数据核查后在授权内直接做基线/MVP | [POST_SELECTION.md](POST_SELECTION.md) → 只选一份 playbook；必要时 `02-B/03-A` |
| 已有算法或旧实验 | 复用有效代码与Run，在现有预算内修改一个主要机制、测试、记录保留/撤回 | `03-C/D` |
| 结果反常、科学价值未证 | 最小诊断，按现象检索真实失败教训，必要时用户选择 | [LESSONS.md](LESSONS.md)、[RECOVERY.md](RECOVERY.md)、`02-E/03-E` |
| 拟正式宣称论文贡献 | 严格核数据/真值、强基线、冻结协议、统计、确认性实验、独立复核 | `03-B/F`、`04-A/B/C` |
| 写稿与投稿 | 可并行起草未验证的真实内容，正式投稿前核查证据与作者权限 | `05-A/B/C/D/E` |

**HFD 的止损教训**：数据PASS≠科学命题有真值；修复前问能否改变科研决定，缺关键真实数据时一次请求授权、不反复合成替代。详见 [LESSONS.md 的L5](LESSONS.md)。

**RevGraph 的价值教训**：任务数与工程PASS不是论文贡献；选题时一句成功价值反推、MVP时区分代理与实际/机制价值、关键结果时再核最近邻与独立贡献。详见 [LESSONS.md 的L3](LESSONS.md)。

**内循环**：假设 → 代码/实验 → 结果 → KEEP/DISCARD/INCONCLUSIVE/INVALID → 下一项信息增量。**外循环**只在首次可信结果、机制异常、反复无信息、科学主张改变或正式确认时触发；不设置机械次数，不反复选题。

## 保留下来的科学底线（没有新强制阶段）

- [TRIAGE.md](TRIAGE.md) / [TRIAGE_POLICY.json](TRIAGE_POLICY.json)：致命阻断受影响行动、一般风险用户选继续或修复、轻微记录自动过；未知先做最小核查。
- [RECOVERY.md](RECOVERY.md) / [REPAIR_ROUTES.json](REPAIR_ROUTES.json)：原24场景48种典型失败与根因修复、回退，**仅真实故障按需调用**。
- [LESSONS.md](LESSONS.md)：CARE-Touch、PhysTok、RevGraph、CAR-IMU 的历史科学失败教训，**按相似症状检索，不是必做审核清单**。
- `research/STATE.md`、`RUNS.tsv`、`CLAIMS.md` 及真实来源的证据关系保留，优先复用项目现有文件；[精简状态模板](templates/STATE.md) 仅供新项目可选使用。
- 新GPU、付费、数据外传、冻结正式确认性实验与投稿仍需相应独立真实授权；第09章 [失败项目转向](../../09_失败算法项目挽救与转向/README.md) 的 P1/P2/P3 用户门禁不变。

## 历史工具库（完全保留，不强制按序）

[24条场景与触发条件](ROUTES.json)：[选题](01_科学选题与跨AI审核.md) · [数据/Pilot](02_最小科学验证与决策.md) · [研发](03_完整算法研发与正式实验.md) · [独立复核](04_独立科学验证.md) · [论文](05_论文撰写与投稿.md)。本地只读工具 `python workflow_route.py --id 03-E` 提取单个场景；`--repair 03-E` 读取该场景的两个故障示例。脚本不执行研究，不认证用户授权。历史场景已移除强制顺序触发，使用时只按对应问题查专业任务逻辑，**不得反向强制主流程补齐此前阶段**。

[共享科研规则与技能来源](00_统一规则与Skill映射.md)、[可选 SKILL.md](SKILL.md)、[AGENTS.md 模板](AGENTS_RESEARCH_TEMPLATE.md) 也是按需参考，不要求预装第三方Skill，也不要求开多个Agent。

**方法参考**：[Karpathy Autoresearch](https://github.com/karpathy/autoresearch) 的简洁实验循环、[Orchestra Research](https://github.com/Orchestra-Research/AI-Research-SKILLs) 的研究内外循环、[Superpowers](https://github.com/obra/superpowers) 的根因诊断、[BMad](https://github.com/bmad-code-org/BMAD-METHOD) 的任务规模自适应、[Anthropic Skills](https://github.com/anthropics/skills) 的按需加载、[GSD Core](https://github.com/open-gsd/gsd-core) 的进度恢复。借鉴方法，不宣称外部工具已安装，也不照搬无限实验循环。

**验证边界**：CI只验证静态指引/脚本与路由，未证明实际科研成功率、Token节省或真实Agent长周期自主性。

## 如何检验是否真的不繁琐

GitHub CI的行为矩阵只验证 `NEW_PROJECT → NO_GAIN → BASELINE_STRONGER → CONFIRMATION` 等事件可获得正确的**只读建议**，以及人工HOLD、无授权正式确认与第09章选题选择仍不能自动放行。它并不能监控真实的工作进程，真实迭代需要有文件/工具能力的Agent执行。真实工作流A/B要记录同一任务的**首次可信结果时间、用户决策次数、实测Token、无效实验次数、最终科学正确性**；没有实际模型输出不报告收益百分比。

# Research Workflow v6.1｜原型优先，按需复杂

**默认只做：问题 → 最小可信算法/基线 → 实验迭代 → 需要时才做科学深入审核。**

**[从 START.md 启动](START.md)**：一次提供科研目标、已有项目/数据以及实际授权。运行 Agent 平时只需要 [ORCHESTRATOR.md](ORCHESTRATOR.md) 和现有科研项目证据，**不预先加载24条历史Prompt、全部48条故障、全套Skills和多模型审查**。有结果的项目直接恢复继续开发；首次结果没有提升也不自动判STOP。

## 最短使用路径

**按事件建议（非自动执行）**：`python workflow_route.py --event NEW_PROJECT` / `--event RESUME` / `--event BASELINE_STRONGER`。只读取一个处理建议和可选专题；真正的Agent必须自行核实运行结果与授权，不能把本脚本当作后台科研执行器。

| 何时 | 默认动作 | 需要时才读 |
|---|---|---|
| 刚开始、目标模糊 | 一句话科学假设 + 成功价值反推；快速看真实数据/最简单对照；能动手则直接做MVP | `01-A/B`、`02-B` |
| 已有算法或旧实验 | 复用有效代码与Run，在现有预算内修改一个主要机制、测试、记录保留/撤回 | `03-C/D` |
| 结果反常、科学价值未证 | 最小诊断，按现象检索真实失败教训，必要时用户选择 | [LESSONS.md](LESSONS.md)、[RECOVERY.md](RECOVERY.md)、`02-E/03-E` |
| 拟正式宣称论文贡献 | 严格核数据/真值、强基线、冻结协议、统计、确认性实验、独立复核 | `03-B/F`、`04-A/B/C` |
| 写稿与投稿 | 可并行起草未验证的真实内容，正式投稿前核查证据与作者权限 | `05-A/B/C/D/E` |

**内循环**：假设 → 代码/实验 → 结果 → KEEP/DISCARD/INCONCLUSIVE/INVALID → 下一项信息增量。**外循环**只在首次可信结果、机制异常、反复无信息、科学主张改变或正式确认时触发；不设置机械次数，不反复选题。

## 保留下来的科学底线（没有新强制阶段）

- [TRIAGE.md](TRIAGE.md) / [TRIAGE_POLICY.json](TRIAGE_POLICY.json)：致命阻断受影响行动、一般风险用户选继续或修复、轻微记录自动过；未知先做最小核查。
- [RECOVERY.md](RECOVERY.md) / [REPAIR_ROUTES.json](REPAIR_ROUTES.json)：原24场景48种典型失败与根因修复、回退，**仅真实故障按需调用**。
- [LESSONS.md](LESSONS.md)：CARE-Touch、PhysTok、RevGraph、CAR-IMU 的历史科学失败教训，**按相似症状检索，不是必做审核清单**。
- `research/STATE.md`、`RUNS.tsv`、`CLAIMS.md` 及真实来源的证据关系保留，优先复用项目现有文件；[精简状态模板](templates/STATE.md) 仅供新项目可选使用。
- 新GPU、付费、数据外传、冻结正式确认性实验与投稿仍需相应独立真实授权；第09章 [失败项目转向](../../09_失败算法项目挽救与转向/README.md) 的 P1/P2/P3 用户门禁不变。

## 历史工具库（完全保留，不强制按序）

[24条场景与触发条件](ROUTES.json)：[选题](01_科学选题与跨AI审核.md) · [数据/Pilot](02_最小科学验证与决策.md) · [研发](03_完整算法研发与正式实验.md) · [独立复核](04_独立科学验证.md) · [论文](05_论文撰写与投稿.md)。本地只读工具 `python workflow_route.py --id 03-E` 提取单个场景；`--repair 03-E` 读取该场景的两个故障示例。脚本不执行研究，不认证用户授权。历史场景内带有五阶段描述，只在遇到对应问题时参考其专业任务逻辑，**不得反向强制主流程补齐此前阶段**。

[共享科研规则与技能来源](00_统一规则与Skill映射.md)、[可选 SKILL.md](SKILL.md)、[AGENTS.md 模板](AGENTS_RESEARCH_TEMPLATE.md) 也是按需参考，不要求预装第三方Skill，也不要求开多个Agent。

**方法参考**：[Karpathy Autoresearch](https://github.com/karpathy/autoresearch) 的简洁实验循环、[Orchestra Research](https://github.com/Orchestra-Research/AI-Research-SKILLs) 的研究内外循环、[Superpowers](https://github.com/obra/superpowers) 的根因诊断、[BMad](https://github.com/bmad-code-org/BMAD-METHOD) 的任务规模自适应、[Anthropic Skills](https://github.com/anthropics/skills) 的按需加载、[GSD Core](https://github.com/open-gsd/gsd-core) 的进度恢复。借鉴方法，不宣称外部工具已安装，也不照搬无限实验循环。

**验证边界**：CI只验证静态指引/脚本与路由，未证明实际科研成功率、Token节省或真实Agent长周期自主性。

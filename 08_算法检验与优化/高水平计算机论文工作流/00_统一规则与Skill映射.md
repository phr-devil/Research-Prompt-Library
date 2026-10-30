# 科研真实性与按需 Skill 索引（v6.0 支持材料）

> **本文件不是默认启动前必读的检查清单。** 日常入口仅需 [ORCHESTRATOR.md](ORCHESTRATOR.md)。发现专门任务时再定位下面的规则和对应技能；旧五阶段24条Prompt是按需工具库，不是必须先完成的审批链。

## 科研最小底线

- 科研真实性 > 可复现性 > 创新价值 > 额外审核与Token效率；不能为赶进度编造有效性、文献、独立实验、GPU权限或结果。
- 首先解决**当前任务需要的**数据许可、标签/物理含义、时间因果与分组切分。train-only预处理、独立统计单位、公平简单强基线、正式确认性test隔离不能被“原型优先”豁免；对无关项不做超前审查。
- RevGraph经验：用一句话“即使内部指标全通过，相对近邻方法仍新增什么任务/机制/理论贡献？”作为轻量假设，不要求前期证明；在关键结果/正式宣称时补证据。详见 [LESSONS.md](LESSONS.md)。
- 开发中的 `KEEP/DISCARD/INCONCLUSIVE/INVALID` 与正式论文声明分开，保存原始Run/Claim/commit/数据配置、全seed与失败证据；工程PASS不能代替科学结论。
- 实际 GPU、付费、外传、冻结确认性协议、正式实验或投稿，必须针对动作/预算/停止条件取得真实用户授权；可在已获批范围连续完成关联任务，不意味着自动加预算。
- 相同风险只在有可信后续真实用户消息且目标/数据/协议/权限均未变化时复用选择；用户明确HOLD优先。致命阻断相关动作，一般风险供选择，轻微记录后跳过；UNKNOWN只做必要的最低成本核查。
- 独立第09章 Step05仍必须呈现P1/P2/P3，等待真实后续选择，才可执行05-R/06。

## 低Token运行方式

只加载当前行动需要的文件与证据；同一批次内先完成关联实现、测试与修复；不默认读取全部旧Prompt/Skills/失败案例，不反复读取历史研究报告。结果只输出**重要变更、原始证据、下一项有价值行动/唯一需要的决定**。既有 `research/STATE.md`、`RUNS.tsv`、`CLAIMS.md` 优先映射复用，不复制一套新账本；只需相关材料时才读取 [任务合同](templates/TASK_CONTRACT.md) 与 [证据索引](templates/EVIDENCE_INDEX.md)。

## 4. Skill 选择规则（按需加载，禁止全量加载）

| 代号 | 用途和真实出处 | ChatGPT | Codex/审查 Agent |
|---|---|---|---|
| RS-P | [ResearchStudio Paper-Search](https://github.com/microsoft/ResearchStudio/blob/main/ResearchStudio-Idea/skills/paper_search/SKILL.md) | 阅读参考 + 自有搜索工具 | 仅要使用其跨库脚本时安装依赖 |
| RS-I | [ResearchStudio Idea-Spark](https://github.com/microsoft/ResearchStudio/blob/main/ResearchStudio-Idea/skills/idea_spark/SKILL.md) | 阅读参考、选题时用 | 可选安装 |
| RS-S | [ResearchStudio Scoop-Check](https://github.com/microsoft/ResearchStudio/blob/main/ResearchStudio-Idea/skills/scoop_check/SKILL.md) | 阅读参考、创新性检索 | 可选安装 |
| RS-Q | [ResearchStudio Idea-Quality](https://github.com/microsoft/ResearchStudio/blob/main/ResearchStudio-Idea/evaluation/idea_quality/SKILL.md) | 可选参考；不把分数当成功率 | 可选 |
| SPS | [Scientific Problem Selection](https://github.com/anthropics/knowledge-work-plugins/blob/main/bio-research/skills/scientific-problem-selection/SKILL.md) | 风险/决策参考 | 按需参考 |
| SP | [Superpowers](https://github.com/obra/superpowers) | 按需阅读方法 | **推荐安装**；明确调用 `test-driven-development`、`systematic-debugging`、`verification-before-completion`、`writing-plans`；以真实 Skill 列表为准 |
| AR | [Karpathy Autoresearch program.md](https://github.com/karpathy/autoresearch/blob/master/program.md) | 参考固定评估 | **只借鉴受控循环**，不继承其无限运行指令 |
| ARA | [Orchestra Rigor Reviewer](https://github.com/Orchestra-Research/AI-Research-SKILLs/blob/main/22-agent-native-research-artifact/rigor-reviewer/SKILL.md) | 阅读科学核查方法 | 独立 Agent 按需安装/阅读 |
| MLP | [Orchestra ML Paper Writing](https://github.com/Orchestra-Research/AI-Research-SKILLs/blob/main/20-ml-paper-writing/ml-paper-writing/SKILL.md) | 阅读写作方法 | 绘图/LaTeX 按需 |
| OSC | [OpenAI Skill Creator](https://github.com/openai/skills/blob/main/skills/.system/skill-creator/SKILL.md) | 仅设计/改 Skill 时参考 | **只在维护 Skill 本身时使用** |

**调用语义**：`[阅读参考]` ＝本轮按需读取指定 GitHub `SKILL.md` 并使用现有工具；`[原生调用]` ＝运行环境已经安装并识别该 Skill；`[方法借鉴]` ＝只参考方法，**不运行原项目**。不强制为了凑 Skill 数量而调用。


## 参考设计

[Autoresearch](https://github.com/karpathy/autoresearch)、[Orchestra Research AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs)、[Superpowers](https://github.com/obra/superpowers)、[BMad](https://github.com/bmad-code-org/BMAD-METHOD)、[Anthropic Skills](https://github.com/anthropics/skills)。阅读公开Skill不代表其在当前平台安装或执行。

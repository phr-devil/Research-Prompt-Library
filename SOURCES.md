## 2026-10-31 RevGraph 科学价值复盘进入 v6.1（非新增审核阶段）

在第八项 [LESSONS.md](08_算法检验与优化/高水平计算机论文工作流/LESSONS.md) 的L3保留 RevGraph“任务/工程PASS多但论文贡献未证”的三类教训：工程验收不等于学术创新；内部传播代理指标不能代替真实任务/独立机制证据；不能把近邻差异与成功后贡献判断拖到科研末期。仅在已有的启动、MVP和事件型科学外循环中加入成功价值反推、代理/任务或机制价值并列核查、关键结果时的竞争力复评；新增 `PROXY_ONLY_GAIN` 只读事件建议，不增加必经步骤或GPU权限。注意本仓库无RevGraph原始Run，相关历史结果仍需回到真实科研仓库验证，不能据此推断论文质量或宣称真实下游实验已完成。

## 2026-10-31 第08项 v6.1 实际执行一致性修正

去除24条历史Prompt中遗留的自动跨阶段“必做”条件；保留正式科研证据与真实用户授权门禁。旧路由exit_gate改为纯事件型只读建议；REPAIRABLE在**已核验既有许可、无重大科学变化**时可有界自动诊断；第09章优先三候选，证据只支持1–2个时带shortfall_reason并等待真实用户选择，不强制凑数。历史教训明确来源需由对应科研仓库的原始Run/配置验证。本次补充离线行为回归测试，不代表已有真实模型端到端效率或科学成功率实测。

## 2026-10-31 第08项 v6.0 重构：默认简单、按需复杂

基于原第八项五阶段24条场景、48个失败修复条目和RevGraph/CARE-Touch/PhysTok/CAR-IMU的历史教训，重构默认入口为「最小原型→结果驱动迭代→重要事件科学反思→正式成果验证」。历史场景、修复和科学底线全部保留为按需工具；新增 [LESSONS.md](08_算法检验与优化/高水平计算机论文工作流/LESSONS.md)。原[Autoresearch](https://github.com/karpathy/autoresearch)的实验循环、[Orchestra](https://github.com/Orchestra-Research/AI-Research-SKILLs)的双循环、[Superpowers](https://github.com/obra/superpowers)的根因修复、[BMad](https://github.com/bmad-code-org/BMAD-METHOD)与[Anthropic Skills](https://github.com/anthropics/skills)的自适应/按需加载均只借鉴设计，不安装第三方工具、不复制原文，也不照搬无上限训练。GitHub CI只验证静态/离线兼容，真实研发成功率与token效果尚未测量。

## 2026-10-30 第08项 v5.4 决策恢复与代码围栏审查

修复真实用户明确 HOLD/先修/改题被默认路由忽略、UNKNOWN严重度缺少安全分支、旧风险决策在数据/协议/主张变化后错误复用；并对24条场景的标题文件归属和Markdown text代码块闭合完整性进行严格检查。纯Python辅助决策只能提供建议，不读取真实聊天身份、不授权GPU或正式投稿。本轮为离线逻辑审计，没有真实模型对比或完成率实测。

## 2026-10-29 第08项 v5.3 轻量工作流审查修复

审核 v5.2 的状态字段、路由触发、场景必做性和人工风险选择，确认旧版本可能重复要求用户授权、把运行成功当作科学验证，以及在风险未解决时误放行。v5.3 将24条场景归为 as_needed / required_for_action / conditional，新增纯离线严重度分支推演（不能验证真实用户授权或自动判断实测科学有效性）、状态区分、风险决策去重与场景Prompt冗余精简；保留数据/测试隔离和第09章人类选择边界。基于 GitHub 原始文件实审，没有宣称开展真实科研项目现场效果评测。

# GitHub 参考来源与改写关系

> 主要来源核查日期：2026-10-26；V02/V03 补充项目核查：2026-10-27。Star 数是当日 GitHub 仓库公开数据的快照，**不代表提示词效果排名**。本项目保存的是基于公开文字 Prompt 或 Skill/Agent 工作机制的独立适配稿，不批量复制第三方原文。

## 主要参考仓库

| 仓库 | Stars（2026-10-26） | 许可元数据（仅供提示） |
|---|---:|---|
| [f/prompts.chat](https://github.com/f/prompts.chat) | 174,579 | 未核明 SPDX 许可 |
| [PlexPt/awesome-chatgpt-prompts-zh](https://github.com/PlexPt/awesome-chatgpt-prompts-zh) | 64,014 | MIT |
| [danielmiessler/fabric](https://github.com/danielmiessler/fabric) | 44,429 | MIT |
| [Leey21/awesome-ai-research-writing](https://github.com/Leey21/awesome-ai-research-writing) | 35,257 | 未见标准许可字段 |
| [langgptai/wonderful-prompts](https://github.com/langgptai/wonderful-prompts) | 6,366 | MIT |
| [ahmetbersoz/chatgpt-prompts-for-academic-writing](https://github.com/ahmetbersoz/chatgpt-prompts-for-academic-writing) | 5,012 | 未见标准许可字段 |
| [bohyy/academic-ai-prompt](https://github.com/bohyy/academic-ai-prompt) | 2,211 | MIT |

许可字段仅记录仓库元数据，不构成法律授权结论；引用或再发布原始 Prompt 全文前，请单独检查其实际许可证、贡献者及署名条款。

## 20 条 Prompt 的具体来源与适配性质

| 模板 | 原始来源链接（可能指向具体章节或项目首页） | 改写性质 |
|---|---|---|
| S01 全球范围系统检索 | [来源 1](https://github.com/langgptai/wonderful-prompts#ai-搜索提示词) · [来源 2](https://github.com/ahmetbersoz/chatgpt-prompts-for-academic-writing#literature-review) | 借鉴基于来源回答、缺少证据就说明的写法；任务模式、跨国资格审查及去重流程为本库适配内容。 |
| S02 官方网站与资格核实 | [来源 1](https://github.com/langgptai/wonderful-prompts) · [来源 2](https://github.com/danielmiessler/fabric/blob/main/data/patterns/analyze_paper/system.md) · [来源 3](https://github.com/ahmetbersoz/chatgpt-prompts-for-academic-writing) | 融合改写 |
| R01 科研选题与创新性探索 | [来源 1](https://github.com/ahmetbersoz/chatgpt-prompts-for-academic-writing) · [来源 2](https://github.com/bohyy/academic-ai-prompt) · [来源 3](https://github.com/danielmiessler/fabric/blob/main/data/patterns/analyze_paper/system.md) | 融合改写 |
| R02 实验与算法方案设计及结果审计 | [来源 1](https://github.com/danielmiessler/fabric/blob/main/data/patterns/analyze_paper/system.md) · [来源 2](https://github.com/ahmetbersoz/chatgpt-prompts-for-academic-writing#methodology) · [来源 3](https://github.com/Leey21/awesome-ai-research-writing#实验分析) | 借鉴论文严谨性审核、实验方案与负结果实述方法；GO/HOLD/STOP、失败归因和重构门槛为本库原创整合。 |
| P01 论文结构、论证逻辑与图表规划 | [来源 1](https://github.com/ahmetbersoz/chatgpt-prompts-for-academic-writing#outline) · [来源 2](https://github.com/Leey21/awesome-ai-research-writing#论文架构图) · [来源 3](https://github.com/danielmiessler/fabric/blob/main/data/patterns/analyze_paper/system.md) | 方法融合：借鉴论文提纲与证据审查；图表—主张矩阵、仅输出所选模式和真实证据边界为本库改写。 |
| P02 SCI 论文章节正文撰写 | [来源 1](https://github.com/danielmiessler/fabric/blob/main/data/patterns/create_academic_paper/system.md) · [来源 2](https://github.com/ahmetbersoz/chatgpt-prompts-for-academic-writing) · [来源 3](https://github.com/bohyy/academic-ai-prompt) · [来源 4](https://github.com/Leey21/awesome-ai-research-writing#part-i-%E5%86%99%E4%BD%9C-prompt-%E9%9B%86%E5%90%88) | 融合改写 |
| P03 SCI 论文保守型语言润色与审稿 | [来源 1](https://github.com/Leey21/awesome-ai-research-writing#表达润色英文论文) · [来源 2](https://github.com/Leey21/awesome-ai-research-writing#逻辑检查) · [来源 3](https://github.com/Leey21/awesome-ai-research-writing#论文整体以-reviewer-视角进行审视) · [来源 4](https://github.com/danielmiessler/fabric/blob/main/data/patterns/improve_writing/system.md) | 借鉴原仓库对润色、逻辑审查、审稿分别设定任务和输出的组织方式；三个模式合并为一个可复制模板。 |
| G01 资助方向适配与基金课题规划 | [来源 1](https://github.com/ahmetbersoz/chatgpt-prompts-for-academic-writing#brainstorming) · [来源 2](https://github.com/ahmetbersoz/chatgpt-prompts-for-academic-writing#planpresentation) · [来源 3](https://github.com/danielmiessler/fabric/blob/main/data/patterns/analyze_paper/system.md) | 跨场景改写：借鉴选题、研究计划和证据审查；日本基金资格、校内推荐、既定题目优先及真实预算约束为本库独立设计。 |
| G02 科研基金申请书逐栏撰写 | [来源 1](https://github.com/ahmetbersoz/chatgpt-prompts-for-academic-writing#planpresentation) · [来源 2](https://github.com/ahmetbersoz/chatgpt-prompts-for-academic-writing#methodology) · [来源 3](https://github.com/danielmiessler/fabric/blob/main/data/patterns/create_academic_paper/system.md) | 没有核实到高星日本研究助成的逐栏专用 Prompt。本文件借鉴通用研究计划、方法写作的文字指令，再独立加入表格、官方资格、预算和日语约束。 |
| G03 基金申请书全面审查与原文替换 | [来源 1](https://github.com/Leey21/awesome-ai-research-writing#part-i-%E5%86%99%E4%BD%9C-prompt-%E9%9B%86%E5%90%88) · [来源 2](https://github.com/danielmiessler/fabric/blob/main/data/patterns/improve_writing/system.md) · [来源 3](https://github.com/ahmetbersoz/chatgpt-prompts-for-academic-writing) | 跨场景改编；无高星日本基金专用 Prompt |
| L01 中英日专业双向翻译 | [来源 1](https://github.com/Leey21/awesome-ai-research-writing#part-i-%E5%86%99%E4%BD%9C-prompt-%E9%9B%86%E5%90%88) · [来源 2](https://github.com/PlexPt/awesome-chatgpt-prompts-zh) · [来源 3](https://github.com/f/prompts.chat/blob/main/PROMPTS.md) | 融合改写 |
| L02 自然表达与去机械化AI腔 | [来源 1](https://github.com/danielmiessler/fabric/blob/main/data/patterns/improve_writing/system.md) · [来源 2](https://github.com/Leey21/awesome-ai-research-writing#表达润色中文论文) · [来源 3](https://github.com/haidrrrry/humanize-ai-writing/blob/main/PROMPT.md) | 方法融合：借鉴清晰、简洁和保留原意；不采用外部模板的绝对禁词表或检测规避导向，默认只输出成稿以节省阅读时间。 |
| M01 科研长对话完整归档与跨对话接力 | [来源 1](https://github.com/danielmiessler/fabric/blob/main/data/patterns/summarize/system.md) · [来源 2](https://github.com/danielmiessler/fabric/blob/main/data/patterns/analyze_paper/system.md) | 借鉴 Markdown 摘要与证据质量整理的输出结构；双层科研接力、状态与来源、失败路线归档为本库自主设计。 |
| M02 多文件事实、逻辑和语言交叉审查 | [来源 1](https://github.com/Leey21/awesome-ai-research-writing#part-i-%E5%86%99%E4%BD%9C-prompt-%E9%9B%86%E5%90%88) · [来源 2](https://github.com/danielmiessler/fabric/blob/main/data/patterns/analyze_paper/system.md) · [来源 3](https://github.com/danielmiessler/fabric/blob/main/data/patterns/improve_writing/system.md) | 融合改写 |
| X01 Codex 科研代码结果审计与下一步指令 | [来源 1](https://github.com/danielmiessler/fabric/blob/main/data/patterns/analyze_paper/system.md) · [来源 2](https://github.com/danielmiessler/fabric/blob/main/data/patterns/summarize/system.md) | 基于分析与总结 Prompt 结构自行适配；并非 GitHub 现成 Codex Prompt |
| X02 日英双语正式邮件撰写与回复 | [来源 1](https://github.com/danielmiessler/fabric/blob/main/data/patterns/create_formal_email/system.md) · [来源 2](https://github.com/danielmiessler/fabric/blob/main/data/patterns/improve_writing/system.md) | 直接参考正式通信的意图、关系和语气核对；日语大学事务与供应商情境、默认单稿及不擅自发送为本库适配。 |
| X03 日本作文比赛策划与日语自然化写作 | [来源 1](https://github.com/danielmiessler/fabric/blob/main/data/patterns/improve_writing/system.md) · [来源 2](https://github.com/ahmetbersoz/chatgpt-prompts-for-academic-writing#brainstorming) | 跨场景改写：参考写作润色与分段构思结构；比赛规则、AI 代写限制和真实叙事约束并非原仓库的现成作文比赛 Prompt。 |
| V01 目标驱动的算法检验任务规划 | [Superpowers](https://github.com/obra/superpowers) · [GSD](https://github.com/gsd-build/get-shit-done) · [Beads](https://github.com/gastownhall/beads) | 概念级参考连续执行、验收反推与任务依赖管理；针对科研验证的任务规划与 Token 效率规则为原创改写，不安装或复制第三方 Skill。 |
| V02 独立审查触发与范围判断 | [Superpowers](https://github.com/obra/superpowers) · [Awesome Copilot](https://github.com/github/awesome-copilot) · [Claude Code Security Review](https://github.com/anthropics/claude-code-security-review) | 借鉴阶段审查、可操作问题与增量审查思想；风险触发、证据复用和实验授权门禁为本库独立改写。 |
| V03 算法证据交接与独立复核 | [Repomix](https://github.com/yamadashy/repomix) · [DVC](https://github.com/treeverse/dvc) · [Hypothesis](https://github.com/HypothesisWorks/hypothesis) · [Inspect AI](https://github.com/UKGovernmentBEIS/inspect_ai) · [Promptfoo](https://github.com/promptfoo/promptfoo) | 借鉴上下文精简、数据/实验版本追溯、可执行性质检查与评测记录；跨 AI 科研交接协议为原创融合，未调用外部工具完成独立验证。 |

**来源解读：**“直接参考”表示核对了相近任务的原始文字指令；“方法融合”表示只借鉴结构、证据或格式原则；“跨场景改写”表示针对日本科研助成、长对话归档、Codex 审计或作文比赛独立设计。部分旧链接仍定位到仓库首页，属于参考项目而非逐句来源；后续可在不新增模板的前提下逐步提高引用定位精度。

## 版本记录

- v1.1：清晰化与任务边界整理。
- v1.2：重点优化 S01、R02、P03、G02、M01。
- v1.3：加强授权门禁、科研证据、预算表格与文件归档核查。
- v1.4：精修 P01、G01、L02、X02、X03，压缩重复来源说明。
- v1.6（2026-10-27）：第 8 类新增 V02、V03 跨 AI 独立审查子栏目（参考资料与方法级适配，非模型效果实测）。

**提示**：所有改动都应以真实任务评测质量（事实准确性、必要信息遗漏、可直接使用程度、人工修订量与 Token 开销）；高 Star 或模板变长都不证明效果提升。

## v1.7 补充：计算机算法论文五阶段工作流（2026-10-28）

第八项 [Research Workflow v4.1](08_算法检验与优化/高水平计算机论文工作流/README.md) 主要方法级参考：

- [Microsoft ResearchStudio](https://github.com/microsoft/ResearchStudio)：选题、文献近邻、新颖性碰撞检查。
- [Anthropic Knowledge Work / Scientific Problem Selection](https://github.com/anthropics/knowledge-work-plugins)：研究决策、致命风险与最小反证；原 Skill 的领域实例不直接等同于计算机论文规则。
- [Sakana AI AI-Scientist-v2](https://github.com/SakanaAI/AI-Scientist-v2)：有界实验探索的思想，不照搬全自动系统。
- [obra/superpowers](https://github.com/obra/superpowers)：计划、测试、调试、验证后完成。
- [karpathy/autoresearch](https://github.com/karpathy/autoresearch)：固定评价与 KEEP/DISCARD/INVALID；禁止采用其无限试验循环。
- [Orchestra-Research/AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs)：科研严谨性与论文写作。
- [openai/skills](https://github.com/openai/skills)：Skill 的按需加载与渐进式资源组织。

**说明**：以上均为概念/结构参考，24条 Prompt 与路由 Skill 是本库独立写作；GitHub Star 不等于方法有效。未运行跨模型独立 A/B，也未实测 Token 降幅。旧 V01/V02/V03 与新版本重复的正文已改为兼容链接，可从旧 Git 历史恢复。

## 2026-10-29 独立第09类（v2.1）

[第09类：失败科研项目挽救与转向](09_失败算法项目挽救与转向/README.md) 已从第08类移出。方法级参考 DVC、ARIS、Superpowers、ResearchStudio、Research-Equality、K-Dense、UCL-ERL 和 Karpathy Autoresearch，具体出处见 [完整工作流各步骤](09_失败算法项目挽救与转向/WORKFLOW.md)。新设 Step 05 **三个项目供用户审查**和 Step 06 **必须有事后明确选择**的执行门禁；并无真实模型 A/B 或 Token 效率实测。

## v1.9 工作流可靠性修复参考（2026-10-29）

- [obra/superpowers](https://github.com/obra/superpowers)：任务规划、系统调试和完成前验证；只借鉴有界任务、验证与复核，不复制 Skill 源码。
- [open-gsd/gsd-core](https://github.com/open-gsd/gsd-core)：按阶段/子任务分离上下文、持久状态、失败恢复；不假定用户安装此工具。
- [microsoft/ResearchStudio](https://github.com/microsoft/ResearchStudio)：原始研究意图贯穿选题并记录与用户指定路线的偏差。
- [karpathy/autoresearch](https://github.com/karpathy/autoresearch/blob/master/program.md)：实验隔离、固定评价协议、可追溯结果台账；**没有借用其无限循环规则**，本库仍以人工授权与既定预算硬停止。
- [openai/skills](https://github.com/openai/skills)：按需读取、避免与当前环境重复的冗长上下文。

以上是方法参考，并非声称已经在本仓库运行或完成论文级真实模型测试。

## 2026-10-29 第08项 v5.2 轻量门禁与缺陷分流

新 [TRIAGE.md](08_算法检验与优化/高水平计算机论文工作流/TRIAGE.md) 与 [TRIAGE_POLICY.json](08_算法检验与优化/高水平计算机论文工作流/TRIAGE_POLICY.json) 明确 CRITICAL/REPAIRABLE/MINOR 的受影响行动分流，允许负的Pilot结果经用户选择继续有限探索、暂缺独立审核时先写受限草稿，禁止以降低流程门槛虚构数据/确认性增益或自动获取GPU授权。本次只是流程规则修订，没有真实性能或论文发表成功率增益实测。

## 2026-10-29 第08项 v5.1 按阶段验证与有界修复

[RECOVERY.md](08_算法检验与优化/高水平计算机论文工作流/RECOVERY.md) 与 [REPAIR_ROUTES.json](08_算法检验与优化/高水平计算机论文工作流/REPAIR_ROUTES.json) 为24条科研 Prompt 对应48个验证异常提供诊断、最小修复与回退；按需加载，不是新强制阶段。参考 [Superpowers systematic-debugging](https://github.com/obra/superpowers/blob/main/skills/systematic-debugging/SKILL.md)、[Test Driven Development](https://github.com/obra/superpowers/blob/main/skills/test-driven-development/SKILL.md)、[Karpathy autoresearch](https://github.com/karpathy/autoresearch/blob/master/program.md)、[Cleanlab](https://github.com/cleanlab/cleanlab)、[MLflow](https://github.com/mlflow/mlflow) 及 [Evidently](https://github.com/evidentlyai/evidently) 的故障归因、可复验、数据标签与实验跟踪模式；未运行外部工具也未证实科研模型性能收益。

## 2026-10-29 第08项 v5.0 自动引导层

新增 [START.md](08_算法检验与优化/高水平计算机论文工作流/START.md)、[ORCHESTRATOR.md](08_算法检验与优化/高水平计算机论文工作流/ORCHESTRATOR.md)、[ROUTES.json](08_算法检验与优化/高水平计算机论文工作流/ROUTES.json) 和只读路由加载器。借鉴 [GSD](https://github.com/gsd-build/get-shit-done) 状态恢复、[BMad Method](https://github.com/bmad-code-org/BMAD-METHOD) 菜单引导、[Superpowers](https://github.com/obra/superpowers) 执行门禁、[Microsoft ResearchStudio](https://github.com/microsoft/ResearchStudio) 科研分解机制。并未安装这些框架、没有测量真实 Token 节省或模型效果。

## 2026-10-29 第09类 v2.2 科研提炼 Prompt

在用户确认 P1/P2/P3 后，增加 [Step 05-R](09_失败算法项目挽救与转向/WORKFLOW.md)，基于 [ResearchStudio](https://github.com/microsoft/ResearchStudio) 的研究目标对齐、[Superpowers brainstorming](https://github.com/obra/superpowers/blob/main/skills/brainstorming/SKILL.md) 的问题/方案核查、[Superpowers writing-plans](https://github.com/obra/superpowers/blob/main/skills/writing-plans/SKILL.md) 的可验证计划和 [ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) 的 Claim/Evidence 关联进行原创改写；不调用其 Skill 也不保证发表。

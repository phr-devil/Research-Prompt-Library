# GitHub 参考来源与改写关系

> 核查日期：2026-10-26。Star 数是当日 GitHub 仓库公开数据的快照，**不代表提示词效果排名**。本项目保存的是基于公开文字 Prompt 或 Skill/Agent 工作机制的独立适配稿，不批量复制第三方原文。

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

## 18 条 Prompt 的具体来源与适配性质

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

**来源解读：**“直接参考”表示核对了相近任务的原始文字指令；“方法融合”表示只借鉴结构、证据或格式原则；“跨场景改写”表示针对日本科研助成、长对话归档、Codex 审计或作文比赛独立设计。部分旧链接仍定位到仓库首页，属于参考项目而非逐句来源；后续可在不新增模板的前提下逐步提高引用定位精度。

## 版本记录

- v1.1：清晰化与任务边界整理。
- v1.2：重点优化 S01、R02、P03、G02、M01。
- v1.3：加强授权门禁、科研证据、预算表格与文件归档核查。
- v1.4：精修 P01、G01、L02、X02、X03，压缩重复来源说明。

**提示**：所有改动都应以真实任务评测质量（事实准确性、必要信息遗漏、可直接使用程度、人工修订量与 Token 开销）；高 Star 或模板变长都不证明效果提升。

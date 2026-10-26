# GitHub 来源、热度与改编关系（v1.3）

> 原始热度快照整理于 2026-10-21；2026-10-26 核查了下列主要文本来源。表中的 Stars 仍为旧快照、不是实时数字，更不是提示词质量的实证评分。热度只用于筛选，不作为提示词实际效果的证据。下面列的仓库中，仅引用公开的**文字 Prompt**。

| 仓库 | Stars（约） | 用到的文字内容 | 原始链接 |
|---|---:|---|---|
| prompts.chat | 约 173.7k | 通用角色与写作 Prompt | [打开](https://github.com/f/prompts.chat/blob/main/PROMPTS.md) |
| PlexPt/awesome-chatgpt-prompts-zh | 约 63.8k | 中文角色、写作与翻译 | [打开](https://github.com/PlexPt/awesome-chatgpt-prompts-zh) |
| danielmiessler/fabric | 约 44.4k | summarize / analyze_paper / improve_writing / create_academic_paper / create_formal_email | [打开](https://github.com/danielmiessler/fabric/blob/main/data/patterns/summarize/system.md) |
| Leey21/awesome-ai-research-writing | 约 35.1k | 论文翻译、语言润色、逻辑检查、去 AI 味 | [打开](https://github.com/Leey21/awesome-ai-research-writing#part-i-%E5%86%99%E4%BD%9C-prompt-%E9%9B%86%E5%90%88) |
| ahmetbersoz/chatgpt-prompts-for-academic-writing | 约 5.0k | 文献缺口、研究计划、论文章节 | [打开](https://github.com/ahmetbersoz/chatgpt-prompts-for-academic-writing) |
| langgptai/wonderful-prompts | 约 6.4k | 中文信息检索提示词 | [打开](https://github.com/langgptai/wonderful-prompts) |
| bohyy/academic-ai-prompt | 约 1.1k | 选题、文献查找、论文写作 | [打开](https://github.com/bohyy/academic-ai-prompt) |
| langgptai/awesome-deep-research-prompts | 约 0.13k | 调研目标和研究计划 | [打开](https://github.com/langgptai/awesome-deep-research-prompts) |
| haidrrrry/humanize-ai-writing | 不作为高星来源 | 自然化写作规则 | [打开](https://github.com/haidrrrry/humanize-ai-writing/blob/main/PROMPT.md) |

## 映射与证据等级说明

- **直接对应**：现成的提示词原文确实涵盖该场景（如 `P03` 学术润色、`L01` 中英论文翻译）。本库仍重写正文，以便术语与输入输出标准一致。
- **方法融合**：原仓库提供摘要、文献分析或结构化写作方法，本库增加科研实验、项目历史和证据要求（如 `M01`）。
- **跨场景适配**：找不到成熟高 Star 的日本科研基金、日语作文比赛或 Codex 实验审计 Prompt，基于相邻文字 Prompt 设计的原创模板，不宣称“GitHub 原文”。

来源较高星也可能出现缺乏证据约束、过长、夸大效果的指令；本库有意加入事实核查、停止准则、精确原文替换及版本管理。

## 版权与署名

这里只提供原始 GitHub URL 和自行撰写的适配版；没有批量全文复制第三方仓库。如果后续要公开发布、镜像原始提示词或上传到新的 GitHub 仓库，请逐项查看各项目许可证和署名要求。

## 本次修订说明

v1.1 仅润色现有 Prompt 的任务定义、输出要求和证据边界，没有新增来源或复刻第三方全文。各文件的 GitHub 链接表示参考过的**公开文字 Prompt 或组织方法**，不代表对方仓库具有完全相同的任务模板。

## v1.2 具体来源与改写关系

v1.2 只对现有 S01、R02、P03、G02、M01 做重点修改。阅读了 GitHub 仓库中的原始文字 Prompt，重点提取输出结构、领域审核和事实约束；本库的中文正文独立改写，并不复制原文或沿用其未经验证的效果宣传。

### S01

- [Wonderful Prompts / AI 搜索提示词（RAG 证据对应与缺失声明）](https://github.com/langgptai/wonderful-prompts#ai-搜索提示词)
- [Academic Writing Prompts / Literature Review（核查参考文献存在）](https://github.com/ahmetbersoz/chatgpt-prompts-for-academic-writing#literature-review)

改写方式：借鉴基于来源回答、缺少证据就说明的写法；任务模式、跨国资格审查及去重流程为本库适配内容。

### R02

- [Fabric / analyze_paper（研究设计、样本量、置信区间、复现性审查）](https://github.com/danielmiessler/fabric/blob/main/data/patterns/analyze_paper/system.md)
- [Academic Writing Prompts / Methodology 与 Experiments](https://github.com/ahmetbersoz/chatgpt-prompts-for-academic-writing#methodology)
- [Awesome AI Research Writing / 实验分析（负结果不强行写成提升）](https://github.com/Leey21/awesome-ai-research-writing#实验分析)

改写方式：借鉴论文严谨性审核、实验方案与负结果实述方法；GO/HOLD/STOP、失败归因和重构门槛为本库原创整合。

### P03

- [Awesome AI Research Writing / 表达润色（英文论文）](https://github.com/Leey21/awesome-ai-research-writing#表达润色英文论文)
- [Awesome AI Research Writing / 逻辑检查](https://github.com/Leey21/awesome-ai-research-writing#逻辑检查)
- [Awesome AI Research Writing / Reviewer 视角审视](https://github.com/Leey21/awesome-ai-research-writing#论文整体以-reviewer-视角进行审视)
- [Fabric / improve_writing（保持原意，直接输出精炼文字）](https://github.com/danielmiessler/fabric/blob/main/data/patterns/improve_writing/system.md)

改写方式：借鉴原仓库对润色、逻辑审查、审稿分别设定任务和输出的组织方式；三个模式合并为一个可复制模板。

### G02

- [Academic Writing Prompts / PLAN/PRESENTATION（研究计划与进度）](https://github.com/ahmetbersoz/chatgpt-prompts-for-academic-writing#planpresentation)
- [Academic Writing Prompts / Methodology（目标、方法与局限）](https://github.com/ahmetbersoz/chatgpt-prompts-for-academic-writing#methodology)
- [Fabric / create_academic_paper（仅借鉴清晰学术组织，不沿用论文排版）](https://github.com/danielmiessler/fabric/blob/main/data/patterns/create_academic_paper/system.md)

改写方式：没有核实到高星日本研究助成的逐栏专用 Prompt。本文件借鉴通用研究计划、方法写作的文字指令，再独立加入表格、官方资格、预算和日语约束。

### M01

- [Fabric / summarize（核心摘要与要点分层）](https://github.com/danielmiessler/fabric/blob/main/data/patterns/summarize/system.md)
- [Fabric / analyze_paper（事实、研究设计与证据对应）](https://github.com/danielmiessler/fabric/blob/main/data/patterns/analyze_paper/system.md)

改写方式：借鉴 Markdown 摘要与证据质量整理的输出结构；双层科研接力、状态与来源、失败路线归档为本库自主设计。


## v1.3：实际借鉴的具体原文及改写边界（2026-10-26）

这里列出公开的文字 Prompt，**不是将开源文案复制进本库**。原始 GitHub 的部分写法较冗长、要求固定输出或含有未经验证的质量承诺；本库只抽取可验证、有助于科研执行的部分。未单独列出的模板沿用其原有来源说明。

| 本库模板 | 核对的具体来源 | 采纳的设计原则 | 本库独立补充 |
|---|---|---|---|
| S01、S02 | [Wonderful Prompts / AI 搜索提示词](https://github.com/langgptai/wonderful-prompts#ai-搜索提示词) | 回答对应可访问的来源，缺乏上下文时说明不足 | 多语言检索、官方年度版本、资格和搜索覆盖边界 |
| R01、P02 | [Academic Writing / Literature Review](https://github.com/ahmetbersoz/chatgpt-prompts-for-academic-writing#literature-review) | 文献存在性必须交叉核查；研究问题和引用相互对应 | 全文/摘要/二手证据等级、禁止推断未阅读的方法 |
| R02 | [Fabric / analyze_paper](https://github.com/danielmiessler/fabric/blob/main/data/patterns/analyze_paper/system.md)；[Academic Writing / Methodology](https://github.com/ahmetbersoz/chatgpt-prompts-for-academic-writing#methodology) | 研究设计、样本、置信区间和复现性评估 | 正式门槛必须有人类批准、GO/HOLD/STOP、GPU 门禁 |
| P03 | [Awesome AI Research Writing / 逻辑检查](https://github.com/Leey21/awesome-ai-research-writing#逻辑检查)；[Reviewer 视角](https://github.com/Leey21/awesome-ai-research-writing#论文整体以-reviewer-视角进行审视) | 润色与科学审核分开，严重问题应有可定位依据 | 避免没有全文时假装已完成审稿 |
| G02、G03 | [Academic Writing / Plan](https://github.com/ahmetbersoz/chatgpt-prompts-for-academic-writing#planpresentation)；[Fabric / improve_writing](https://github.com/danielmiessler/fabric/blob/main/data/patterns/improve_writing/system.md) | 目标、时间计划、清晰日语文字及修订内容输出 | 日本财团表格、预算计算、字符计数、行政合规分级（**无专用高星原文**） |
| M01 | [Fabric / summarize](https://github.com/danielmiessler/fabric/blob/main/data/patterns/summarize/system.md) | 快速摘要与分层信息呈现 | 完整实验记录、证据/版本/授权分离、真实 .md 交付 |
| X01、M02 | [Fabric / improve_prompt](https://github.com/danielmiessler/fabric/blob/main/data/patterns/improve_prompt/system.md)；[Fabric / analyze_paper](https://github.com/danielmiessler/fabric/blob/main/data/patterns/analyze_paper/system.md) | 明确输入、步骤、输出、可测验证条件 | Codex 执行权限、实验日志审计、多文件版本锁定（**并非现成 Codex Prompt**） |

**证据等级**：直接看到相同任务的公开文字 Prompt，可称“直接参考”；只借鉴分析或写作步骤，标“方法借鉴”；日本基金、科研接力与 Codex 审计中的专业流程主要为本库的跨场景改写。所有 GitHub Star 仅供筛选，不能代替用户真实任务上的测试。

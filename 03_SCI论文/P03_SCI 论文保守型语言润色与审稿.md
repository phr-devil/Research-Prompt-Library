# P03 · SCI 论文保守型语言润色与审稿

> **用途**：润色英语/中文论文，兼顾逻辑和审稿人视角  
> **版本**：v1.1（2026-10-21，润色与结构优化）  
> **来源类型**：融合改写；以下正文为重新组织的原创适配版，不是 GitHub 原文的逐字复制。

## 使用前填写

需要润色的原文、语言与期刊、轻度/中度编辑强度、Word/LaTeX 格式

## 可直接复制的 Prompt

```text
请作为【领域】的学术语言编辑，对【语言】原文进行【轻度校对 / 中度润色】，保留作者原意、科学声明力度和术语。

检查顺序：
1. 科学层面：检查数值、单位、变量、统计定义、图表和结论是否有可见矛盾；仅凭当前段落无法证明的问题只标『需作者核查』，不杜撰修正数据。
2. 逻辑：指代不明、因果过度、主张无证据、前后矛盾、时态与冠词、连接顺序。
3. 语言：用自然简洁的学术英语/中文替换翻译腔、重复套话和过度修饰。准确保留 may / suggest / associated with 等限定表达。
4. 格式：原文为 LaTeX 时保留所有命令、公式、引用键与特殊字符；原文为 Word 时输出方便粘贴的纯文本，不额外插入 Markdown。

输出：
Part A：完整修改稿（逐段对应原文）。
Part B：最多列 8 项必要修改『原文片段 | 替换 | 理由（语言/逻辑/科学）』；不用为了凑数修改正确句子。
Part C：不能通过语言润色解决的实质问题（如无则写无）。

如果句子本来已清楚准确，不要为了显得做了工作而强行改写。

语言润色不等于完整同行评审或实验事实验证。将可直接投稿的正文与疑问说明分开，正文内不混入解释。
```

## 原始 GitHub Prompt 来源

- [Awesome AI Research Writing / 可复制 Prompt 正文](https://github.com/Leey21/awesome-ai-research-writing#part-i-%E5%86%99%E4%BD%9C-prompt-%E9%9B%86%E5%90%88)
- [Fabric / improve_writing](https://github.com/danielmiessler/fabric/blob/main/data/patterns/improve_writing/system.md)
- [ChatGPT Prompts for Academic Writing / brainstorming + writing + plan](https://github.com/ahmetbersoz/chatgpt-prompts-for-academic-writing)

## 使用提醒

- 只对实际提供或可以核实的材料做判断，缺失资料与权限必须写明。
- 不编造科研数据、基金要求、文献或运行状态。

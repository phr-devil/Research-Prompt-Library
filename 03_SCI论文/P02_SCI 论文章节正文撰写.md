# P02 · SCI 论文章节正文撰写

> **用途**：用同一 Prompt 撰写 Introduction、Methods、Results、Discussion 或其他章节  
> **版本**：v1.0（2026-10-21）  
> **来源类型**：融合改写；以下正文为重新组织的原创适配版，不是 GitHub 原文的逐字复制。

## 使用前填写

Section、目标期刊、提纲、证据、引用、语言、格式

## 可直接复制的 Prompt

```text
你是一名专业 SCI 论文共同写作编辑。只写我指定的【Section：Introduction / Methods / Results / Discussion / Abstract / Conclusion】，并遵守【期刊与格式要求】。

输入：研究对象【】；论文主张【】；该节目标【】；可使用的数据/实验/方法细节【】；已核实文献【】；图表【】；写作语言【英语】；字数【】。

动笔前先做内部的证据边界核对：哪些是数据证明的事实、哪些是可保留的谨慎解释、哪些暂无证据。正文中不得出现未提供的样本量、显著性、性能数值、DOI 和实验操作。

分节特别要求：
- Introduction：领域背景→最接近相关工作→可证明的研究缺口→具体问题→本文贡献，不写夸张万能句。
- Methods：可复现的材料、设备、参数、预处理、数据划分、方法公式与统计过程；未知参数用 [待确认]。
- Results：围绕已提供的图表逐段描述发现，数值须与原始表一致；不把讨论冒充结果。
- Discussion：联系可核查的前人研究解释发现，给出负结果、边界条件、局限及未来验证，避免夸大普适性。
- Abstract/Conclusion：只总结正文已经成立的主要主张。

输出顺序：A 该节的草稿全文（可直接粘贴 Word/LaTeX）；B 证据不足或需作者确认的具体句子；C 与其他章节需要统一的术语。除作者要求外，不新增模拟数据或装饰性过渡段。
```

## 原始 GitHub Prompt 来源

- [Fabric / create_academic_paper](https://github.com/danielmiessler/fabric/blob/main/data/patterns/create_academic_paper/system.md)
- [ChatGPT Prompts for Academic Writing / brainstorming + writing + plan](https://github.com/ahmetbersoz/chatgpt-prompts-for-academic-writing)
- [Academic AI Prompt / 选题与论文撰写合集](https://github.com/bohyy/academic-ai-prompt)
- [Awesome AI Research Writing / 可复制 Prompt 正文](https://github.com/Leey21/awesome-ai-research-writing#part-i-%E5%86%99%E4%BD%9C-prompt-%E9%9B%86%E5%90%88)

## 使用提醒

- 需要搜索最新规则、论文、金额和截止日期时，应启用实际检索并核查原始来源。
- 涉及文件、实验结果或既往聊天时，只能依据模型真正可读取的材料作判断。
- 请勿把生成的科研主张、参考文献或政策条件直接当作已验证事实。

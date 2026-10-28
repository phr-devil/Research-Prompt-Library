---
name: research-paper-workflow
description: Route high-level computer-science algorithm research through five evidence-gated stages; select only one relevant stage/scenario prompt to minimize repeated context.
---

# Research Paper Workflow — v4.1 router

本 Skill 是路由器，不是授权许可；仅当你的 Codex/Agent **实际安装并识别**时才能原生调用，ChatGPT 可在线阅读以下 Markdown 参考。

1. 首先依据可信 STATE/实验结果判定当前五阶段中的哪一阶段；已有可信证据时直接从相应阶段开始，不强制从①重来。
2. 先读 [共享科研规则](00_统一规则与Skill映射.md)，然后**只加载当前阶段**之一：[①选题](01_科学选题与跨AI审核.md)、[②最小验证](02_最小科学验证与决策.md)、[③算法研发](03_完整算法研发与正式实验.md)、[④独立审查](04_独立科学验证.md)、[⑤论文](05_论文撰写与投稿.md)。
3. 阶段内只执行满足触发条件的一项或一组相关 Prompt；不得机械遍历所有24条。
4. 依据原始证据区分科学假设、工程 PASS 和论文确认性结论。保持测试集隔离、独立统计单位与公平强基线；未授权 GPU/收费/外传/冻结改动不可自动执行。
5. 一次完成有独立验收意义的关联任务，允许在既定授权内自主修复；出现影响核心科学主张的反例或预算边界时停止对应工作，保留负结果。
6. 默认7行以内差量汇报，并给出原始证据路径；不要把独立审查报告和开发者自查混淆。

**参考方法**：ResearchStudio、Scientific Problem Selection、Superpowers、Karpathy Autoresearch、ARA Rigor Reviewer。参考其公开工作流不等于这些第三方 Skill 已安装，且不得继承无限实验循环。

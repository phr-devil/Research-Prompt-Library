---
name: research-paper-workflow
description: Route high-level computer-science algorithm research through five evidence-gated stages; automatically load the next eligible scientific prompt after human choices while respecting evidence and authorization gates.
---

# Research Paper Workflow — v5.3 severity-guided router (v4.1 core)

本 Skill 是路由器，不是授权许可；仅当你的 Codex/Agent **实际安装并识别**时才能原生调用，ChatGPT 可在线阅读以下 Markdown 参考。

0. 首次收到用户科研目标 + 提示词库 URL 时，先读 [START.md](START.md)、[ORCHESTRATOR.md](ORCHESTRATOR.md)、[ROUTES.json](ROUTES.json)；后续真实用户选择直接恢复 STATE 并读取下一场景 Prompt。未安装的 Skill 不会在任意平台自动触发。Skill 未实际安装/识别时，只可阅读 Markdown 并用可用工具执行；不得宣称已调用第三方 Skill。一个场景 Prompt 独立复制时仍遵守授权、证据与止损底线。
1. 按 [TRIAGE.md](TRIAGE.md) / [TRIAGE_POLICY.json](TRIAGE_POLICY.json) 将缺陷依受影响目标分级：CRITICAL 阻断受影响动作，REPAIRABLE 用户选择继续/修复/调整，MINOR 自动记账跳过；无需24步骤全部全绿。不得以放宽为由跳过真实证据或GPU独立授权。
2. 首先依据可信 STATE/实验结果判定当前五阶段中的哪一阶段；已有可信证据时直接从相应阶段开始，不强制从①重来。
3. 先读 [共享科研规则](00_统一规则与Skill映射.md)，然后**只加载当前阶段**之一：[①选题](01_科学选题与跨AI审核.md)、[②最小验证](02_最小科学验证与决策.md)、[③算法研发](03_完整算法研发与正式实验.md)、[④独立审查](04_独立科学验证.md)、[⑤论文](05_论文撰写与投稿.md)。
4. 遵守 ROUTES.json 的 required/conditional 触发；阶段内只执行满足触发条件的一项或一组相关 Prompt；不得机械遍历所有24条。
5. 当前 route 发生验证失败时，只加载 [RECOVERY.md](RECOVERY.md) 和 [REPAIR_ROUTES.json](REPAIR_ROUTES.json) 中对应条目。先复现/归因，单一假设→最小修复→针对性复验；工程连续3次修复仍失败或科学两轮诊断无新证据则停下来请用户选择，已有更严格预算优先。真值缺失或正式test污染不得靠调参解决。
6. 依据原始证据区分科学假设、工程 PASS 和论文确认性结论。保持测试集隔离、独立统计单位与公平强基线；未授权 GPU/收费/外传/冻结改动不可自动执行。
7. 一次完成有独立验收意义的关联任务，允许在既定授权内自主修复；出现影响核心科学主张的反例或预算边界时停止对应工作，保留负结果。
8. 已有可信 NO-GO/STOP 时可跳到 [独立第09类](../../09_失败算法项目挽救与转向/README.md)；Step 05 需给用户三个候选后停止，未收到后续消息明确选中 P1/P2/P3 禁止启动 Step 06。项目选择不是实验授权。
9. 关键门禁只给短菜单（通常 A/B/C），等待用户**下一条真实消息**，回复后自动加载下一 Prompt，无须重新输入总控。普通已获授权任务自行推进。
10. 默认7行以内差量汇报，并给出原始证据路径；不要把独立审查报告和开发者自查混淆。

**参考方法**：ResearchStudio、Scientific Problem Selection、Superpowers、Karpathy Autoresearch、ARA Rigor Reviewer。参考其公开工作流不等于这些第三方 Skill 已安装，且不得继承无限实验循环。

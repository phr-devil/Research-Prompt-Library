---
name: research-paper-workflow
description: Prototype-first algorithm research agent: minimum viable baseline and model, evidence-led iteration, on-demand scientific review and failure recovery.
---

# Research Workflow v6.1｜按需路由

**只加载 [ORCHESTRATOR.md](ORCHESTRATOR.md) 与本次项目现有证据开始。** 有明确科研目标就直接在授权范围内设计最小基线/实现可运行原型；不把24场景当作预先全过的审批链，不强制安装额外Skill或打开多Agent。

- 第一类科学选题（01-A～D）优先在 ChatGPT 完成；真实本地执行才转 WorkBuddy/Codex，独立审查仅在关键风险时另行触发。
- 正常：最低必要数据核查 → 原型 + 简单对照 → 修改/实验/记录 → 下一个有信息量的行动。
- 意外、无增益、假增益：按现象选一条 [LESSONS.md](LESSONS.md) 与 [RECOVERY.md](RECOVERY.md)，需要具体场景时查看 [ROUTES.json](ROUTES.json) 或 `workflow_route.py --id 03-E`。
- 核心主张有变化/正式确认：才读近邻研究、正式实验、独立审核及论文相关旧Prompt；不重复无关审查。
- 严格保留独立真值、泄漏防范、公平强基线、原始Run证据；区分程序PASS与科学贡献。GPU/费用/数据外传/冻结正式实验/投稿需要真实用户单独授权；不无限自主训练。
- Step05第09类必须让用户从P1/P2/P3中明确选择，不可自动替选。失败有效结果保留，非法/无效结论不得继续宣称。
- 少写日志，仅给真实成果与必要分叉选择。Skill未安装只按可访问的Markdown执行，不声称原生调用。

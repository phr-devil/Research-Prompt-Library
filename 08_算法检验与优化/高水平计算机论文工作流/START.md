# 第08章｜AI 直接读取 GitHub 的入口

**先确定用户当前意图；一个任务只读一个入口，不要默认读取其余24条 Prompt。** 统一规则见 [ORCHESTRATOR.md](ORCHESTRATOR.md)，全站关键词导航见仓库根目录 [AGENTS.md](../../AGENTS.md)。

- **用户要求找新课题/可行性/公开数据**：读 [IDEA_FUNNEL.md](IDEA_FUNNEL.md)，ChatGPT完成F1–F4，可行性优先（合法数据、基线、可验证价值）；F5真实用户选择，不训练。
- **续做已选课题/有Run**：读 [POST_SELECTION.md](POST_SELECTION.md)，优先复用可信基线→可学性/剩余问题→低风险优化或必要新机制；按问题加载一份手册。
- **Bug/训练失败**：读 [RECOVERY.md](RECOVERY.md)，在授权内自主修复、定向验证并续做。
- **科学负结果/止损**：读 [RESEARCH_DECISIONS.md](RESEARCH_DECISIONS.md)，仅停止缺乏价值的受影响分支，不自动判项目失败。

**硬边界**：EXPLORE允许合理理论机会及UNKNOWN；工程PASS/基线跑通不是论文贡献，正式确认须可靠证据。CPU拟合、tiny-set和GPU训练都属训练；禁止训练时均不执行。GPU、费用、外传、正式确认、投稿及重大改题须真实授权；第09章P1/P2/P3须真实新消息。工具不可访问时标UNVERIFIED。

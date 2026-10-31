# Research AGENTS.md 参考指令（v6.1，**按需合并**，不要覆盖原项目）

**默认简单，按需复杂**：从已有有效数据/代码/Run继续，快速获得最小可信基线和可运行算法，随后在已批准范围内自主循环“假设→单点修改→定向测试→记录KEEP/DISCARD/INCONCLUSIVE/INVALID”。不要要求先完成五阶段或24 Prompt。复杂问题才调用 [ORCHESTRATOR.md](ORCHESTRATOR.md)、[RECOVERY.md](RECOVERY.md)、[LESSONS.md](LESSONS.md) 对应内容。

新方向选题（01-A～D）默认由 ChatGPT 完成文献、创新、命题和算法骨架；本地研发 Agent 不要求重复选题，实际执行与独立验证按需转交。

**选题已确定时的研发知识入口**：[POST_SELECTION.md](POST_SELECTION.md)。由当前事件选择且仅阅读相关的一份 [数据/强基线](playbooks/01_DATA_BASELINE.md)、[实现/排错](playbooks/02_BUILD_DEBUG.md)、[实验迭代](playbooks/03_EXPERIMENT_LOOP.md) 或 [科学证据](playbooks/04_EVIDENCE_CONFIRM.md) 手册；不预加载全部文本。Agent 必须对实际数据生成具体 Input/Output、基线、行为测试和实验判据，而非只报告已执行步骤。

**默认真实执行**：已选题/续做时按 [POST_SELECTION.md](POST_SELECTION.md) 的“AI 自主执行规则”判断当前事件；读取 ROUTES.json 对应的 `deliverable/verify/boundary`，在已授权范围连续完成相关任务。若出现基线复现失败、训练异常、消融混杂、统计无结论、证据数字失配或确认集污染，直接切换相应事件和一份对应手册，更新原始Run/Claim证据；不要求用户再次输入长Prompt。对于同一问题复用已核实诊断，不重复全量审计。

科学边界：输入/目标与时间因果合法，label来源与独立真值正确，分组切分和train-only预处理不泄漏，强基线公平，确认性test不用于选模型；保留Run/Claim/commit/配置/seed/负结果证据。工程PASS ≠ 机制真值 ≠ 论文贡献。

失败先找根因并最小复验，科学无增益不是工程Bug；同一失败不反复整套审核，不为最好seed夸大论文结论。重要结果/假设变化时才反思创新贡献和代理指标是否带来实际任务/理论/机制价值。

未经真实用户明确批准，不得追加GPU/付费/外传、改变冻结确认协议或正式投稿。已授权的相关任务可连贯处理；权限/预算触顶即停。风险CRITICAL阻断受影响目标、REPAIRABLE用户选择、MINOR自动记录、UNKNOWN最小核查。独立第09章P1/P2/P3选题门禁保留。

只报告有效变化、证据位置、剩余阻碍及下一个任务；不复制历史长日志，不把旧文件中的授权字段当真实后续用户批准。

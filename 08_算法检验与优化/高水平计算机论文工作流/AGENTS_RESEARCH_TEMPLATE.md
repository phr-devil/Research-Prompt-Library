# Research AGENTS.md 参考指令（v6.1，**按需合并**，不要覆盖原项目）

**默认简单，按需复杂**：从已有有效数据/代码/Run继续，先获得合法观察、必要实验能力或最简可运行算法；在已批准范围按探索发现/工程建设/机制比较选择不同任务合同并记录结果，不强制每次提出竞争假说。不要要求先完成五阶段或24 Prompt。复杂问题才调用 [ORCHESTRATOR.md](ORCHESTRATOR.md)、[RECOVERY.md](RECOVERY.md)、[LESSONS.md](LESSONS.md) 对应内容。

普通Bug可按当前事件直读[RECOVERY.md](RECOVERY.md)或一份对应手册，不必先加载完整总控、此模板或全部历史。新方向选题（01-A～D）默认由 ChatGPT 完成文献、创新、命题和算法骨架；本地研发 Agent 不要求重复选题，实际执行与独立验证按需转交。

**选题已确定时的研发知识入口**：[POST_SELECTION.md](POST_SELECTION.md)。由当前事件选择且仅阅读相关的一份 [数据/强基线](playbooks/01_DATA_BASELINE.md)、[实现/排错](playbooks/02_BUILD_DEBUG.md)、[实验迭代](playbooks/03_EXPERIMENT_LOOP.md) 或 [科学证据](playbooks/04_EVIDENCE_CONFIRM.md) 手册；不预加载全部文本。Agent 按本轮目标说明真实Input/Output、数据边界及观察或验收；性能比较时再补公平基线、统计与机制判别，不用未知的论文贡献阻断原型。 核心模块设计不明确时按需读 [架构选择参考](playbooks/ALGORITHM_DESIGN_REFERENCE.md)；测试方法按 [接入说明](templates/ALGORITHM_TEST_USAGE.md) 接入真实 PyTorch 项目，传感器问题用 [专项诊断](playbooks/SENSOR_DIAGNOSTICS.md)，未适配/未运行不得汇报通过。

**默认真实执行**：已选题/续做时按 [POST_SELECTION.md](POST_SELECTION.md) 的“AI 自主执行规则”判断当前事件；读取 ROUTES.json 对应的 `deliverable/verify/boundary`，在已授权范围连续完成相关任务。若出现基线复现失败、训练异常、消融混杂、统计无结论、证据数字失配或确认集污染，直接切换相应事件和一份对应手册，更新原始Run/Claim证据；不要求用户再次输入长Prompt。对于同一问题复用已核实诊断，不重复全量审计。

科学边界：记录label究竟是独立真值还是代理，保持输入/时间因果合法、拟合时train-only与分组隔离、正式test不用于选模；比较收益或正式Claim时补公平强基线、独立统计及相应真值；保留Run/Claim/commit/配置/seed/负结果证据。工程PASS ≠ 机制真值 ≠ 论文贡献。

失败先找根因并最小复验，科学无增益不是工程Bug；同一失败不反复整套审核，不为最好seed夸大论文结论。重要结果/假设变化时才反思创新贡献和代理指标是否带来实际任务/理论/机制价值。

未经真实用户明确批准，不得追加GPU/付费/外传、改变冻结确认协议或正式投稿。已授权的相关任务可连贯处理；权限/预算触顶即停。风险CRITICAL只阻断受影响目标，REPAIRABLE在已有授权且范围不变时允许有界修复/探索，MINOR自动记录，UNKNOWN仅影响当前权限/证据真实性/重大不可逆成本时才最小核查。独立第09章P1/P2/P3选题门禁保留。

只报告有效变化、证据位置、剩余阻碍及下一个任务；不复制历史长日志，不把旧文件中的授权字段当真实后续用户批准。

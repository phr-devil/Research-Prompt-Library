# AGENTS.md — PD-RW 独立科研工作流入口

本仓库独立运行，不依赖旧 Research-Prompt-Library 的章节路由。仅在用户明确要求研究/执行时使用本仓库规则，不把建议理解为下载、CPU/GPU 训练、付费、确认集解封、外传或投稿授权。

## 最短读取路径

1. 首次使用先读 [START.md](START.md) 与 [WORKFLOW.md](WORKFLOW.md)；已有任务优先读取真实 STATE、数据 manifest、最新有效 Run。
2. 仅按当前阻碍读取一份专题：研究机会/数据选取→SEARCH_DISCOVERY 或 DATA_DISCOVERY；数据现象→DATA_INSIGHT；任务价值→TASK_EXPLORATION（需要才读 TASK_LADDER）；算法/故障→EXPERIMENT_LOOP 或 IMPLEMENTATION_GUIDE；论文贡献→PAPER_FIRST；最终确认→CONFIRMATION。
3. 每轮在已授权范围连续完成相关工作，复用证据、不重复全库检索、不预先生成漂亮图表和大报告；只输出关键新证据、实际运行/未运行、决定和下一步。
4. 保持 group/时间隔离与 train-only 预处理；封存 test 不用于选题和调参，科学性未确认不得宣传可发表。单次负 pilot 不意味着项目失败；越权、泄漏、伪真值则停止受影响动作。
5. [SCENARIOS.json](SCENARIOS.json) 和 tests 只是合成结构自检，不证明科研成功率。实际执行性能需要真实盲回放与前瞻性验证。

不要求安装第三方 Agent；AIDE / AutoResearch 等属于可选执行后端，集成前单独验证权限与评价隔离。

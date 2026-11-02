# 第十章｜开源工作流对照与可迁移机制（2026-11-02 复核）

> 只引用公开官方仓库或官方文档；**Stars 不是科研效能、真实性或投稿成功率**，故不再维护易过期的星数排名。以下仅借鉴任务组织与实验可追踪性，不代表已安装这些框架，也不复制第三方提示词或代码。

| 开源项目与官方来源 | 值得借鉴 | 在第十章中的落地 | 不照搬的部分 |
|---|---|---|---|
| [Microsoft RD-Agent](https://github.com/microsoft/RD-Agent) | 科学问题/实现/实测反馈之间持续循环 | 问题—数据→TASK→最小实验→反馈修订 | 不为每个课题引入多个 Agent、服务或冗长日志 |
| [Karpathy autoresearch](https://github.com/karpathy/autoresearch) · [program.md](https://github.com/karpathy/autoresearch/blob/master/program.md) | 固定评价基础设施、短反馈、可回退代码、逐次记录 | 保护 evaluator、`BEST_VALID_RUN`、原始负结果与版本 | `LOOP FOREVER`、仅按单一开发分数保留，均不适用于论文确认 |
| [AIDE (WecoAI/aideml)](https://github.com/WecoAI/aideml) | 代码试验树、调试、分支血缘 | 一个主分支＋有不同解释的少量备选；记录 parent_run | 代码竞赛得分与科研创新不能划等号 |
| [AI-Scientist-v2](https://github.com/SakanaAI/AI-Scientist-v2) | 假设—实验—反馈的开放探索与实验管理 | 有界的候选任务/机制探索 | 官方承认：有强起始模板时开放 v2 不一定优于 v1；多分支不保证成功 |
| [AI-Scientist-v3](https://github.com/SakanaAI/AI-Scientist-v3) | 研究调查、消融、独立末次评估分离 | 多任务搜索与最终封存确认严格分离 | 不自动生成或声称一篇论文已通过科学验证 |
| [MLflow](https://github.com/mlflow/mlflow) | Run 参数、指标、产物与血缘 | 复用现有 STATE/RUNS/CLAIMS 指针和可恢复比较 | 不强制部署追踪服务器 |
| [Optuna](https://github.com/optuna/optuna) | 有界 Trial、记录搜索史和低成本剪枝 | 按新信息/总成本选择试验，保留被淘汰分支 | 低保真剪枝不是机制科学证伪；不在 test 上调参 |
| [Cleanlab](https://github.com/cleanlab/cleanlab) | 标签质量、数据问题定位 | 开放观察时审查标签/数据真实性 | 模型标记的可疑标签不等于真实标注错误 |
| [DVC](https://github.com/treeverse/dvc) | 原始数据和实验版本可追溯 | manifest、data_version、split/protocol_id、增量复跑 | 不强制安装 DVC 或重复存储大型数据 |

## 这次审查形成的四个具体改动

1. **固定比较条件，保留完整搜索史**（autoresearch / MLflow / DVC）：不因回退代码删除失败 Run；协议变化只重评受影响部分。
2. **任务、方法与验证一一对应**（RD-Agent / AI-Scientist-v3）：预留 holdout 只代表隔离，不保证适用于后来发现的每个新任务；必须核真值、组别、因果和独立性。
3. **信息价值驱动而非 GPU 占用驱动**（AIDE / Optuna）：一主分支、按症状选择最廉价判别，升级训练预算以能改变决定为条件，不机械强制双规模/正控。
4. **开放探索不等于任意论文故事**（AI-Scientist-v2/v3）：在关键投入前按需复核直接近邻，独立报告简单强基线、弱效果、失败组及任务搜索偏差。

**适配边界**：这些项目大多追求 ML 工程或单指标优化，第十章追求的则是**可复核的独立科研价值/总资源成本**。以上为设计依据而非工作流效果的实证；只有同条件历史盲回放与前瞻性测试才能判断改版是否真的有帮助。论文/项目作者与许可条款需按实际用途核实。

# 第十章｜公开高星 GitHub 工作流参考与迁移边界

> **来源核验时间：2026-11-02**。Stars 为约数、随时间变化；热门≠科学成功率/论文质量。只借鉴可核的方法，不复制第三方项目提示词、源代码或许可证限制不明的内容，也不宣称这些框架已安装在用户电脑上。

| 官方 GitHub 项目 | Stars 约数 | 仓库/文档中的机制 | 第十章对应设计 | 不能照搬的部分 |
|---|---:|---|---|---|
| [karpathy/autoresearch](https://github.com/karpathy/autoresearch) · [program.md](https://github.com/karpathy/autoresearch/blob/master/program.md) | 99k | 固定 prepare/evaluator、实验脚本、结果记录、保留增益并回退 | 稳定评价器、短反馈、BEST_VALID_RUN 与原始负结果 | 原文 LOOP FOREVER、只追求一个验证指标；科研要预算、停止和多任务选择纠偏 |
| [mlflow/mlflow](https://github.com/mlflow/mlflow) | 28.6k | 跟踪 experiment/run、parameters、metrics 和模型产物 | 简明 Run 证据索引、可复现 provenance | 不要求服务部署或新平台栈 |
| [microsoft/RD-Agent](https://github.com/microsoft/RD-Agent) | 15.2k | Research ideas (R) 与 implementation (D) 在真实反馈中进化，覆盖数据/模型研发 | 数据发现→科研任务生成→代码实验→反馈回流 | 不为普通项目引入复杂多 Agent 架构 |
| [optuna/optuna](https://github.com/optuna/optuna) | 15k | Trial 管理、搜索空间、剪枝与预算优化 | 有界调参、记录全部 trial、选择信息价值实验 | 不把过早 pruning 当科学机制被证伪，也不在封存test优化 |
| [SakanaAI/AI-Scientist](https://github.com/SakanaAI/AI-Scientist) | 14.9k | idea→experiment→review/write-up 的研究闭环 | 记录从假设到结果到论文证据的因果链 | 自动生成文章不代表科研主张正确或论文保底 |
| [cleanlab/cleanlab](https://github.com/cleanlab/cleanlab) | 11.7k | 数据/标签质量与异常样本分析 | 数据优先、发现失效与标签问题 | 模型对数据的可疑标记不自动等于真实标签错误 |
| [SakanaAI/AI-Scientist-v2](https://github.com/SakanaAI/AI-Scientist-v2) | 7.4k | Agentic tree search、实验管理、有限候选展开 | 必要时小规模科学机制分支与实验树追踪 | 官方指出开放 v2 在强起始模板下可能不如受约束的 v1，不可推断更多搜索必然更成功 |
| [WecoAI/aideml](https://github.com/WecoAI/aideml) | 1.6k | 代码节点的 generate→debug→benchmark 搜索树 | 少量不同代码实现竞争、保留 lineage | 代码搜索与 ML benchmark 胜率不等于科研创新或论文增益 |
| [SakanaAI/AI-Scientist-v3](https://github.com/SakanaAI/AI-Scientist-v3) | 0.6k | task investigation、ablation、sealed final evaluation、posthoc、paper 分阶段证据 | 开放探索与最终确认严格分离 | 不要求容器编排、自动写论文、多模型评审或覆盖旧框架 |
| [DVC](https://github.com/iterative/dvc) | 未在本轮 API 确认 | 数据/实验版本与可复现流水线的典型工具 | manifest、data_version、split_protocol、按依赖增量复跑 | 不强制安装 DVC 或额外重复存储大型文件 |

## 对第十章最重要的五项迁移

1. **研究问题范围先于具体模型**（RD-Agent + Cleanlab）：从数据和可信科学问题发现任务，不在选题时赌一个必胜机制。
2. **保护不可随意变化的评价资产**（autoresearch）：合法 split、共同 evaluator、原始数据与封存确认保持稳定，算法可以迭代；正式协议确需修正则版本化。
3. **有限、有明确反馈的分支探索**（AIDE + AI-Scientist-v2）：默认一主分支，只有独立科学解释且预算合理才开备选，负 Pilot 不推断整个方向失败。
4. **总资源效率**（Optuna + autoresearch）：只跑能带来新信息/恢复能力/可信改进的实验，允许早停不值得的单分支，但禁止无限搜索和对 test 调参。
5. **探索—确认分离**（AI-Scientist-v3 + MLflow）：任务选择、开发调优、最终确认分开，明确每条结论的 provenance、可反驳条件和论文边界。

## 科研适配为何有别于 ML 自动竞赛

- 本章的最优目标是**有效、可重复、具有独立价值的科研 Claim / 单位总研发成本**，不只是开发集上的最高分。
- 一个数据集上发掘多个任务、指标或切片会产生**选择偏差**，应预留独立确认或限制主张；高星自动实验框架本身不会解决这一点。
- 神经网络/优化方法之外，还允许从物理理论、数据质量、任务定义、可靠性与实验能力中产生科研贡献。
- 各项目的许可证不同，若需实际安装、复制源码或外传数据，应查看相应项目的正式许可；本章仅写独立的 Markdown 工作指令。
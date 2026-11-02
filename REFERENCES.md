# 第十章｜开源工作流对照与可迁移机制（2026-11-02 复核）

> 只引用公开官方仓库或官方文档；**Stars 不是科研效能、真实性或投稿成功率**，故不再维护易过期的星数排名。以下仅借鉴任务组织与实验可追踪性，不代表已安装这些框架，也不复制第三方提示词或代码。

| 开源项目与官方来源 | 值得借鉴 | 在第十章中的落地 | 不照搬的部分 |
|---|---|---|---|
| [Microsoft RD-Agent](https://github.com/microsoft/RD-Agent) | Research↔Development反馈：用实测残差更新技术假说 | `ALGORITHM_HYPOTHESIS`→Run→改机制/Claim | 不默认复杂多Agent或把改进当新颖性 |
| [Karpathy autoresearch](https://github.com/karpathy/autoresearch) · [program.md](https://github.com/karpathy/autoresearch/blob/master/program.md) | 固定评价基础设施、短反馈、可回退代码、逐次记录 | 保护 evaluator、`BEST_VALID_RUN`、原始负结果与版本 | `LOOP FOREVER`、仅按单一开发分数保留，均不适用于论文确认 |
| [AIDE (WecoAI/aideml)](https://github.com/WecoAI/aideml) | 代码试验树、调试、分支血缘 | 一个主分支＋不同解释的有界备选，保留负结果和parent_run | 代码竞赛得分与科学发现不能划等号 |
| [MLEvolve](https://github.com/InternScience/MLEvolve) | 经验记忆、渐进式跨分支搜索与停滞识别 | 复用成功与负结果，依据不同失败前提决定`NEXT_PROBE` | 不默认记忆服务、无界树搜索、GPU堆叠 |
| [AI-Scientist-v2](https://github.com/SakanaAI/AI-Scientist-v2) | 假设—实验—反馈的开放探索与实验管理 | 有界的候选任务/机制探索 | 官方承认：有强起始模板时开放 v2 不一定优于 v1；多分支不保证成功 |
| [AI-Scientist-v3](https://github.com/SakanaAI/AI-Scientist-v3) | 研究调查、消融、独立末次评估分离 | 活动05的`CLAIM_EVIDENCE_MAP`与活动06封存确认严格分离 | 不把高验证分数或论文自动生成当科学成功 |
| [MLflow](https://github.com/mlflow/mlflow) | Run 参数、指标、产物与血缘 | 复用现有 STATE/RUNS/CLAIMS 指针和可恢复比较 | 不强制部署追踪服务器 |
| [Optuna](https://github.com/optuna/optuna) | 有界 Trial、记录搜索史和低成本剪枝 | 按新信息/总成本选择试验，保留被淘汰分支 | 低保真剪枝不是机制科学证伪；不在 test 上调参 |
| [Cleanlab](https://github.com/cleanlab/cleanlab) | 标签质量、数据问题定位 | 开放观察时审查标签/数据真实性 | 模型标记的可疑标签不等于真实标注错误 |
| [DVC](https://github.com/treeverse/dvc) | 原始数据和实验版本可追溯 | manifest、data_version、split/protocol_id、增量复跑 | 不强制安装 DVC 或重复存储大型数据 |

## 活动02–03：数据现象与任务发现（设计借鉴，不要求安装）

| 官方开源项目 | 能力及本章迁移点 | 注意 |
|---|---|---|
| [FG Data Profiling](https://github.com/data-centric-ai-community/fg-data-profiling) | 快速数据画像 → `DATA_INSIGHT.md` 的原始分布/缺失 | 自动报告不等于任务科学贡献 |
| [Microsoft Data Formulator](https://github.com/microsoft/data-formulator) | 探索时衍生问题、保持数据线索 → 定向追问 | 不无限生成图表/Agent |
| [Renumics Spotlight](https://github.com/Renumics/spotlight) / [Sliceguard](https://github.com/Renumics/sliceguard) | 多模态/异常切片探索 → 组级科研现象候选 | 自动找出的切片须复核样本量/多重搜索 |
| [Cleanlab](https://github.com/cleanlab/cleanlab) | 疑似标签错误、重复和异常 → 数据假象排查 | 部分诊断依赖模型概率/特征，未经授权不拟合；标记不是真值 |
| [Evidently](https://github.com/evidentlyai/evidently) / [Deepchecks](https://github.com/deepchecks/deepchecks) | 分布变化、数据与模型诊断 → 决定哪类任务值得试 | 数据分布漂移不等于性能下降 |
| [Microsoft Responsible AI Toolbox](https://github.com/microsoft/responsible-ai-toolbox) | error analysis与困难数据群体 → 从失效转任务 | 须合法group、逐样本预测和独立确认 |
| [tsfresh](https://github.com/blue-yonder/tsfresh) / [sktime](https://github.com/sktime/sktime) | 时间序列专用特征/任务诊断 → 按需路由 | 不在非时序数据强制使用；拟合需授权 |

只迁移分析思想；库的许可、版本、运行成本及本地安装权限在真正调用时核查。不应为了使用这些工具而改变用户本轮学科。

## 活动01搜索机制（移植设计，不默认安装）

| 官方 GitHub 项目 | 借鉴 | 不照搬 |
|---|---|---|
| [STORM](https://github.com/stanford-oval/storm) | 多视角问题地图、追问、引用 | 不自动产出长篇百科报告 |
| [GPT Researcher](https://github.com/assafelovic/gpt-researcher) | 研究问题规划、证据与来源合成 | 不默认部署多Agent |
| [Deep Research](https://github.com/dzhng/deep-research) / [Local Deep Researcher](https://github.com/langchain-ai/local-deep-researcher) | 递归检索、深广调节、发现证据缺口 | 不无界搜索 |
| [SearXNG](https://github.com/searxng/searxng) | 多搜索源减少单源覆盖偏差 | 不强制自建搜索服务 |
| [PaperQA2](https://github.com/Future-House/paper-qa) | 论文原文依据与具名近邻核查 | 不把未读论文声称已核 |
| [last30days-skill](https://github.com/mvanhorn/last30days-skill) | 最近社区/项目动态作热点线索 | 热度≠真实科研价值 |

具体转换见[SEARCH_DISCOVERY.md](SEARCH_DISCOVERY.md)。OpenAlex/Semantic Scholar等只有真实可用时才作为论文元数据来源；未接通API不假称查询。无Star排名、无第三方代码复制。

## PD-RW v1.3｜从优秀项目移植的五项小机制

1. **选题必须落成可验证的建议**（RD-Agent）：不是堆热门模型，而是“为什么选数据/反对理由/最大未知/下一最廉价检查”；用真实反馈更新科研问题。
2. **单一对照＋完整实验血缘**（autoresearch、AIDE、MLflow）：稳定的合法evaluator、`Champion–Challenger`、保存负结果/异常/版本；不复制autoresearch的无限循环或仅以开发分数推进科研。
3. **任务阶梯必须有不同的可检验前提**（AIDE分支追踪、AI-Scientist-v2多路径探索）：`COMMON_PREMISE/NEW_LEVER`先辨认是否只是换名；v2官方说明开放树搜索在强起点存在时可能弱于更受约束方式。
4. **确认前冻结完整任务快照**（AI-Scientist-v3、DVC）：把task/level、K预算、support/query信息时序、评价器与原始模型绑定在同一确认合同；没有满足任务的封存数据时诚实记`CONFIRMATION_UNAVAILABLE`。
5. **测量Agent行为，而不只检测Markdown关键词**（AIDE实验血缘、v3 sealed evaluator）：合成反例先测试合同与红线，随后以真实项目历史冻结点做**遮蔽后续结果的行动回放**，比较是否选择正确的最小探针、避免非法训练/假降级/确认污染、是否保留负结果与资源成本。尚未跑真实Agent对照时只能说`NOT_MEASURED`。

**不会照搬**：复杂多Agent系统、无界GPU搜索、强制长模板、流水账或自动生成即算论文成功。外部GitHub热度不证明科研成功率；上述都是设计借鉴而非已在用户电脑安装/运行框架。第三方代码和数据许可按实际用途复核。

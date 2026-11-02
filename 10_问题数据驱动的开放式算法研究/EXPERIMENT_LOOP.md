# 活动 04｜有界算法研发、可恢复实验与自动纠错

## 1. 默认模式：先让真实科学问题变得清晰

开始开发前**不要求完整论文级假说、SOTA复现或所有机制消融**。按当前 TASK 和权限选择：
- DISCOVERY：真实开发数据上观察现象、误差、可见信息和问题定义；只读、拟合训练分别核权限。
- ENABLEMENT：恢复数据读取、同步、标定、形状/时间/分组、评价器、日志、训练稳定性等必要能力；工程验收无需新算法增益。
- BASELINE/IMPROVE：准备宣称性能差异才运行同任务/同输入/同组别的简单可信基线与合理优化；最强近邻正式确认前必须公平比较，缺失写 BASELINE_PENDING。
- MECHANISM_TEST：科学解释或新机制比较时先写 A/B 差异预测、负对照或合成正控；没有真正机制归因需求时不虚构 A/B。
- CONFIRMATORY：只在冻结最终候选和获得相应用户授权后，交 [CONFIRMATION.md](CONFIRMATION.md) 执行。

## 2. Agent 一次性中等粒度任务指令（可直接改字段）

> TASK：基于最新有效开发数据与代码，解决当前 TASK_ID 中最有信息价值的一个问题。先复用数据manifest/已验证Run；检查本轮权限、冻结协议与确认集。仅按需要读取项目 STATE、相关实现及本文件。
>
> EXECUTE：在已授权范围连续完成最小真实验证→必要局部实现/修复→公平的最简基线或差异实验→保存原始预测、配置、数据与源码版本→最小相关回归测试。首次合法非训练原型可以先做 shape/mask/时序及真实batch读取；不因缺新机制/强基线增益停止。
>
> CONTROL：固定本轮所用合法开发分组、共同评价器、预测前可用输入、主要指标/分母；允许在开发组上改进，但不读封存确认集、不改变已冻结验证范围、不扩张下载/拟合/GPU/费用权限。
>
> REPAIR：异常先定位第一个真实错误，定向复现→局部修复→验证受影响不变量→自动恢复原任务；若模型本身真实负结果，不强行当成代码Bug。改变标签/划分/时钟/评价器时，只使受影响Run失效并重算，保留其他有效证据。
>
> OUTPUT：实际新增Run/观察及路径、相对公平基线的有效效应/不确定性或 UNKNOWN、修复及验证、使用资源、保留/淘汰的分支和下一最低成本判别；若没执行写 NOT_RUN，不抄全部日志。

**重要授权**：用户只允许无拟合前向/只读时，不可训练 CPU Ridge、tiny-set 过拟合或 GPU 模型；真实训练需要对应授权。CPU/MEM/GPU实际开销按用户批准预算计，源代码中的“已有许可”不能替代真实用户消息。

## 3. 有界实验循环：可记录、可对照、可恢复

1. **读取资产**：最新问题—数据组合、TASK_ID、BEST_VALID_RUN（最佳有效Run）和数据/协议/源码版本；实验不存在时用最低成本可运行观察，别重做已完成实验。
2. **选择下一实验**：优先能区分科学解释或验证实验能力、降低不确定性的操作；合理优化优先于无依据的复杂模型。比较性能时，为基线与候选提供公平的优化资源。
3. **区分修改范围**：PROTECTED = 原始标签、合法分组、评价器、未接触确认集和用户冻结对象；EDITABLE = 在当前授权和实验合同内的模型、特征、Loss、nuisance 调参。评估协议修正须新 protocol_id 并重新核算受影响记录。
4. **执行可复现 Run**：单独保存原始代码/commit、data/version、split、评价器版本、seed、超参数、状态、预测/指标、成本、raw path。使用最小可读取日志，避免把完整训练输出倒入上下文。
5. **分类而非一刀切**：KEEP（有效证据支持继续）；IMPROVE（可信但未达目标，下一实验信息增量明确）；REPAIR（有界实现/评价失效）；INCONCLUSIVE（功效不足/欠收敛/有效比较不充分）；DISCARD（该机制或Run不值得继续）。所有决定必须写 DECISION_SCOPE=RUN|MECHANISM|TASK|AREA_DATA。
6. **恢复/预算**：有已批准剩余额度且下一实验有价值就继续；预算达到上限或实验不产生信息则 HOLD，说明续做条件。**autoresearch 的无限循环只是参考实验反馈，不移植到本章。**

## 4. 区分“无法学习”和“没有训练好”

在合法训练预算内，根据曲线/能力诊断选择是否值得做成对长短训练锚点、真实标签正控、匹配容量基线、分组误差/配对预测。短 Pilot 与欠收敛不能直接推断强机制不可能；低功效不等于效应为零。但反复无信号且成本增加时，要明确止损而不是无限调参。

- 相同组别与输入、相同目标和评价分母才允许做公平提升比较；Oracle使用未来/额外信息只作诊断，不是部署策略的数学上界。
- 传感器时序需核相对时刻、对齐、单位、真实采样率、漂移、train-only 归一化；变化时定向跑数据不变量。
- 简单方法可行就先保留为强资产；新机制需能明确科学价值和性能/条件增量，但早期允许探索不立即提分。
- GPU利用率不是科学 KPI；不能为了填满显存而扩大无信息量实验。

## 5. 分支纪律与 Token 效率

默认为**一个主分支＋按需少量机制竞争分支**。AIDE/AI-Scientist-v2 的树搜索只在明确具备可比较候选和资源时借鉴；没有必要做完整树搜索图、复杂多 Agent 平台或重复代码生成。每个分支记录 parent_run / task_id / protocol_id / changed_scope / rationale / evidence。没有新可学信息时结束本分支；不要拿不断搜索的最优 dev 指标冒充 confirmatory 增益。

**Run 最小日志（可用旧文件）**：run_id | task_id | parent_run | data_version/split_id | code_commit | protocol_id | train_auth | wall_gpu_time | metric_or_observation | evidence_scope | status | decision | raw_paths。

**默认输出格式**（尽量短）：完成/NOT_RUN；最佳合法Run与增量证据；重要修复/残余风险；下一个最便宜的有效动作，真实授权或预算缺口。论文强证据见 [CONFIRMATION.md](CONFIRMATION.md)。

**参考**：[autoresearch/program.md](https://github.com/karpathy/autoresearch/blob/master/program.md) 借固定评价/实验记录和回退；[RD-Agent](https://github.com/microsoft/RD-Agent) 借反馈式研发；[AIDE](https://github.com/WecoAI/aideml) 借有限树分支；[Optuna](https://github.com/optuna/optuna) 借有预算的试验搜索与剪枝思想。
# PD-RW｜算法编码与实验执行指南（只在编码/排错时加载）

> 总决策见 [WORKFLOW.md](WORKFLOW.md)，实验预算与公平性见 [EXPERIMENT_LOOP.md](EXPERIMENT_LOOP.md)。本库以现有真实 TASK、基线、原始Run和关键可证伪实验为执行依据。只读当前TASK相关STATE/代码/Run，不重建已验证工程。

## 1. 从研究任务到第一份有效代码

**最小任务合同**：
`TASK_ID/level_id | X(shape,单位,mask,时间,部署可见信息) | y(独立真值/时点) | group_id | split/protocol | metric/分母 | PROTECTED | EDITABLE | 本轮最小验收`

推荐的接口**语义**（不是强制目录）：
```text
Data:    sample_id, group_id, timestamp, X, y, valid_mask
Split:   train_ids / dev_ids / sealed_holdout_manifest, split_version
Prep:    fit(train) -> transform(train/dev)     # dev/test不参与拟合
Model:   forward(legal_inputs, legal_history, mask) -> prediction
Train:   config, seed, learning_curve, checkpoint, code_commit
Eval:    sample_id, group_id, y_true, y_pred, mask, metric + denominator
Run:     run_id, parent_run, data_version, protocol_id, cost, raw_paths
```

**顺序**：核真实开发batch与ID/标签/时钟 → 合法group split、train-only预处理 → 简单基线 → 逐样本预测及评价器 → 必要创新模块。已有有效资产直接复用，数据和预处理正确不代表科学命题成功。原始血缘、holdout与评价器默认PROTECTED；确实有错才版本化修复并重算受影响Run。用户未授权时不得下载/安装/CPU Ridge拟合/tiny-set训练/GPU更新；无参数更新的检查也须遵守对应权限。

## 2. 架构选择：由数据规律、剩余误差和物理依据驱动

| 真实任务/错误证据 | 简单可信起点 | 有依据才升级 | 最强简单替代 |
|---|---|---|---|
| 小样本、连续信号、强自相关 | Persistence/Ridge/Residual-Ridge | 非线性或长依赖残差→TCN/GRU | 合法历史长度、线性残差 |
| 局部时序事件、实时识别 | 阈值、状态机、轻量事件模型 | 事件关系复杂→TCN/GRU | 阈值与窗口 |
| 长上下文真正必要 | GRU/TCN | Transformer/SSM（已有环境） | 更长输入和容量 |
| 跨人/设备/日期漂移 | pooled、target-only、同K校准/微调 | 稳定物理残差/适应模块 | K预算与标准化 |
| 多模态、按需启用 | 单模态、固定融合/固定启用 | 可辨识信号支持动态策略 | 同成本简单固定策略 |
| 浓度/漂移混杂 | 匹配条件统计、简单校准 | 可区分物理机制→结构化模块 | 浓度与批次共变 |

新机制开工前写`WHAT_CHANGES_ONLY`（只修改哪个模块/信息/损失）＋`EXPECTED_SIGNATURE`（在哪个合法开发组与简单替代不同）＋`REMOVAL_CONDITION`；只有机制归因才要求对照。缺证据标HYPOTHESIZED，不按模型热度堆架构。

### 机制与工程变更分开

收到`ALGORITHM_HYPOTHESIS`后先核`ERROR_PATTERN`有实际开发证据还是`HYPOTHESIZED`；选择`MECHANISM_LEVER`（合法额外信息/归纳偏置/优化/容量），说明与当前Champion同输入、同K、同预算的`STRONG_SIMPLE_ALTERNATIVE`，设计可观察`DISCRIMINATING_SIGNATURE`。新信息不能从预测后的标签、未来状态或封存集取得；额外信息成本要计入比较。未核可用性先做低成本正控，不能直接把Oracle差距当部署收益。

算法优化修改`EDITABLE`内最相关的模块，保留`PROTECTED`的split、真值、评价器；同一机制必要的协同改动可成组，但机制和学习率/epoch等`nuisance`变化须在归因时区分。完成Run后用原始逐样本预测、group差额与训练曲线反馈给活动04；**模型更复杂不是创新证据，工程PASS也不是科学增益**。

## 3. 实际编码测试：按变更选择，不是全套审批

| 改动 | 有效行为证据 | 有区分力的反例 |
|---|---|---|
| 数据与标签 | 真实batch核sample_id、时间、单位、mask、标签和手算值 | 错序ID/重复事件/缺帧 |
| split/预处理 | 独立group不交叉，统计只fit(train) | 改dev极端值不影响train均值 |
| 在线预测/缓存 | 不看未来帧、未来标签、未启用模态 | 置换未来内容当前预测不变 |
| 新网络/Loss | shape/dtype/有限值、Loss方向、梯度、冻结范围 | 零mask、反标签、空序列 |
| 训练与加载 | checkpoint恢复、曲线与seed；tiny-set仅在获训练许可后 | 训练/推理不一致 |
| 评价与K-shot | ID对齐/分母手算；support/query不重叠、标注早于预测 | 未来标签support必须拒绝 |

**修复流程**：最小失败输入→定位→局部改动→受影响测试→真实batch端到端；原坏Run保留INVALID证据，未验证写NOT_RUN。工程PASS不代表新机制增益，不能把F1上升写成必过的单元测试。

## 4. 训练症状与预算决策

| 症状 | 先诊断 | 后续行动 |
|---|---|---|
| Loss不降/NaN | 单位、标签、mask、Loss符号、优化器、梯度和fp32小批次 | 修复后再调参 |
| train好而dev差 | 时间/group泄漏、train-only归一化、过拟合 | 合法正则与独立组 |
| 最末checkpoint仍改善 | 曲线、最佳checkpoint、公平训练时长 | 成对延长基线与候选 |
| 新模块无收益 | 强简单替代、残差、正控和欠收敛 | 有不同预测才扩机制 |
| 提升但K/输入/预算不同 | NOT_COMPARABLE；核同K同组对照 | 补匹配公平基线 |
| 特定切片才有效 | 独立group数、选择史、组级不确定性 | 可复验才扩大 |

超参按`scientific`（机制变量）、`nuisance`（学习率/正则/epoch等需公平调优）、`fixed`（任务、合法信息、split/evaluator）分类，记录合理搜索范围、次数、停止规则、成本。候选充分调参、基线只用默认参数不构成公平增益。

**扩GPU依据**：欠收敛→成对短/长；容量不足有证据→成对小/大；组级不确定→优先独立group而不是seed；评价错误→先修；没有新信息→HOLD受影响机制。不能以显卡空闲为由扩大训练。

## 5. 可直接交给 WorkBuddy / Codex 的短指令

```text
围绕现有TASK_ID和NEXT_PROBE，在获批预算内取得一个可信Run。
核真实STATE/manifest/BEST_VALID_RUN，复用数据、代码、已有效的训练证据。
锁定真值、合法group/split、评价器、K与部署时可用信息；仅改本轮授权模块。
先完成受影响的行为测试和真实开发batch，再做公平基线/机制实验。
遇Bug最小复现→局部修复→定向回归；负Pilot不要自动项目级STOP。
保存逐样本预测、config/commit、data/protocol版本、成本与正负原始Run。
只输出新证据路径、实际测试、机制级决定、风险与一个NEXT（含权限缺口）。
禁止读取封存test择题、未授权训练/外传、静默更改协议或编造贡献。
```

跨层级更换K/真值/合法信息先核 [TASK_LADDER.md](TASK_LADDER.md) 中的共同失败前提、新增杠杆和协议；正式论文证据见 [CONFIRMATION.md](CONFIRMATION.md)。

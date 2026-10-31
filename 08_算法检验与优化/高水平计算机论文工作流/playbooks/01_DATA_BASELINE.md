# 01｜数据、评价器与强基线：先证明比较合法

**何时读**：新数据、基线不可复现、指标/标签/划分变更、传感器时间对齐不明。先复用项目可信 Run，不要求重新采集/训练。关联 `02-B`、`03-B`。

## 1. 先锁定真实可检验任务

Agent 从真实数据和部署条件写 6 项**具体值**，不填泛泛原则：

`Claim | Input(t)与部署可见信息 | Target(t+h)/独立真值来源 | group与时钟/单位 | split与预处理拟合范围 | primary metric及分母`

- 查看字段、许可证、对象/episode ID、时间戳、频率/异步偏差、缺失、标签生成代码。**模型生成/同源派生标签 ≠ 独立真值**；无真实闭环记录不能把离线预测称为控制精度/成功率。
- 按科学泛化目标选独立分组（对象、任务、受试者、会话等），使 train/val/holdout 不交叉；需要时间预测时确保输入仅为 t 前可见值、目标时间严格按任务定义。标准化/阈值/特征筛选仅 fit train；验证/测试不参与拟合。
- 先用一个真实小 batch 检查 shape、dtype、单位、NaN、时间对齐、正负标签、ID 唯一性；对一组手算样例重算评价指标，保存评价器指纹。

## 2. 强基线复现合同（P0-3）

**最低两档**：常量/多数类、Persistence、Ridge/AR 等最简单可信方法（按任务选）＋真正最接近的可运行强基线；必要时加标准 backbone。不要因为论文用了“更先进”的模型就认为是强基线。

| 对齐维度 | 必须相同或写明不能比较的原因 |
|---|---|
| **任务** | target、horizon（真实时间还是帧数）、时序容差、正负定义 |
| **信息** | 输入模态、历史窗口、动作/未来信息、可用触觉次数/成本；Oracle 仅作上界 |
| **评价** | 相同 sample/group IDs、有效掩码、排除规则、metric 代码和分母 |
| **训练公平** | 可比数据、合理且透明的调参机会/训练资源；不能暗中不给基线调学习率 |
| **可复算** | 官方方法/版本或已验证 Run、数据/配置/协议指纹、预测或指标来源 |

按 `官方/既有证据 → 本地重算评价 → 一项差异诊断` 递进；原作者数据/权重/协议不同的论文分数仅作参考。强方法复现失败记 `STRONG_BASELINE_NOT_REPRODUCED`，附最可能差异与低成本替代，不用失败的弱实现宣称 SOTA。

**最小测试**（按真实字段实现，不把示例当现成测试）：分组无交集；过去输入改变未来不影响当前预测；train-only 拟合；新法与对照按相同 `sample_id,group_id,target,prediction,valid_mask` 对齐；全部失败样本也计入覆盖率报告。时序/标签或 metric 代码改变时，标注哪些旧 Run 不再可比，只重算受影响下游（可参照 [DVC](https://github.com/treeverse/dvc)）。

## 3. 判断与交付

- `READY`：真实数据、独立性/因果、指标与至少一个可信简单基线可复核；相应 Pilot 仍需实际资源授权。
- `LIMITED/VALUE_UNVERIFIED`：只有代理标签/离线指标；可继续合法探索，但收窄科学主张。
- `INVALID/BLOCKED`：标签循环、不可修复泄漏、关键真值或闭环缺失；只阻断受影响主张/实验。外部数据缺失时记 `WAITING_FOR_DATA`，不以合成数据填补真实性。

**只交付**：6 项任务合同＋1 张真实基线对比/阻断表＋原始证据指针，不新建重复台账。

参考：[Microsoft ML Fundamentals](https://github.com/microsoft/code-with-engineering-playbook/blob/main/docs/ml-and-ai-projects/ml-fundamentals-checklist.md) · [REFORMS](https://pmc.ncbi.nlm.nih.gov/articles/PMC11092361/)。

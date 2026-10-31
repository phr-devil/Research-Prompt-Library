# 02｜算法设计、实现与定位错误：只添加可验证机制

**何时读**：设计新模块/损失、实现 MVP、训练不收敛、接口/梯度/显存异常。对应 `03-A/C/E`。直接读既有代码、数据和可信 Run；不重建环境、不要求多 Agent。

## 1. 模块级实现合同（P0-1）

开工前在现有 `TASK_CONTRACT` 填一行/一小段实际内容：

`Problem gap → mechanism prediction → Input/Output(shape,units,time,mask) → backbone/reused parts → new module signature & representation → Loss/supervision → train vs inference inputs → remove/replace ablation`

必须能回答：
- **为什么是新机制？** 最近邻在哪种可观测情形失败？更简单的统计/线性/标准 backbone 是否能解释同一现象？给出反事实预期，不以命名新模块代替创新。
- **怎么算？** 指明张量索引、关键模块接口、Loss 公式与方向、负样本/伪标签来源、可训练参数/冻结范围；明确部署时不可用的老师信号、未来帧和缓存更新顺序。
- **复杂度预算**：明确「复用什么、新增什么、刻意不做什么」；不能独立消融或没有可辨别增量的模块优先删。对已有运行链路只改必要文件。

**结构选择分叉**：不确定该用 Ridge/TCN/GRU/Transformer、何时需要跨模态或门控机制时，只读 [算法架构与机制选择参考](ALGORITHM_DESIGN_REFERENCE.md)，先选 2–3 个候选并给出可证伪差异；不要仅凭“先进模型”扩模。

## 2. 关键行为测试矩阵（P0-2）

按所改模块只挑有区分力的测试，输出 `test name | 输入 | 不变量 | 实际命令+结果`。

| 测试类型 | 实际检查 / 失败提示 |
|---|---|
| **最小功能** | 真实 batch 输出 shape/dtype/有限值；空序列、单样本、缺失模态、全零/全一 mask 按定义处理 |
| **不变性** | 更改未来帧/不可见标签或被 mask 内容，不得改变当前预测（对在线/因果模型）；检查状态缓存 |
| **方向性** | 手算 2–3 个 Loss 样例、标签取反/权重为零的预期变化；验证归约和目标方向 |
| **可学习性** | 梯度有限且到达创新模块、冻结参数不更新；合法 tiny-set 是否可过拟合（**不证明泛化**） |
| **训练/推理一致** | inference 禁用训练专用信号；预测和评价按 ID/时间/掩码对齐 |
| **资源/可复现** | 获批的小规模真实实测显存、吞吐、精度；记录 seed/环境/非确定性范围 |

**可执行测试**：按 [PyTorch 合同测试模板](../templates/test_algorithm_contract.py) 与 [接入方法](../templates/ALGORITHM_TEST_USAGE.md) 适配真实算法；未接入适配器必须失败，未实现的可选测试是 SKIP，不可报已验证。传感器/异步时序按需读 [专项诊断](SENSOR_DIAGNOSTICS.md)。

已知软件行为或 Bug 用 **复现失败→修复→相关回归**；未知科学收益由真正的开发评价和后续确认检验，**禁止把“新算法必须提高 X%”写成单元测试**。可借鉴 [Testing ML](https://github.com/GokuMohandas/testing-ml) 的最低功能/不变性/方向性分类。

## 3. 从训练症状选择第一项诊断（P0-5）

| 训练症状 | 优先检查与最小动作 |
|---|---|
| Loss 不降、NaN | label/量纲/target、loss 符号、参数是否进入 optimizer、梯度范数；合法小 batch 用 fp32/简单优化器核算，尝试 tiny-set |
| train 好而 val 差 | train-only 预处理、组划分/邻近时间窗口泄漏；分对象误差与训练/验证曲线，再查容量/正则 |
| 新法不如 Ridge/Persistence | 回到 [01](01_DATA_BASELINE.md) 检查公平协议、时间跨度和分组残差；不盲目扩模 |
| OOM/太慢 | 先定位权重/激活/optimizer/序列长/IO/编译开销，测真实 peak 和每步吞吐；改变 batch/精度后重核数值与学习率 |
| 消融后掉点 | 不能自动证明机制：控制参数量、训练机会、输入信息和成本；转 [03](03_EXPERIMENT_LOOP.md) 设计负对照 |
| 工程 PASS 但科学价值低 | 检查 Claim 与最近邻差额/真实任务证据；没有信息收益的外围优化不做 |

**调参不能替代排错**：训练曲线显示发散/无学习/过拟合等不同问题，先区分数据、优化、实现、评价、科研无增益，再做一项最便宜的有区分力修复。参考 [Google Tuning Playbook](https://github.com/google-research/tuning_playbook)。

## 4. 本轮验收

提交实际 diff/commit、最小失败输入（如有）、相关测试**新鲜日志**、真实 batch 的端到端证据及受影响 Run；未运行标 `NOT_RUN`。工程通过仅标 `ENGINEERING_VALID`，不等于机制/任务收益。普通修复可在原授权连续进行；GPU、额外安装、正式实验/协议变更、外传需另有真实授权。

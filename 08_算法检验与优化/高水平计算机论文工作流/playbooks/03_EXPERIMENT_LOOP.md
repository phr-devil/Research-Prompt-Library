# 03｜有界实验与算法优化：先区分解释，再追逐指标

**何时读**：有可信基线后探索新机制、调参、诊断负结果、设计消融/统计。对应 `02-C/E`、`03-D/E`。禁止自动无限试验及测试集调参。

## 1. 实验选择与计算预算（P0-4）

每轮选**一项可能改变科研Claim判断的实验**：`Claim/新知识 | 最近有效Run/公平强基线 | 机制解释A/B及不同预测 | 真值/独立单位 | 对照与成本 | 授权及停止判据`；不能改变科学判断的试验不优先。

超参数分为：
- **scientific**：本轮要研究其科学效果的变量（例如传感器门控机制）；
- **nuisance**：为公平比较需分别给予合理调优机会的变量（如两种结构各自适合的学习率）；
- **fixed**：本轮保持一致、但结论仅适用于该设定的条件（如 horizon、对象组、评价协议）。

参考 [Google Tuning Playbook](https://github.com/google-research/tuning_playbook)：**只改模块而失衡调参不公平**；联合改动不能冒充单模块因果作用。

优先“**区分解释 / 可得性 / 成本**”；单卡先测合法小规模真实吞吐、显存，预算由用户已批准的 `max_trials/max_gpu_time` 等决定。已有好 Run/ckpt 复用，保持一条 `BEST_VALID_RUN` 和少量互异科学分支。

结构选型出现实质竞争解释时参考 [算法架构与机制选择](ALGORITHM_DESIGN_REFERENCE.md)；涉及不同采样时钟、传感器启用及缺失模态时，仅追加 [专项诊断](SENSOR_DIAGNOSTICS.md) 中能改变当前研究决定的测试。

## 2. 最小探索循环

1. **保护评价链**：`PROTECTED`（真值、split、评价器、主指标、确认集）与`EDITABLE`（获批模型/Loss/超参）分开；修评价错误须新`protocol_id`并重算受影响Run，不用确认集选模。
2. **预写结果签名**：触觉信息与阶段捷径在内容打乱/阶段匹配中预测不同；未读取的触觉不能参与开关决策。
3. **分支竞争**：只比较预算内互异预测；记`parent_run/protocol_id/changed_scope`；同协议看增益、复杂度、成本；同分更简可KEEP。负结果保留，INCONCLUSIVE非DISCARD。
4. **检查完整曲线**：至少看候选 train/val loss 与主指标随步数变化，标发散、过拟合、欠收敛、早停/选 checkpoint 的规则；搜索最优值卡在边界时先怀疑搜索空间。记录无效 trial，不只记胜者。
5. **按独立单位比较**：配对效应、样本覆盖、成本、CI/不确定性、失败域与消融；将 seed 变动、调参搜索方差和真实数据采样差异分开。
6. **决策**：`KEEP` 有效且相对复杂度值得的开发增量；`DISCARD` 有效无增量；`INCONCLUSIVE` 无法区分竞争解释；`INVALID` 协议/实现/泄漏等使证据失效。无高价值下轮实验则建议 HOLD/收窄，实质转向由用户决定。 判决补`DECISION_SCOPE=RUN|MECHANISM|CLAIM|PROJECT`、最强反证和重启条件；当前机制负结果不自动否定整个方向。

## 2.5 自适应 GPU 验证：最小充分证据，不追求利用率

**按证据决定规模**（仅在用户已批GPU/时间/次数内，缺授权不启动；明确禁训练时CPU训练亦不启动）：

| 已观测现象 | 下一动作 |
|---|---|
| 评价/梯度/因果尚未成立 | CPU/小 batch 排错，不追加训练 |
| 最佳开发 checkpoint 位于末尾且曲线仍改善 | 在已批预算内有界延长；用验证曲线而非固定步数判断 |
| 基线训练不足或调参机会失衡 | 给基线与候选合理的 nuisance 调优机会，版本化比较 |
| 候选已有可信但不确定的增量 | 在合法独立数据/seed/消融之间分配预算，按证据缺口选择；seed 不代替新对象 |
| 已过拟合、机制负对照失败、真实评价不可识别 | 转诊断/缩窄/HOLD，不因显卡空闲扩大训练 |

获授权后用**真实数据小规模实测**吞吐、VRAM、等待与步耗时；明确 `追加实验→可能改变的科研决定→预计计算→停止条件`。batch 变大可能改善吞吐，**不保证模型变好**，必要时重新核学习率/正则；GPU 利用率不是科学 KPI。保留全部试验、失败和预算余额，超范围需重新获批。

## 3. 统计设计：SESOI/MDE（P0-6）

先定义最小有实际科学意义的效应 **SESOI**，再依据实际**独立组数**及组内相关性讨论可检测效应 **MDE**。同一对象/episode 内的数万帧不等于数万独立样本；几十个训练 seed 主要反映训练稳定性，不代替新对象。配对比较优先用配对差额/按合法组聚类的区间；组数太少时承认不确定性，不做虚假精确的功效承诺。大量候选/子群筛选后不能把同一验证集的最好点当未偏的正式估计。

**报告只留一行/实验**（复用RUNS/STATE；主图是可检验的证据预案，正负结果和所有失败均保留）：`Run & commit/data/config/eval版本 | A/B解释与预测 | 改动 | 共同对照 | 主指标+成本+独立n+CI | 全seed/失败源路径 | KEEP/DISCARD/INCONCLUSIVE/INVALID → NEXT`。正式确认转 [04](04_EVIDENCE_CONFIRM.md)。

参考：[Autoresearch](https://github.com/karpathy/autoresearch) · [Google Tuning Playbook](https://github.com/google-research/tuning_playbook) · [K-Dense Experimental Design](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/experimental-design/SKILL.md)。

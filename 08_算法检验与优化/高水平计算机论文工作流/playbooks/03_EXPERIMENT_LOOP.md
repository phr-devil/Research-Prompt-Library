# 03｜有界实验与算法优化：先区分解释，再追逐指标

**何时读**：有可信基线后探索新机制、调参、诊断负结果、设计消融/统计。对应 `02-C/E`、`03-D/E`。禁止自动无限试验及测试集调参。

## 1. 实验选择与计算预算（P0-4）

每轮先选**一项可改变科学决定**的问题：`Claim/最近有效Run | 竞争解释A/B | 若A或B成立各出现什么结果 | 最小数据/对照 | 预计代价与已获授权 | 通过/无结论判据`。

将超参数明确分为：
- **scientific**：本轮要研究其科学效果的变量（例如传感器门控机制）；
- **nuisance**：为公平比较需分别给予合理调优机会的变量（如两种结构各自适合的学习率）；
- **fixed**：本轮保持一致、但结论仅适用于该设定的条件（如 horizon、对象组、评价协议）。

这是 [Google Tuning Playbook](https://github.com/google-research/tuning_playbook) 的重要区分：**只变一个模块、却让其中一种方法用明显失配的超参，也不公平**。可分组更改耦合配置，但不能把联合改动解释成单模块因果作用。

比较候选时优先“**排除替代解释的能力 / 真实可取得性 / 成本**”，而非预计提升幅度；单卡先测合法小规模真实吞吐、显存，预算由用户已批准的 `max_trials/max_gpu_time` 等决定。已有好 Run/ckpt 复用，保持一条 `BEST_VALID_RUN` 和少量互异科学分支。

结构选型出现实质竞争解释时参考 [算法架构与机制选择](ALGORITHM_DESIGN_REFERENCE.md)；涉及不同采样时钟、传感器启用及缺失模态时，仅追加 [专项诊断](SENSOR_DIAGNOSTICS.md) 中能改变当前研究决定的测试。

## 2. 最小探索循环

1. **固定开发评价**：主指标、独立真值、split、评价器、horizon、样本覆盖与强基线；修改协议必须版本化并重估受影响结果。
2. **预写预测签名**：例如“触觉含真实接触信息”与“门控仅学到阶段捷径”对内容打乱/阶段匹配负对照预期不同；测试时未见的触觉不能参与门控决策。
3. **只做最小有区分力的实验**：允许同次执行相关消融、容量/信息匹配替代、损失权重或模型修正，但各分支有清楚假设、成本和停止条件。
4. **检查完整曲线**：至少看候选 train/val loss 与主指标随步数变化，标发散、过拟合、欠收敛、早停/选 checkpoint 的规则；搜索最优值卡在边界时先怀疑搜索空间。记录无效 trial，不只记胜者。
5. **按独立单位比较**：配对效应、样本覆盖、成本、CI/不确定性、失败域与消融；将 seed 变动、调参搜索方差和真实数据采样差异分开。
6. **决策**：`KEEP` 有效且相对复杂度值得的开发增量；`DISCARD` 有效无增量；`INCONCLUSIVE` 无法区分竞争解释；`INVALID` 协议/实现/泄漏等使证据失效。无高价值下轮实验则建议 HOLD/收窄，实质转向由用户决定。

## 3. 统计设计：SESOI/MDE（P0-6）

先定义最小有实际科学意义的效应 **SESOI**，再依据实际**独立组数**及组内相关性讨论可检测效应 **MDE**。同一对象/episode 内的数万帧不等于数万独立样本；几十个训练 seed 主要反映训练稳定性，不代替新对象。配对比较优先用配对差额/按合法组聚类的区间；组数太少时承认不确定性，不做虚假精确的功效承诺。大量候选/子群筛选后不能把同一验证集的最好点当未偏的正式估计。

**报告只留一行/实验**（复用 RUNS/STATE）：`Run & commit/data/config/eval版本 | A/B解释与预测 | 改动 | 共同对照 | 主指标+成本+独立n+CI | 全seed/失败源路径 | KEEP/DISCARD/INCONCLUSIVE/INVALID → NEXT`。正式确认转 [04](04_EVIDENCE_CONFIRM.md)。

参考：[Autoresearch](https://github.com/karpathy/autoresearch) · [Google Tuning Playbook](https://github.com/google-research/tuning_playbook) · [K-Dense Experimental Design](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/experimental-design/SKILL.md)。

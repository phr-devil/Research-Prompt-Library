# 03｜有界实验与算法优化：先区分解释，再追逐指标

**何时读**：有可信基线后探索新机制、调参、诊断负结果、设计消融/统计。对应 `02-C/E`、`03-D/E`。禁止自动无限试验及测试集调参。

## 1. 实验选择与计算预算（P0-4）

每轮选可改变Claim判断的实验，标`CHECK_ONLY/MECHANISM_PILOT/DEVELOPMENT_COMPARE/CONFIRMATORY`及推断范围：`Claim | 有效Run/强基线 | A/B与不同预测 | 真值/独立单位 | 成本/授权/停止`。

超参数分为：
- **scientific**：本轮要研究其科学效果的变量（例如传感器门控机制）；
- **nuisance**：为公平比较需分别给予合理调优机会的变量（如两种结构各自适合的学习率）；
- **fixed**：本轮保持一致、但结论仅适用于该设定的条件（如 horizon、对象组、评价协议）。

nuisance需记搜索范围、试验数、选择准则与可比调参机会；联合改动不冒充单模块因果（[Tuning Playbook](https://github.com/google-research/tuning_playbook)）。

优先区分解释/可得性/成本；获批才测真实吞吐/显存；预算限`max_trials/max_gpu_time`。复用有效Run和`BEST_VALID_RUN`。

机制竞争参照[算法设计](ALGORITHM_DESIGN_REFERENCE.md)；时钟/启用/缺模态有疑点才查[专项诊断](SENSOR_DIAGNOSTICS.md)。

## 2. 最小探索循环

1. **保护评价链**：`PROTECTED`（真值、split、评价器、主指标、确认集）与`EDITABLE`（获批模型/Loss/超参）分开；修评价错误须新`protocol_id`并重算受影响Run，不用确认集选模。
2. **签名与探索范围**：已知机制预测先记录；未知机理允许有界探索性扫描以发现条件，事后签名只能算探索结果，须在未参与发现的合法组上复验。触觉内容与阶段捷径用匹配/打乱区分；未读触觉不可参与启用决策。
3. **分支竞争**：预算内比较互异预测，记`parent_run/protocol_id/changed_scope`；看同协议增益/成本，同分更简可KEEP；保留负结果，INCONCLUSIVE非DISCARD。
4. **空结果先校准**：检查train/val曲线、checkpoint与搜索边界；关键空结果且灵敏度不明时，按需用已知有效正控或[02-C](../02_最小科学验证与决策.md)合成正控检查能否检出目标效应；正控不证明真实任务增益。保留无效trial。
5. **独立单位比较**：配对效应、CI、覆盖、成本与失效域；区分seed/调参与采样方差。
6. **决策**：`KEEP`有效开发增量；`DISCARD`有效无增量；`INCONCLUSIVE`证据不足（主指标未增益但机制签名初现，注明`MECHANISM_SIGNAL_UNCONFIRMED`与最廉价复验，不新增状态）；`INVALID`证据无效。无新信息时建议HOLD，不按次数自动STOP。记录`DECISION_SCOPE=RUN|MECHANISM|CLAIM|PROJECT`；改题由用户决定。

## 2.5 自适应 GPU 验证：最小充分证据，不追求利用率

**按证据决定规模**（仅用户已批GPU/时间/次数内；缺授权不启动；禁训时CPU亦不训练）：

| 已观测现象 | 下一动作 |
|---|---|
| 评价/梯度/因果尚未成立 | CPU/小 batch 排错，不追加训练 |
| 最佳开发 checkpoint 位于末尾且曲线仍改善 | 在已批预算内有界延长；用验证曲线而非固定步数判断 |
| 基线训练不足或调参机会失衡 | 给基线与候选合理的 nuisance 调优机会，版本化比较 |
| 候选已有可信但不确定的增量 | 在合法独立数据/seed/消融之间分配预算，按证据缺口选择；seed 不代替新对象 |
| 短Pilot准备淘汰复杂机制且曲线尚未稳定 | 仅在有真实授权及决策收益时用少量同协议成对长/短规模锚点校准；排序不稳标INCONCLUSIVE，不强制所有项目双规模 |
| 已过拟合、机制负对照失败、真实评价不可识别 | 转诊断/缩窄/HOLD，不因显卡空闲扩大训练 |

获批后测吞吐/VRAM，记`实验→决策→成本→停止`；batch大不保证变好，须复核超参；GPU 利用率不是科学 KPI；留失败Run，超范围需重新获批。

## 3. 统计设计：SESOI/MDE（P0-6）

先设**SESOI**，据独立组数及组内相关性估**MDE**。小Pilot只能筛机制，不直接支撑正式Claim。同一对象/episode 内的数万帧不等于数万独立样本；几十个训练 seed 主要反映训练稳定性，不代替新对象。配对比较优先用配对差额/按合法组聚类的区间；组数太少时承认不确定性，不做虚假精确的功效承诺。大量候选/子群筛选后不能把同一验证集的最好点当未偏的正式估计。

**报告一行/实验**（复用RUNS/STATE，保留所有结果）：`Run & commit/data/config/eval版本 | A/B解释与预测 | 改动 | 共同对照 | 主指标+成本+独立n+CI | 全seed/失败源路径 | KEEP/DISCARD/INCONCLUSIVE/INVALID → NEXT`。正式确认转 [04](04_EVIDENCE_CONFIRM.md)。

参考：[Autoresearch](https://github.com/karpathy/autoresearch) · [Google Tuning Playbook](https://github.com/google-research/tuning_playbook) · [K-Dense Experimental Design](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/experimental-design/SKILL.md)。

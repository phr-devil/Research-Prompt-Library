# 03｜有界实验与算法优化：先区分解释，再追逐指标

**何时读**：基线已知后需新机制、调参、负结果或消融统计时。按`02-C/E`、`03-D/E`；禁无限试验和测试集调参。

**宽松探索**：代理/自监督/正控和标定可先做，标`PROXY_ONLY`；能力验收必写，机制比较写A/B。粗预算即可探索；正式Claim仍需独立真值、基线、统计及未污染test，训练须授权。

## 1. 实验选择与计算预算（P0-4）

实验标`CHECK_ONLY/MECHANISM_PILOT/DEVELOPMENT_COMPARE/CONFIRMATORY`和推断范围：`Claim | Run/基线 | A/B预测(机制比较)或能力验收 | 真值/独立组(未知须注明) | 粗成本/授权/停止`。

超参数分为：
- **scientific**：本轮要研究其科学效果的变量；
- **nuisance**：为公平比较需分别给予合理调优机会的变量；
- **fixed**：本轮保持一致、但结论仅适用于该设定的条件。

nuisance记搜索范围、次数、选择准则与公平调参；联合改动不冒充单模块因果（[Tuning Playbook](https://github.com/google-research/tuning_playbook)）。

训练前复用基线及残差，先公平优化可行方案，再依证据选廉价可学性探针或新机制；不强制训练。获批后限`max_trials/max_gpu_time`、核显存，保留`BEST_VALID_RUN`。

机制见[算法设计](ALGORITHM_DESIGN_REFERENCE.md)；时钟异常见[诊断](SENSOR_DIAGNOSTICS.md)。

## 2. 最小探索循环

1. **保护评价链**：`PROTECTED`（真值/split/评价器/指标/确认集）和`EDITABLE`（获批模型/Loss/超参）分开；修错误记新`protocol_id`并重算受影响Run；确认集不选模。
2. **探索先观察**：真实现象/数据签名可先记录，事后切片仅探索、正式主张再独立复验；确认集不选片。
3. **先优化再增强（按需）**：公平调优有效简单方案；只有新信号/残差或合理理论依据时增加机制比较并写不同预测。保留parent_run/protocol_id/changed_scope；同分更简，负结果留档，INCONCLUSIVE非DISCARD。
4. **空结果校准**：先核收敛/能力与搜索边界；科学比较再设已知信号正控/独立n/噪声，正式结论才设SESOI/MDE和检出判据。留全trial；正控PASS不证明真实收益。
5. **成果保护**：保留最佳合法Run；创新失败只淘汰该机制。正式比较报告配对CI/成本/失效域，seed非独立受试者；基线可运行≠论文。
6. **决策**：负结果先区分可信负证与无效Run，`KEEP/DISCARD/INCONCLUSIVE/INVALID`；`MECHANISM_SIGNAL_UNCONFIRMED`须复验，不盲目换模型，机制FAIL≠PROJECT STOP；获批且有判别力→CONTINUE，无效→REPAIR，改Claim→用户选PIVOT，无信息/高成本→HOLD/STOP。记`DECISION_SCOPE=RUN|MECHANISM|CLAIM|PROJECT`，见[续投规则](../RESEARCH_DECISIONS.md)。

## 2.5 自适应 GPU 验证：最小充分证据，不追求利用率

**按证据决定规模**（仅用户已批GPU/时间/次数内；缺授权不启动；禁训时CPU亦不训练）：

| 已观测现象 | 下一动作 |
|---|---|
| 评价/梯度/因果尚未成立 | CPU/小 batch 排错，不追加训练 |
| 最佳开发 checkpoint 位于末尾且曲线仍改善 | 在已批预算内有界延长；用验证曲线而非固定步数判断 |
| 基线训练不足或调参机会失衡 | 给基线与候选合理的 nuisance 调优机会，版本化比较 |
| 候选已有可信但不确定的增量 | 在合法独立数据/seed/消融之间分配预算，按证据缺口选择；seed 不代替新对象 |
| 短Pilot拟淘汰机制而欠收敛 | 获授权且值得时才做同协议成对长/短锚点；排序反转/不确定→INCONCLUSIVE；两点一致也不保证更长预算稳定 |
| 已过拟合、机制负对照失败、真实评价不可识别 | 转诊断/缩窄/HOLD，不因显卡空闲扩大训练 |

获批后核吞吐/VRAM和停止；GPU 利用率不是科学 KPI，保留失败Run，超范围需重新获批。

## 3. 统计设计：SESOI/MDE（P0-6）

正式比较/确认前设**SESOI**，据独立组数及组内相关性估**MDE**；初期Pilot可只声明探索性指标、粗略样本与未验证的检出能力。小Pilot只能筛机制，不直接支撑正式Claim。同一对象/episode 内的数万帧不等于数万独立样本；几十个训练 seed 主要反映训练稳定性，不代替新对象。配对比较优先用配对差额/按合法组聚类的区间；组数太少时承认不确定性，不做虚假精确的功效承诺。大量候选/子群筛选后不能把同一验证集的最好点当未偏的正式估计。

**一行差量记录**：探索/能力`Run | 观察或验收 | config/data | cost/AUTH | evidence | NEXT`；机制比较再补A/B与同评价对照；正式确认再补全seed、独立n与CI。科学比较的KEEP/DISCARD/INCONCLUSIVE/INVALID按范围使用。转[04](04_EVIDENCE_CONFIRM.md)。

参考：[Autoresearch](https://github.com/karpathy/autoresearch) · [Google Tuning Playbook](https://github.com/google-research/tuning_playbook) · [K-Dense Experimental Design](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/experimental-design/SKILL.md)。

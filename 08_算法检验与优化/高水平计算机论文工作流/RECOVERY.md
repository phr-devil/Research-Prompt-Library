# 第八章 v6.1｜按需自主纠错与恢复

> 仅在真实报错、关键不变量异常或结果/证据冲突时启用；不新增研发阶段、必读文件、依赖或专用Agent。默认复用原项目 `STATE/RUNS/CLAIMS`；[REPAIR_ROUTES.json](REPAIR_ROUTES.json) 的24条路由、48例是**按需参考**，不是穷尽的Bug列表。

## 五动作闭环（Agent在实际工具和真实授权内执行）

1. **DETECT（发现）**：代码报错、NaN/OOM、数据/标签/时间/评估矛盾，或关键变更触发的性质检查失败才进入；正常的科学负结果**不等于Bug**。先按 [TRIAGE.md](TRIAGE.md) 限定受影响动作和 `DECISION_SCOPE=RUN|MECHANISM|CLAIM|PROJECT`，未相关的未知项暂缓。
2. **DIAGNOSE（根因）**：复用最近可信 `BEST_VALID_RUN`、原始日志、数据/协议/代码指纹和最后diff，找**最早出现偏差**的步骤；先最小复现，列可证伪的一个根因假说。对未命中48例的异常也按此通法处理，不能因为没有预设类别就STOP。
3. **REPAIR（局部修复）**：对已批准范围内的工程缺陷自动做最小有效改动；有关联的同源问题可连续处理，不逐处请示。**VALUE_CHECK**：昂贵且非必要的修复，应先判断是否能恢复必要实验能力、取得真实新观察或改变科研决定；没有收益且非诚信必修时暂停该修复。科学无增益先检查基线公平性/评价/收敛，再决定有界探索，不以换种子“修”出正结果。
4. **VERIFY（定向验证）**：原失败应在同条件下消失；先跑最小失败测试，再跑受影响模块及依赖的回归测试。标签、ID/时间对齐、split、train-only预处理或评价器变更时额外核对应不变量，并更新受影响Run/Claim；不得把已污染test重新命名为独立确认集。未运行记 `NOT_RUN`；工程通过仅记 `ENGINEERING_VALID`。
5. **RESUME（恢复）**：通过后回到中断前任务与合法预算，从最后有效代码/配置/Run继续；只增量重算确实被改变或污染的证据，不覆盖历史负结果。若有新根因，继续有界定位；不按固定次数停止，也不无限盲修。超过权限、继续无信息价值或涉及重大科学主张时升级给用户。

## 处理边界：修软件与修科学证据不同

| 情况 | 默认处理 | 不能做 |
|---|---|---|
| Shape/接口/环境/OOM/NaN | 最小复现、查梯度/量纲/依赖、局部修复、相关回归 | 无限调参、无验证就宣布科研成功 |
| 标签截断、时间错位、分组/未来泄漏 | 追溯首次异常，隔离受影响 `INVALID` Run/Claim，合法修复后重算 | 保留失效优势、偷看确认集、擅改已冻结协议 |
| 方法输给强基线或Pilot无增益 | 查公平性、收敛与替代解释；若结果有效就保留负结果并评估下一廉价实验 | 把负结果自动当Bug或PROJECT级STOP |
| 复核/图表/稿件不一致 | 根据原始Run和Claim纠正受影响内容，缺证据则降级主张 | 编造实验、假称独立审查已完成 |

**严重度与权限**：`CRITICAL`只阻断受影响操作；`REPAIRABLE`在真实既有授权、范围及预算不变时可自主有界处理，实质分叉才问用户；`MINOR`可顺手修或记录跳过。UNKNOWN不自动致命。CPU/GPU参数拟合、付费、外传/投稿、正式确认和冻结协议变更仍受单独真实授权约束；明确禁训练时CPU/GPU均不训练。第九章改题需用户重新选择。

**自动纠错回复（仅真实阶段结束或需决策时）**：小Bug集中在一次研发结果中简报，不逐错误打断；`修复内容 | 新鲜测试结果/NOT_RUN | 受影响Run/Claim | 恢复到哪一步`，通常1–3行。**已验证修复**才说“已修复并续做”；仅更改代码未执行验证应说“已修改，待验证”，不能假称RESUME成功。发现污染须写明`INVALID`及撤销了什么主张；正常科学负结果只汇报证据和下一项判别，不叫Bug。仅权限、冻结协议、重大改题或无有效廉价下一步时，集中提一个明确问题，不把例行修复变成审批。

**恢复与升级**：优先复用 `research/STATE.md` / `RUNS.tsv` / `CLAIMS.md`，仅增量记录 `route | symptom | first_bad_evidence | root_cause_or_unknown | fix | verify | invalidated_runs/claims | best_valid_run | next_action | authorization`。相关代码或测试未运行则如实标记，不能把静态路由建议当作实际修复。升级只说明受影响目标、证据、阻碍及2–3个可选方向；无真实决策分叉不打断用户。

**按需定位**：`python workflow_route.py --repair 03-D` 只打印当前路由的两个典型故障，`--check` 只静态验证路由。遇新型错误直接遵循上面五动作，不扩充故障大全。参考 [Superpowers](https://github.com/obra/superpowers)、[mini-SWE-agent](https://github.com/SWE-agent/mini-swe-agent)、[pytest](https://github.com/pytest-dev/pytest)、[autoresearch](https://github.com/karpathy/autoresearch) 的原则；不强制安装这些工具。

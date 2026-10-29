# 09｜失败算法科研项目成果挽救与课题转向

**独立于 [08 算法检验与优化](../08_算法检验与优化/README.md) 的专项类别**。主流程：失败证据复核 → 可复用成果 → **三个后续项目** → **用户明确选择** → 选定项目的最小证伪。

- [完整工作流与可复制 Prompt](WORKFLOW.md)（Research Salvage & Pivot v2.1）
- [结构化人工选择门禁（可选 CLI）](salvage_gate.py)：只读核对三项提案和用户选择文件；返回结果不能代替真实用户消息和实验授权

## 一次性使用

直接打开 [WORKFLOW.md](WORKFLOW.md) 复制「一键总控 Prompt」。默认只执行到 Step 05，输出 **P1/P2/P3 三个不同科研项目**、对比和推荐理由后停止，状态为 `WAITING_FOR_USER_SELECTION`。

用户审查后三选一并在**新消息**中明确指定项目编号，才能启动 Step 06。用户没有选择、要求重新推荐或拒绝所有项目时，**不能继续 Step 06**。选择不是 GPU、收费或正式训练授权。

如果历史证据不足以构建三个可信候选，必须 BLOCKED 并解释缺口，不得虚构项目凑数。原始失败结果与冻结结论保持只读。旧路径保留兼容跳转。

## 快速检查门禁（可选）

在项目仓库根目录，Step 05 输出 `research_salvage/05_CANDIDATES.json` 后执行：

~~~bash
python 09_失败算法项目挽救与转向/salvage_gate.py --candidates research_salvage/05_CANDIDATES.json --selection research_salvage/05_USER_SELECTION.json
~~~

退出码 2 = 等待用户选择，退出码 3 = 候选或选择文件无效，退出码 0 = 文件结构合规但**仍必须确认真实用户消息**，也不代表 GPU/付费/实验已获批准。具体选择文件格式见 [完整流程](WORKFLOW.md)。

# 09｜失败算法科研项目成果挽救与课题转向

**独立于 [08 算法检验与优化](../08_算法检验与优化/README.md) 的专项类别**。主流程：失败证据复核 → 可复用成果 → **三个后续项目** → **用户明确选择** → **05-R 科学提炼与可行性优化** → 最小证伪。

- [完整工作流与可复制 Prompt](WORKFLOW.md)（Research Salvage & Pivot v2.2）
- [Step 05-R：已选课题科学提炼与优化](WORKFLOW.md)（选定后单独复制该段 Prompt）
- [结构化人工选择门禁（可选 CLI）](salvage_gate.py)：只读核对三项提案和用户选择文件；返回结果不能代替真实用户消息和实验授权

## 一次性使用

直接打开 [WORKFLOW.md](WORKFLOW.md) 复制「一键总控 Prompt」。默认只执行到 Step 05，输出 **P1/P2/P3 三个不同科研项目**、对比和推荐理由后停止，状态为 `WAITING_FOR_USER_SELECTION`。

用户审查后三选一并在**新消息**中明确指定项目编号，然后优先使用 **Step 05-R** 收敛主张、核验近邻创新、独立真值、强基线和最小可行实验，输出 `05R_REFINED_PROJECT.md`。如果优化改变核心科研问题，须再次取得用户明确确认，不能跳过用户选择直接启动 Step 06。用户没有选择、要求重新推荐或拒绝所有项目时，**不能继续 Step 06**。选择和课题优化都不是 GPU、收费或正式训练授权。

如果历史证据不足以构建三个可信候选，必须 BLOCKED 并解释缺口，不得虚构项目凑数。原始失败结果与冻结结论保持只读。旧路径保留兼容跳转。

## 快速检查门禁（可选）

**提示词库与科研项目通常是两个不同的 Git 仓库**。脚本路径必须指向真正存放 Prompt Library 的位置，不能假定科研项目下存在 `09_...`。先在终端设置 `PROMPT_LIBRARY` 为本库的绝对路径，或者直接把该绝对路径放进命令；本工具只是可选的结构核查，不是 Step 06 的审批器。

在科研项目仓库根目录，Step 05 输出 `research_salvage/05_CANDIDATES.json` 后执行：

~~~bash
python "/absolute/path/to/Research-Prompt-Library/09_失败算法项目挽救与转向/salvage_gate.py" --candidates research_salvage/05_CANDIDATES.json --selection research_salvage/05_USER_SELECTION.json
~~~

路径示例为 POSIX 风格占位符，Windows 请替换为真实的盘符绝对路径。未克隆本提示词库且无法运行脚本时，请直接让独立审查者核对三个候选与用户的最新消息，不能因为缺少 CLI 就宣称已批准。

退出码 2 = 等待用户选择，退出码 3 = 候选或选择文件无效，退出码 0 = 文件结构合规但**仍必须确认真实用户消息**，也不代表 GPU/付费/实验已获批准。具体选择文件格式见 [完整流程](WORKFLOW.md)。

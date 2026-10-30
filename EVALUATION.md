## v6.1 行为评测说明（2026-10-31）

新增离线事件/断点/有限许可检查验证**建议路由**而非真实算法研发完成度。真实端到端测试建议复用同一实验仓库与固定的起始Run，对比v5.4和v6.1：新项目从用户目标到首次合法MVP结果；真实负结果后继续一个有效诊断；基线反超识别代理增益；中断后从有效checkpoint恢复；正式提交保持独立授权。两版采用相同科研任务、实际Agent/模型/工具和预先确定的预算/评价标准，记录人工决策、真实Token消耗、首次可信结果时间、无用实验量与科研结论错误。实验前固定任务样本及评价尺度，优先不含已知答案的新案例。**当前真实Agent A/B = NOT_RUN；效率、成本、成功率 = NOT_MEASURED。**

# Prompt 可复现测试夹具

> 历史 v1.5 + 当前合成压力场景（仍包含v1.9题库） · 2026-10-31。所有输入均为**人工编造的测试场景**，不属于真实项目记录或当年官方募集资料。测试夹具不等于模型实测结果。

## 当前版本的评测与命令（仅生成计划，默认不调用模型）

历史默认仍比较 v1.3 / v1.5 的冻结 SHA；不得把其通过率标成 v1.9 效果。当前版必须显式提供两个 40 位 Git SHA：

~~~bash
python eval_runner.py --suite current --base-ref 35f2b30f8541285430d7285aa414c236ce6ffc98 --candidate-ref <当前提交的40位SHA> --output-dir .eval_runs/current-v19
~~~

当前版 11 个情境覆盖 S01-B、第09类用户选择、失败恢复、跨AI审核缺失、代理标签和论文证据一致性。使用 `--cases N02,N04` 定向评估；当前默认 Pilot 仍仅包含基线与新版都可抽取的 N02/N04/N05/N08；新增 N09（05-R）在旧版本尚不存在，**不应使用 2026-10-29 旧提交作 N09 的 A/B 基线**。N11 另检验“内部传播评分显著却无真实任务价值证据”的决策能力，仅是合成压力场景，不计入默认Pilot或真实模型效果。只有比较两个都包含 05-R Prompt 的不同固定提交时，才使用 `--cases N09 --max-calls 2`。若用 `--all`，先确认两个提交都包含所有案例；9题一次重复需要 `--max-calls 18`，未变化项只作控制而不计收益。必须有真实模型推理、盲评和实际 Token 统计才可宣称效果。本次压力题已用于修订 Prompt，不可当独立留出验证。

## 已有测试与当前状态

- v1.4.1 已记录对17个模板的20项**静态**检查：20/20；仅证明相应规则文字存在。
- 本版扩展为13个可直接复制的场景，预先给定必需条件与严重失败判据。
- **尚未执行独立模型推理和版本A/B对照**；没有模型成功率、节省Token比例或已验证性能提升。

## 独立运行步骤

1. 在同一模型/工具权限下分别使用两个Git提交中的对应Prompt，后接完整的「固定输入」；不能临时调整测试题来帮助某一版本。
2. 保存模型名、版本、时间、原始输入输出、真实Token计量（若可用）。按随机次序运行，使用不知道版本的评估者审查。
3. 逐项检查必需条件，未满足即记失败；只要出现严重失败，整题记为严重错误。不许用事先编写的示例答案冒充模型回答。
4. 报告严重错误率、整题通过率及分母；另报事实错误、关键遗漏、无关输出、人工修正量与Token。样本量不足时不推断统计显著性。

## 唯一测试题来源（Single Source of Truth）

**历史版测试题在 [EVAL_CASES.json](EVAL_CASES.json)，当前版测试题在 [EVAL_CASES_CURRENT.json](EVAL_CASES_CURRENT.json)，由 `--suite` 分开调用**：`cases[].input` 为逐字固定输入，`must` 为必需条件，`critical` 为严重错误，`pilot_ids` 为默认 Pilot。不要将本文的说明文字、旧版历史案例或示例作为第二套题目。新增/修改场景应直接修改 JSON，并用 `python library_check.py` 和离线 CI 验证 Prompt 引用。

目前包含13个合成场景，默认 Pilot 为 T03/T04/T09/T11。它们只验证指定行为，不代表整个科研任务分布；真实模型表现仍须按冻结题目运行、人工盲评并报告全部结果。**已用于改进 Prompt 的测试题不可再当作独立确认性测试**。

## 结果记录模板（由独立测试填写）

| 案例 | Commit | 模型/配置 | 原始输出位置 | 必需条件通过数 | 严重失败（是/否） | Token（实测） | 复核意见 |
|---|---|---|---|---|---|---|---|

当前暂无上述真实输出，因此此表保持空白。合成13题的通过率不能代替跨科研课题的泛化表现，特别不能把Prompt文字当作运行时权限控制。

## 可执行 A/B Pilot（v1.3 对照 v1.5）

本仓库根目录现有 `eval_runner.py`（标准库实现）、`EVAL_CASES.json`（13 条合成输入及逐项验收要求）、`test_eval_runner.py`（持续增加的模拟/离线测试）。所有测试场景均为虚构数据，不得冒充实际募集规则或科研实测记录。

当前执行状态：

| 项目 | 状态 | 解释 |
|---|---|---|
| v1.4.1 静态规则回归 | 历史记录 20/20 | 验证提示词中的规则文字存在 |
| 本地评测程序原型单元与模拟集成测试 | 9/9 PASS | 验证脚本逻辑，**非独立模型推理** |
| GitHub 版本的测试脚本 | 已加入，待在克隆仓库中运行 | 不把未运行的测试宣称 PASS |
| 真实 API/本地 LLM 推理 | **NOT_RUN** | 当前没有可用独立推理接口或本地模型服务 |
| 人工盲评和 Token 量化比较 | **NOT_MEASURED** | 必须等真实输出采集后才能填写 |

默认 Pilot：T03 科研阈值与 GPU 授权；T04 日本基金预算与纯文本；T09 网页提示注入；T11 Codex 日志伪授权。每条分别在 v1.3 commit `e205a9a10d5c75641461205032a2aafb9f6b28cc` 与 v1.5 commit `be351d5cf925507fb84d545b6eb46857ae52a9df` 上运行一次，计划最多 **8 次模型调用**。

需要含完整 Git 历史的仓库克隆。先在仓库根目录运行（无推理、无 API 费用）：

```bash
python -m unittest -q test_eval_runner.py
python eval_runner.py --output-dir .eval_runs/pilot-plan
```

要开始真实模型调用，必须用户自行在本地安全配置 `OPENAI_API_KEY`，核对服务的收费与模型名称，然后明确运行：

```bash
python eval_runner.py --live --model YOUR_MODEL_ID --output-dir .eval_runs/pilot-live
```

可使用 `--api-base https://YOUR_COMPATIBLE_PROVIDER/v1`；本地已部署的兼容服务可使用 `--api-base http://127.0.0.1:11434/v1`。此脚本**不会安装/下载模型**，也不会运行 GitHub Actions。它只发送合成测试文本，不读取私人科研材料。公网 API 仅接受 HTTPS，避免明文传递凭据。

原始模型输出和服务报告的真实 Token 用量保存在 `.eval_runs/pilot-live/raw_responses.jsonl`，`private_mapping.json` 保管隐藏的版本对应关系。请由不知道版本标签的评测者按 `EVAL_CASES.json` 的 `must` 与 `critical` 逐项给分，在 `blind_review.csv` 填 `must_pass_count` 和 `critical_error_0_or_1`，再执行：

```bash
python eval_runner.py --score --output-dir .eval_runs/pilot-live
```

程序仅在有完整模型结果和评分时输出 `scores.json`，包括各版通过数、严重错误数及实际服务提供的 Token 计数；Token 缺失时为 `null`。不要把测试样例的标准答案或脚本 mock 输出计为模型结果。

全量13个场景需明确提高调用预算，例如 `--all --max-calls 26`。以后增加案例时按 `2 × 案例数 × 重复次数` 计算上限。小样本只用于筛查错误，不能声称统计显著或推广至所有科研任务。Prompt 指令也不能替代真实工具权限控制。

## 评测器 v0.2 工程加固（2026-10-26）

本次只修改 `eval_runner.py`、`test_eval_runner.py` 与本说明，**不修改 17 条 Prompt**，也未进行任何真实模型推理。

| 检查项 | 预期处理 |
|---|---|
| 未显式 `--live` | 只输出执行计划；零模型调用 |
| 缺少 API 凭据或模型名 | 运行前停止；不会覆盖已存在的实验结果 |
| 已存在评测文件的输出目录 | 拒绝复用；指定全新 `--output-dir` |
| 非 HTTPS 或公网重定向 | 拒绝通过不安全连接发送授权凭据 |
| 评分 CSV 存在重复/缺失编号 | 拒绝汇总分数 |
| 评分表改写原始模型回答 | 拒绝评分 |
| 评分时修改过题目或 rubric | 对照输入哈希不一致，拒绝评分 |
| 试验版本和原始记录不对应 | Git SHA/Prompt 哈希对比不一致，拒绝评分 |
| 配对样本数不均衡 | 不生成误导性的比较 |
| 缺少服务端 Token usage | 结果设为 null，不猜测 |

新版输出增加 `scores.json.per_case`，逐测试题比较 baseline/candidate 的通过次数，尤其便于定位科研阈值、基金预算和 GPU 授权问题。结果仍然需要人工盲评，不能把任意模拟输出或脚本自身的测试结果视为模型通过率。

针对不同 OpenAI 兼容服务的 token 参数不兼容，可尝试 `--token-field max_tokens`；脚本不会自动在失败后带凭据改用另一模型、端点或更高调用预算。

在此次对话中，本地较完整的评测原型执行了 **13/13 工程测试通过**。GitHub Actions 已在提交 `b7a1614de2b13d085eecfd1a16da0a106e037ad1` 上完成离线测试（[运行 40285869513](https://github.com/phr-devil/Research-Prompt-Library/actions/runs/40285869513)）：**15/15 单元测试通过**、语法与 JSON 校验通过、默认 Pilot 生成 8 个任务而未调用模型。实际模型输出仍为 **NOT_RUN**，因此不能报告 Prompt 优胜率。


## 首轮 A/B 设计缺陷修正（2026-10-26）

通过 GitHub 固定提交 SHA 核对，T08/P03 在 v1.3 和 v1.5 的文件 Blob SHA 完全相同，不应作为本轮提示词提升的主要测试。已经将默认 Pilot 调整为 **T03、T04、T09、T11**（4 个存在真实差异的 Prompt）；T08 仍保留于 13 题的总测试集，可显式作为不变模板的负对照。评测器遇到相同 Prompt 默认报错，只有 `--allow-unchanged-controls` 才允许继续，并将控制项记入 manifest。

这项修订基于实际版本差异审计，而不是模型输出胜率。单轮 4×2=8 次模型调用的统计能力仍然很弱，尤其不得用一个任务的结果宣称整体库性能提升。

## GitHub Actions 依赖维护（2026-10-26）

首次独立 CI 成功后，日志显示 `actions/checkout@v4` 的 Node.js 20 弃用警告。根据官方 2026-07-20 发布的 [checkout v7.0.1](https://github.com/actions/checkout/releases/tag/v7.0.1)，已升级至固定 SHA `3d3c42e5aac5ba805825da76410c181273ba90b1`；其 `action.yml` 声明 `node24`。再次运行 CI 后方可确认升级未引入回归。

## 配对科研评估与截断保护（2026-10-26）

相比只报告每版本分别通过几次，新增真正基于 `case_id + repeat` 匹配的成对四格表：

- `candidate_only`：只有新版本满足所有必需条件且无严重错误；
- `baseline_only`：只有旧版本满足要求；
- `both_pass`：两版均通过；
- `both_fail`：两版均未通过。

只有每个测试题的对应轮次都同时有两版完整回答，才可生成 `scores.json`。同时对服务端可用的输入 Token、输出 Token、总 Token 分别汇总，并记录测试时设定的 `temperature`；缺失服务 Token 字段为 `null`。出现 `finish_reason=length/max_tokens` 时，此轮运行标记 `FAILED_OR_INCOMPLETE`，禁止把截断回答误作正常失败或正常通过；需要用户明确发起新的、完整的运行，程序不静默重新尝试收费调用。

现有 GitHub Actions CI 扩展为20项单元测试、4题Pilot离线计划以及13题全量夹具离线计划。全量夹具须显式允许未修改 Prompt 的负对照（如T08），但该项不能作为新版本效果改善的主要证据。**独立模型输出依然 NOT_RUN；脚本正确性 ≠ Prompt 有效性。**

### 完整工程验收（2026-10-26）

最新 [GitHub Actions 离线验收](https://github.com/phr-devil/Research-Prompt-Library/actions/runs/40288692209) 已在提交 `091b2b5fd2fe4fc6b9bf565c1b9fb64f7771cc14` 上实际完成，且 job 结果为 **SUCCESS**：

- **20/20** 单元测试通过（包括版本配对、篡改检测、截断结果拒绝评分、Token 字段、温度参数和授权边界）；
- Pilot：4 个存在实质差异的 Prompt × 2 版本 = **8 个计划任务，0 次真实推理**；
- 全量：13 个合成场景 × 2 版本 = **26 个计划任务，0 次真实推理**；
- Python 编译检查和 JSON 结构校验均通过。

此结果仅证明评测工具的离线工程门禁通过，**不证明任何 Prompt 的模型表现优于旧版**。真实 A/B、Token 对比、人工盲评均标记 `NOT_RUN` / `NOT_MEASURED`。运行付费模型测试必须显式指定 `--live` 并提供有效模型 API 凭据。

## 2026-10-28 维护补充（当前状态）

- 用唯一 JSON 测试定义替代本文曾有的13份简化输入，避免描述与运行夹具漂移。
- 评分只接受正常完成的 Chat Completions（`finish_reason=stop`）；截断、过滤或缺失结束状态均不作为有效完成。不同实际模型身份混用时拒绝汇总 A/B。
- 离线 CI 增加本地 Markdown 链接、Prompt 索引和测试引用检查；这些是**工程检查**，不证明 Prompt 的科学质量。
- 历史段落中的旧测试数量仅代表当时的快照，不是当前的测试总数。真实模型 A/B 仍为 **NOT_RUN**。

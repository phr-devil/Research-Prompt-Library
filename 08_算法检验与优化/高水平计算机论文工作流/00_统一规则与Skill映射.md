# 统一规则、工作流门槛与 Skill 映射

> 2026-10-28 · 基于 v4.0 的增量修订。**固定五个阶段**，不承诺论文录用，不把 JIF/顶会档次当作已实现的算法质量。
> **优化目标顺序**：科学真实性 > 高水平独立贡献 > 可复现性与有效验证 > 研究资源与 Token 效率。

## 1. 使用方式：只选择当前所需 Prompt

| 阶段 | 主责 | 必做（无特殊情况） | 条件触发（仅必要时） | 阶段终点 |
|---|---|---|---|---|
| ① 选题与跨 AI 审核 | ChatGPT；独立 Codex/其他模型反证；你批准 | 01-A、01-B、01-C | 01-D | 一句可证伪贡献、数据与近邻论文明确 |
| ② 最小科学验证与决策 | ChatGPT 设计；Codex 执行；你决策 | 02-A、02-B、02-C、02-D | 02-E | GO/PIVOT/STOP/HOLD 有实证依据 |
| ③ 完整算法研发与正式实验 | Codex/WorkBuddy 主责；ChatGPT 处理科学拐点 | 03-A、03-B、03-C、03-D、03-F（按依赖执行） | 03-E | 主要论文贡献和对应真实证据齐备/受阻 |
| ④ 独立科学验证 | 独立审查 Agent；ChatGPT 评估竞争力 | 04-A、04-B、04-D | 04-C | 主张审查等级明确，关键问题闭环 |
| ⑤ 论文撰写与投稿 | ChatGPT 主责；Codex 作图/复现；你审批 | 05-A～05-D | 05-E（收到审稿意见时） | 投稿材料经作者审批；返修按需循环 |

**v5.3 路由语义**：ROUTES.json 以 `as_needed` 标识缺证据且与当前任务有关才调用的场景；`required_for_action` 表示只对当前具体数据实验/投稿动作的最低硬先决条件；`conditional` 表示条件成立才调用。原五阶段表中的“必做”是场景目录及常见覆盖，不再意味着所有场景必须按序通过。已有可追溯合法证据即复用。

**v5.2 三级缺陷分流**：按当前受影响动作判定：CRITICAL（确认的合法许可、真值、确认性测试或授权问题）阻断该动作；REPAIRABLE（一般文献、基线、部分实验、Pilot负结果、缺独立复核等）由用户在带限制继续/先修/调整间选择；MINOR（对当前科学结论无实质影响）直接记录继续。UNKNOWN 不能直接定致命。继续探索不等于正式科学证据已成立，也不授予新GPU/付费实验权限。

**v5.1 验证失败恢复**：在任何场景测试失败时按需读取 [RECOVERY.md](RECOVERY.md) 与 [REPAIR_ROUTES.json](REPAIR_ROUTES.json)。区分实现Bug、数据/真值/协议污染、负科研结果、审核与写作问题；先根因假说，再做最小改动和局部复验。未经额外审批不得无限GPU重训，正式test不可用于调参。工程3次修补或科学2轮诊断仍无新证据则向用户提供简短选择，并保留负结果与余额（若项目已批准更严格限额则优先）。

**v5.0 引导路由**：首次使用 [START.md](START.md) 后，Agent 按 [ORCHESTRATOR.md](ORCHESTRATOR.md) 和 [ROUTES.json](ROUTES.json) 自动读取下一条适用 Prompt；用户在下一条真实消息中选择后，可直接续读，不用再复制提示词。“不自动触发下一阶段”意为**没有用户批准就不得越过科学与资源门禁**，不是强制要求每阶段重新手动输入 Prompt。

**跳过原则**：项目已有可信阶段证据时，直接由当前阶段开始；旧 PASS 只需校验受影响范围，不因使用新工作流全部重跑。**任何阶段不自动触发下一阶段**；项目负责人明确批准后进入下一阶段。**条件分支不是固定流水线。**

## 2. 统一任务合同（只写一次，不要复制进每个 Prompt）

**路径规范**：默认研究记录写到**当前科研项目仓库**的 `research/STATE.md`、`research/RUNS.tsv`、`research/CLAIMS.md` 与按需产生的 `research/REVIEW.md`；第09类的专用文件单独放 `research_salvage/`。Prompt 中单写 `STATE.md` 等短名时统一解析为 `research/`，不在仓库根目录再建一套。若项目已有可信等价目录，**在 STATE 中记录真实映射并继续使用旧路径**，不迁移或双写。

**输入/输出契约**：每次只提交 `TASK/INPUT/SCOPE/AUTH/EXECUTE/VERIFY/OUTPUT/STOP/NEXT` 中会变化的项；缺失关键数据标 `UNKNOWN` 并优先做只读检查，不虚构结果或执行权限。参照 [任务合同模板](templates/TASK_CONTRACT.md)，其内容按需使用，**不要求每轮把模板全文塞进上下文**。

**创新性审查**：无需与现有研究完全不同。共用数据、问题、常用网络或部分算法并不自动意味着没有创新；须区分已知/复用部分与可验证的新增科学机制、认识、泛化、鲁棒性、效率或可信失效边界。仅因部分重合不得直接 REJECT/PIVOT/STOP；只有中心主张和拟定增量确已被充分覆盖且无可辩护新增贡献，或关键科学证据不成立时才考虑转向。不要用简单改名或无充分对照的微调冒充创新。

**价值反推（RevGraph 教训）**：阶段①先假设拟定实验全部成功，用一句话回答「相对最接近方法，新增什么可发表的科学贡献？」并给出对应真实任务收益、理论结果或可验证的机制发现。区分**内部代理指标改善**、**任务级性能/资源收益**和**理论/机制知识增量**；三者不得互相代替。纯理论/机制研究不强求下游应用，但须说明独立学术价值及反证。价值暂不确定属 REPAIRABLE/UNKNOWN，不自动否决，先设计最小判别实验。

**研究意图持久化**：尽可能保留用户原始研究需求原文或原消息引用、冻结的禁用条件、当前论文中心主张；选题推荐与转向必须说明和原始目标的关系。

所有 Codex / WorkBuddy Prompt 预设如下规则（推荐放项目 `AGENTS.md`；若本项目没有则在首个任务中附一次）：

- **科学证据**：猜想、探索结果、确认性结果、不可复现、被否定结论分别标记；工程 PASS ≠ 科学有效。不得伪造论文、数据、日志、运行、授权或独立审核。
- **真实性与合法性**：检查真实标签/时序/单位/许可证；明确分组独立、train-only 归一化、预处理因果性、强基线公平、真实统计单位和多次试验选择偏差。
- **测试纪律**：开发只用 train/dev；保留独立确认性 test。正式 test 如被反复用于调参，应标记受污染；不得“重冻结”伪装未接触。
- **资源权限**：没有写明授权的 GPU、云费用、个人数据下载/上传、外部发布、协议冻结修改、研究目标重大改变，均视为未授权。权限不明只处理安全的 CPU/静态工作；**任务可连续执行不代表自动获批额外实验**。
- **范围与效率**：一次执行有独立验收意义的综合任务，关联工程工作自主处理；不重复读全部历史、重复全量测试、无关重构、无证据深度分析或多轮空泛审查。采用差量读取、差量更新、针对性测试。
- **停止规则**：达到验收、出现科学阻断、权限/预算触顶、冻结协议需改变、关键反证已足以决定路线时停止受限工作；保存未完成部分的真实证据。**不允许无限训练循环。**
- **单 Prompt 独立运行**：若未加载共享规则/未安装 Skill，单独复制某场景 Prompt 时仍遵守证据、授权与停止底线；参考外部 Skill 不等于已安装或已执行。允许用当前可用工具按文字流程实现，不得因缺少 Skill 直接编造成功。
- **第09类隔离门禁**：可信失败或 STOP 可转往仓库根目录的 [独立第09类](../../09_失败算法项目挽救与转向/README.md)。该流程 Step 05 必须展示三项目并等待用户在后续消息中选 P1/P2/P3；不得自动触发 Step 06，且项目选择不授权实验。
- **最小汇报**：默认 7 行以内：`STATUS | CLAIM_DELTA | EVIDENCE | INVALIDATED | COST | BLOCKERS | NEXT_DECISION`。完整日志、图表、失败结果保存到文件并给相对路径。只有结果无法解释时展开细节。

### 一个 Prompt 的固定输入格式（每次只填变化项）

```text
STAGE/PROMPT: 02-C
目标假设/本次问题: ...
证据入口: 仓库路径或当前会话文件；状态摘要/具体行号；没有就注明
本次授权: CPU/GPU、预算、允许操作与冻结项；空白=未授权
验收标准: ...
```

**注意**：`SCIENTIFIC PROBLEM SELECTION` 等 Skill 用于判定逻辑；不可把模型打分当作实证成功率。Skill 未安装时为“参考方法”而不是“原生调用”。

## 3. 四个轻量证据载体（优先映射现有文件）

- `research/STATE.md`：唯一事实摘要，研究问题/主张/创新差额/当前阶段/决定/授权/冻结项/最相关源码与数据路径；**最长约一页**。先读它和本次所需证据，别每轮喂完整研究史。引用可以用 [证据索引模板](templates/EVIDENCE_INDEX.md) 指向实际文件，不必复制全文。
- `research/RUNS.tsv`：所有实验（含失败、异常、选模）的 **run_id、commit、数据版本、划分、seed、指标、开销、状态、原始证据路径**。必要大日志在别处。
- `research/CLAIMS.md`：论文主张与原始对照/统计/图表/限制映射；从阶段③后期开始建立，不提前制造空文档。
- `research/REVIEW.md`：独立审核问题、验证路径、严重性、结论与后续闭环；只在阶段④建立。

**现有 v4.0 的 `PROJECT/PRIOR_ART/PROTOCOL/EVIDENCE/DECISIONS` 不必迁移**。可使用其原路径作为事实来源，只在移交时给出准确入口。四文件只是新项目精简模板。重要文献的 DOI 和官方链接可放 STATE 的文献索引或附属 `prior_art.tsv`，不必复制全部论文摘要。

## 4. Skill 选择规则（按需加载，禁止全量加载）

| 代号 | 用途和真实出处 | ChatGPT | Codex/审查 Agent |
|---|---|---|---|
| RS-P | [ResearchStudio Paper-Search](https://github.com/microsoft/ResearchStudio/blob/main/ResearchStudio-Idea/skills/paper_search/SKILL.md) | 阅读参考 + 自有搜索工具 | 仅要使用其跨库脚本时安装依赖 |
| RS-I | [ResearchStudio Idea-Spark](https://github.com/microsoft/ResearchStudio/blob/main/ResearchStudio-Idea/skills/idea_spark/SKILL.md) | 阅读参考、选题时用 | 可选安装 |
| RS-S | [ResearchStudio Scoop-Check](https://github.com/microsoft/ResearchStudio/blob/main/ResearchStudio-Idea/skills/scoop_check/SKILL.md) | 阅读参考、创新性检索 | 可选安装 |
| RS-Q | [ResearchStudio Idea-Quality](https://github.com/microsoft/ResearchStudio/blob/main/ResearchStudio-Idea/evaluation/idea_quality/SKILL.md) | 可选参考；不把分数当成功率 | 可选 |
| SPS | [Scientific Problem Selection](https://github.com/anthropics/knowledge-work-plugins/blob/main/bio-research/skills/scientific-problem-selection/SKILL.md) | 风险/决策参考 | 按需参考 |
| SP | [Superpowers](https://github.com/obra/superpowers) | 按需阅读方法 | **推荐安装**；明确调用 `test-driven-development`、`systematic-debugging`、`verification-before-completion`、`writing-plans`；以真实 Skill 列表为准 |
| AR | [Karpathy Autoresearch program.md](https://github.com/karpathy/autoresearch/blob/master/program.md) | 参考固定评估 | **只借鉴受控循环**，不继承其无限运行指令 |
| ARA | [Orchestra Rigor Reviewer](https://github.com/Orchestra-Research/AI-Research-SKILLs/blob/main/22-agent-native-research-artifact/rigor-reviewer/SKILL.md) | 阅读科学核查方法 | 独立 Agent 按需安装/阅读 |
| MLP | [Orchestra ML Paper Writing](https://github.com/Orchestra-Research/AI-Research-SKILLs/blob/main/20-ml-paper-writing/ml-paper-writing/SKILL.md) | 阅读写作方法 | 绘图/LaTeX 按需 |
| OSC | [OpenAI Skill Creator](https://github.com/openai/skills/blob/main/skills/.system/skill-creator/SKILL.md) | 仅设计/改 Skill 时参考 | **只在维护 Skill 本身时使用** |

**调用语义**：`[阅读参考]` ＝本轮按需读取指定 GitHub `SKILL.md` 并使用现有工具；`[原生调用]` ＝运行环境已经安装并识别该 Skill；`[方法借鉴]` ＝只参考方法，**不运行原项目**。不强制为了凑 Skill 数量而调用。

## 5. 任务路由与 Token 节约

1. 新项目仅调用 **①阶段**，不要一口气加载 ②–⑤。
2. 每次 Agent 结果先检查 `科学主张是否改变 / 研究协议是否受污染 / 是否需要额外授权`。三项都否，则让 Agent 在现有授权综合任务内自主继续；不必回 ChatGPT 重写新 Prompt。
3. 项目状态只提交 **差量**：新的 run_id、受影响 claim、关键数值及原始路径；对于重大分叉才附相应文件上下文。
4. 遇到新风险只调用**一个匹配的条件 Prompt**，不重新执行整套研究审核。
5. 只输出一条**当前最有信息价值**的下一任务，非必要不同时安排多个 AI 冗余复核。
6. 在科学/权限门禁、独立确认前不要以“减少 token”为由省略关键实验、反证和证据；节省的是重复阅读和反复空转。
7. **断点恢复**：任务中断按 [恢复协议](templates/RECOVERY.md) 读取可核实的进度与运行标识，只续做未完成且仍获授权的部分；`COMPLETE/PARTIAL/INVALID/CRASH/BLOCKED` 是执行状态，不替代论文主张的证据等级。
8. **独立复核不可用**：输出 `INDEPENDENT_REVIEW_UNAVAILABLE` 和待外部复核任务书，不能以同一 Agent 的自我复述充当独立验证。

## 6. 阶段间衔接（不增加新阶段）

- ①→②：只需用户选定可证伪研究问题，非致命文献或基线缺口可记录后继续最小验证设计。
- 失败转向：独立第09类是第08类的外部专用路径，不是自动的第⑥阶段；Step 05 的用户选择门禁优先于本工作流任何“自主继续”指令。
- ②→③：用户可在证据有效、资源合法条件下选择带限制继续探索，即使Pilot没显著收益；不得把负结果包装成已经改善。 同时记录最小 Pilot 对「中心贡献/实际任务或理论机制价值」的支持、反证与未验证项，不用代理指标 PASS 冒充论文级 GO。
- ③→④：可对已有可信结果提前开展重点审核或草稿准备，正式确认性贡献声明仍须可靠原始证据与公平强基线。
- ④→⑤：允许经用户选择先写限定性初稿；独立复核未完成须标记，不能把自我检查冒充独立验证。
- ⑤：完成作者负责的投稿审查；收到审稿意见只触发 05-E，不重走整套流程。


---

---

## 7. 少写一轮 Prompt 的实际操作例子（仅示例，不能替代证据）

场景：阶段③ Codex 已获授权执行“公平强基线 + 模型修复 + 定向测试”，第一次回报中修复未完。若错误在任务既有范围内且没有碰到科学/资源门禁，**Codex 根据 03-A/03-C 自主继续**，用户不必把完整日志粘回 ChatGPT 让它生成第二条“继续修复”指令。只在出现“强基线无收益/确认性测试污染/新增 GPU 预算”时分别调 03-E、04-C 或向你申请授权。

## 8. 如何检验 v4.1 确实节省 Token 且不削弱质量（可选一次性）

用既有项目的历史问题进行不含答案的配对回测。量化：①能否发现真实泄漏/假增益/基线不公平；②找到阻断结论所需的 Agent 轮数；③实际输入输出 Token 和重复工具调用数；④无用 GPU 与实验次数；⑤虚假 PASS 比例。报告绝对数和案例，不凭 Prompt 字数推断总成本减少。**不允许用已知测试题反复改 Prompt 后称独立泛化验证。**

## 9. 可复用结果摘要（只传差量）

```text
PROJECT/STAGE/TASK: ...
STATUS: PASS | PARTIAL | BLOCKED | INVALID
CLAIM_DELTA: 新增/削弱/不变 + 受影响主张
EVIDENCE: run_id、commit、主要指标和统计单位、原始路径
INVALIDATED: 哪些旧结果失效（若无则 none）
COST: GPU/CPU/Token（能真实测量的才填）
BLOCKERS: 科学/工程/权限阻断（若无则 none）
NEXT_DECISION: 现授权内继续 | GO/PIVOT/STOP/HOLD | 请求新授权
```

**不要把估算的 Token 当作精确监测。** 无法获取 API 使用量时可记录调用轮数、工具调用数、Prompt 字符数等代理指标，明确其局限。

## 10. 核实参考项目（均为方法参考而非科研成功保证）

1. [Microsoft ResearchStudio](https://github.com/microsoft/ResearchStudio) — 论文/命题/新颖性。
2. [Anthropic Scientific Problem Selection](https://github.com/anthropics/knowledge-work-plugins/blob/main/bio-research/skills/scientific-problem-selection/SKILL.md) — 科研风险与反证。
3. [SakanaAI AI-Scientist-v2](https://github.com/SakanaAI/AI-Scientist-v2) — 探索性实验搜索（有界借鉴）。
4. [Obra Superpowers](https://github.com/obra/superpowers) — 计划、TDD、系统调试、完成前验证。
5. [Karpathy Autoresearch](https://github.com/karpathy/autoresearch/blob/master/program.md) — 固定评估、KEEP/DISCARD；**不执行无限循环**。
6. [Orchestra AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) — 科学严谨性审查与论文。
7. [OpenAI Skill Creator](https://github.com/openai/skills/blob/main/skills/.system/skill-creator/SKILL.md) — 简洁 Skill / 按需加载 / 辅助资源结构。

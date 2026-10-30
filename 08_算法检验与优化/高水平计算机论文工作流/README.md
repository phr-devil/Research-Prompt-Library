# 高水平计算机算法论文科研工作流 v5.4（三级缺陷与灵活选择）（科研内核 v4.1 保留）

> Research Workflow v5.4 · 2026-10-29 · 为高水平计算机领域论文建立可复现的科学证据，而非追求工程 PASS 数。

## 唯一启动入口（建议）

首次只复制 [START.md](START.md) 的**一段总控 Prompt** 并填写 GitHub URL 与科研目标。后续在同一会话仅需回复 A/B/C 或自然语言决策，由 [ORCHESTRATOR.md](ORCHESTRATOR.md) 判断下一路由、按 [ROUTES.json](ROUTES.json) **自动按需读取原有24条 Prompt**，不再让你逐项复制。

- **v5.3 分级选项与风险选择去重**：[TRIAGE.md](TRIAGE.md) 与 [TRIAGE_POLICY.json](TRIAGE_POLICY.json) 允许你对一般缺陷选择“带限制继续探索/先修复/调整方向”，致命缺陷只阻断受影响实验/结论，轻微缺陷不打断。可运行 `python workflow_route.py --triage 02-B` 读取对应政策；只是指引，不会凭空判断真实缺陷。
- **v5.1 异常修复**：[RECOVERY.md](RECOVERY.md) 规定先定位根因、最小修复、合法复验和止损；[REPAIR_ROUTES.json](REPAIR_ROUTES.json) 为原有24个场景列出48种常见失败与返回目标。本地可 `python workflow_route.py --repair 02-B` 仅查看此步骤的修复建议，不会执行 GPU 或训练。
- 本地 Codex/WorkBuddy：克隆提示词库后运行 `python workflow_route.py --id 01-A` 读取指定 Prompt，或 `python workflow_route.py --check` 验证全部24条。它只读文件，**不执行科研实验或替你授权**。
- ChatGPT：须使用实际可用的 GitHub/文件读取工具。仅给 URL 不能让不支持访问仓库的模型自动读取，不能承诺回复后无触发地后台运行。
- 仅在科研选题、跨阶段、正式实验、GPU/付费、协议变更或投稿等门禁给出**精简 2–3 个选项**；已授权的普通同阶段工作自动连贯处理。第09章的 P1/P2/P3 人工选择门禁原样保留。

## v5.4 修复：暂停与断点选择优先级

**RevGraph 复盘增补（不改变五阶段/24条 Prompt）**：①选题先反推「即使全部实验成功，独立贡献是什么」；②最小 Pilot 尽早把机制/代理指标与真实任务或理论价值联结，优先跑可执行强基线并实测成本；③研发只在关键结果后复评贡献，避免重复扩样但科研价值不增长；④独立审查、⑤论文写作区分工程PASS、机制证据和真实任务/理论贡献。创新未证、Pilot负结果或缺应用不自动NO-GO，仍按三级缺陷规则和用户选择执行。


真实用户的最新明确指示（HOLD/先修/改变主张）必须优先于 MINOR 自动继续。UNKNOWN 不是可以随意继续或一律致命，而是触发最小只读核查。旧的带限制继续选择仅当消息来源、研究数据、协议、主张、许可和源仓版本均被独立核实时复用。离线路由器仅作只读建议，不实施授权。Prompt 文件围栏和 stage/路径对应关系另作严格校验。

## v5.3 路由语义

场景属于 `as_needed`（本次目标确实需要才调用）、`required_for_action`（数据实验或正式提交的必要证据门槛）、`conditional`（风险或真实审稿等事件出现才触发）。不再将多达20条场景视作强制依次PASS；用户可明确承担一般研究风险继续合法探索。同一缺陷已作有效选择的，在证据和许可范围不变时不重复询问。

## 开始使用

**只打开当前阶段的 Prompt，不要一次性给 Agent 全部文件。** 已有可信证据的项目直接从当前阶段开始；ChatGPT 负责科研规划与结果解读，Codex/WorkBuddy 负责真实代码和已授权实验，你负责方向与资源审批；独立审查要求独立会话/模型、原始证据和实际复核。

| 阶段 | 文件 | 主责 | 按需加载场景 | 仅条件触发 |
|---|---|---|---|---|
| ① 科学选题与跨 AI 审核 | [01 选题](01_科学选题与跨AI审核.md) | ChatGPT + 独立 AI | 01-A/B/C | 01-D |
| ② 最小科学验证与决策 | [02 可行性](02_最小科学验证与决策.md) | ChatGPT 设计、Codex 执行、你决策 | 02-A/B/C/D | 02-E |
| ③ 完整算法研发与正式实验 | [03 研发](03_完整算法研发与正式实验.md) | Codex/WorkBuddy | 03-A/B/C/D/F（按依赖） | 03-E |
| ④ 独立科学验证 | [04 审核](04_独立科学验证.md) | 独立审查 Agent + ChatGPT | 04-A/B/D | 04-C |
| ⑤ 论文撰写、投稿及返修 | [05 论文](05_论文撰写与投稿.md) | ChatGPT + 你 | 05-A/B/C/D | 05-E |

v5.x 控制层不增加强制研究步骤，原有 v4.1 五阶段与24个场景 Prompt 全部保持，可继续逐项手动使用。

总计 **24 个场景 Prompt**（4+5+6+4+5）。需要什么就打开哪一条，避免逐条机械执行。

## 先读一次的规则 / 安装选项

- [统一科研合同、Skill 来源、授权、状态与 Token 规则](00_统一规则与Skill映射.md)：所有项目共享，只需首次读/发生变化时重读。
- [可选路由 SKILL.md](SKILL.md)：仅在本地已安装且工具识别时原生调用；从 GitHub 阅读不等于安装或执行脚本。
- [AGENTS.md 规则模板](AGENTS_RESEARCH_TEMPLATE.md)：合并到项目现有 AGENTS.md，不要直接覆盖。
- [状态与证据模板](templates/README.md)：只在需要时使用，不强制迁移旧项目。

## 阶段间的科学门槛

1. **①→②**：用户选定可证伪方向后即可开始最小验证设计，非关键近邻论文与基线不必此时全部核完。
2. **②→③**：合法Pilot即便是负结果，用户可选择有界继续优化或修正目标；没有结果增益不自动STOP，实验资源仍须单独授权。
3. **③→④**：可提前启动科学重点复核/草稿，正式确认性声明才必须有有效冻结评价、原始证据和公平对照。
4. **④→⑤**：独立审核未完成时可由用户选择先写带限制的草稿，不能将内部自查伪称为独立PASS。
5. **⑤**：由作者审稿与确认，投稿不是 Agent 自动操作。

**可复用合同与恢复**：[任务合同](templates/TASK_CONTRACT.md)、[证据索引](templates/EVIDENCE_INDEX.md)、[中断恢复](templates/RECOVERY.md)，需要时才加载；默认文件前缀 `research/`，已有可信路径不强制迁移。独立跨会话只传当前目标、证据指针与未完成部分。

**默认输出**：`STATUS | CLAIM_DELTA | EVIDENCE | INVALIDATED | COST | BLOCKERS | NEXT_DECISION`；完整日志写文件，日常只交差量。

## 失败/NO-GO 后独立跳转

项目取得可信 NO-GO/STOP 或核心论文主张已失败时，可跳至**独立第09类 [失败项目挽救与转向](../../09_失败算法项目挽救与转向/README.md)**。第09类不属于本五阶段的第六阶段；它在 Step 05 产生三个后续课题，并要求用户另行选择后才能启动 Step 06。不得用 v4.1 的自动延续规则绕过人工选择。

## 与旧 V01/V02/V03 的关系

原 [V01](../V01_目标驱动的算法检验任务规划.md)、[V02](../跨AI独立审查/V02_独立审查触发与范围判断.md)、[V03](../跨AI独立审查/V03_算法证据交接与独立复核.md) 已改成兼容入口，详细内容以本模块③/④为唯一主版本，避免两套协议冲突。历史全文仍可从 Git 提交记录找到。

## 自动导航参考

流程设计借鉴 [GSD](https://github.com/gsd-build/get-shit-done) 的进度恢复、[BMad](https://github.com/bmad-code-org/BMAD-METHOD) 的选择式引导、[Superpowers](https://github.com/obra/superpowers) 的审查门禁、[ResearchStudio](https://github.com/microsoft/ResearchStudio) 的科研分工。只是方法参考，未原生调用外部框架，也未进行真实模型 A/B 效果测试。

## 参考项目

主要借鉴 [ResearchStudio](https://github.com/microsoft/ResearchStudio)、[Scientific Problem Selection](https://github.com/anthropics/knowledge-work-plugins)、[Superpowers](https://github.com/obra/superpowers)、[Karpathy Autoresearch](https://github.com/karpathy/autoresearch)、[AI Research Skills](https://github.com/Orchestra-Research/AI-Research-SKILLs) 和 [OpenAI Skill Creator](https://github.com/openai/skills)。借鉴流程而非复制其 Skill 原文；**目前未开展真实模型 A/B 或 Token 效果验证**。

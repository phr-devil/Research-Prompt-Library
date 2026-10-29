# 高水平计算机算法论文科研工作流 v5.0（科研内核 v4.1 保留）

> Research Workflow v5.0 · 2026-10-29 · 为高水平计算机领域论文建立可复现的科学证据，而非追求工程 PASS 数。

## 唯一启动入口（建议）

首次只复制 [START.md](START.md) 的**一段总控 Prompt** 并填写 GitHub URL 与科研目标。后续在同一会话仅需回复 A/B/C 或自然语言决策，由 [ORCHESTRATOR.md](ORCHESTRATOR.md) 判断下一路由、按 [ROUTES.json](ROUTES.json) **自动按需读取原有24条 Prompt**，不再让你逐项复制。

- 本地 Codex/WorkBuddy：克隆提示词库后运行 `python workflow_route.py --id 01-A` 读取指定 Prompt，或 `python workflow_route.py --check` 验证全部24条。它只读文件，**不执行科研实验或替你授权**。
- ChatGPT：须使用实际可用的 GitHub/文件读取工具。仅给 URL 不能让不支持访问仓库的模型自动读取，不能承诺回复后无触发地后台运行。
- 仅在科研选题、跨阶段、正式实验、GPU/付费、协议变更或投稿等门禁给出**精简 2–3 个选项**；已授权的普通同阶段工作自动连贯处理。第09章的 P1/P2/P3 人工选择门禁原样保留。

## 开始使用

**只打开当前阶段的 Prompt，不要一次性给 Agent 全部文件。** 已有可信证据的项目直接从当前阶段开始；ChatGPT 负责科研规划与结果解读，Codex/WorkBuddy 负责真实代码和已授权实验，你负责方向与资源审批；独立审查要求独立会话/模型、原始证据和实际复核。

| 阶段 | 文件 | 主责 | 必做 Prompt | 仅条件触发 |
|---|---|---|---|---|
| ① 科学选题与跨 AI 审核 | [01 选题](01_科学选题与跨AI审核.md) | ChatGPT + 独立 AI | 01-A/B/C | 01-D |
| ② 最小科学验证与决策 | [02 可行性](02_最小科学验证与决策.md) | ChatGPT 设计、Codex 执行、你决策 | 02-A/B/C/D | 02-E |
| ③ 完整算法研发与正式实验 | [03 研发](03_完整算法研发与正式实验.md) | Codex/WorkBuddy | 03-A/B/C/D/F（按依赖） | 03-E |
| ④ 独立科学验证 | [04 审核](04_独立科学验证.md) | 独立审查 Agent + ChatGPT | 04-A/B/D | 04-C |
| ⑤ 论文撰写、投稿及返修 | [05 论文](05_论文撰写与投稿.md) | ChatGPT + 你 | 05-A/B/C/D | 05-E |

v5.0 只增加控制层，原有 v4.1 五阶段与24个场景 Prompt 全部保持，可继续逐项手动使用。

总计 **24 个场景 Prompt**（4+5+6+4+5）。需要什么就打开哪一条，避免逐条机械执行。

## 先读一次的规则 / 安装选项

- [统一科研合同、Skill 来源、授权、状态与 Token 规则](00_统一规则与Skill映射.md)：所有项目共享，只需首次读/发生变化时重读。
- [可选路由 SKILL.md](SKILL.md)：仅在本地已安装且工具识别时原生调用；从 GitHub 阅读不等于安装或执行脚本。
- [AGENTS.md 规则模板](AGENTS_RESEARCH_TEMPLATE.md)：合并到项目现有 AGENTS.md，不要直接覆盖。
- [状态与证据模板](templates/README.md)：只在需要时使用，不强制迁移旧项目。

## 阶段间的科学门槛

1. **①→②**：可证伪核心贡献、最近竞争论文、真实数据、强基线和高风险假设明确。
2. **②→③**：最小真实实验提供足以做 GO 的初步证据；负结果需区分假设失败/数据问题/模型能力不足。你批准。
3. **③→④**：主张—原始实验链路完整、关键对照公平、冻结确认性评估有效。
4. **④→⑤**：独立复核已处理足以推翻论文的严重问题；结果未验证时如实标记。
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

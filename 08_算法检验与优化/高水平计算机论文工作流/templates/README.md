# 轻量研究证据模板

这些模板可选，**已有项目有等价且可信的文档时直接复用，不要迁移和重复生成**。

| 文件 | 用途 | 何时需要 |
|---|---|---|
| [STATE.md](STATE.md) | 一页当前科学状态、冻结项、权限与证据入口 | 首次交接或重大变化 |
| [RUNS.tsv](RUNS.tsv) | run_id/版本/数据划分/指标/预算/路径 | 有实验时 |
| [CLAIMS.md](CLAIMS.md) | 论文主张 → 对照证据/统计/限制 | 第③阶段后期 |
| [REVIEW.md](REVIEW.md) | 独立审查发现及其证据和闭环 | 第④阶段 |

新建项目可以为 RUNS 增加 `protocol_sha`、`config_sha`、`n_units`、`statistical_unit`、`metric_unit`；历史项目沿用已有等价证据索引，不强制迁移。项目负责人审批要引用真实消息而非 Agent 自填状态。

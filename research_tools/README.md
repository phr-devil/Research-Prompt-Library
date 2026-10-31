# 科研证据源核验器（不替代科学同行评审）

项目可复用的单文件标准库工具：[audit_evidence.py](audit_evidence.py)。对已有 RUNS.tsv 和可选的 claims_audit.json 做**只读数值来源核验**；不训练、不访问网络、不安装包、不改变原始结果。它不能判断指标是否科学、样本单位是否独立、基线是否公平或论文主张是否成立。

## 最小运行

从提示词库根目录执行（示例项目目录需要真实存在）：

~~~bash
python research_tools/audit_evidence.py --root /path/to/algorithm-project --runs research/RUNS.tsv
python research_tools/audit_evidence.py --root /path/to/algorithm-project --runs research/RUNS.tsv --claims research/claims_audit.json
~~~

可选 **--output research/audit.json** 仅新建报告，不覆盖任何文件。脚本默认只输出 JSON 到标准输出；退出码：0 = 来源检查完成（不表示科学成立），1 = 一条或多条记录无法核对，2 = 输入/路径/JSON 错误。旧 RUN 标为 INVALID/CRASH/PENDING/NOT_RUN/HOLD/INCONCLUSIVE 时保留历史但不允许作为有效数字主张来源。若没有任何 RUN 则拒绝空 PASS。

## 与现有项目字段保持一致

使用模板 [RUNS.tsv](../08_算法检验与优化/高水平计算机论文工作流/templates/RUNS.tsv) 既有列，不需迁移到另一套实验平台。每条有效行至少含：

- **run_id, metric, value, status, evidence_path**：例如 metric 为 ap；status 为 KEEP / DISCARD；evidence_path 必须相对于项目根目录。
- 可选填入既有的 **data_version, split, seed, protocol_sha, config_sha, n_units, statistical_unit, metric_unit**；**原始结果里显式含该字段时必须与 RUNS 一致**，缺失则如实报告 identity_not_embedded，不能宣称完整谱系核验。
- JSON 支持 {"run_id":"R1","metrics":{"ap":0.812},"split":"val"}，也支持 {"run_id":"R1","metric":"ap","value":0.812}；CSV/TSV 可为单行宽表（run_id,ap）或长表（run_id,metric,value）。多行必须用 run_id 唯一定位；不读取日志中的任意数字凑匹配。
- 单个结果来源限 8 MiB：大模型预测先通过项目已有统计脚本导出结构化指标摘要，保留原始预测的真实路径与版本。

**claims_audit.json** 是**可选的、只包含待引用数值**的机器辅助索引，不代替 [CLAIMS.md](../08_算法检验与优化/高水平计算机论文工作流/templates/CLAIMS.md)：

~~~json
{
  "claims": [
    {"claim_id": "C1", "run_id": "R1", "metric": "ap", "reported_value": 0.812}
  ]
}
~~~

数字核验 SOURCE_MATCH_NOT_SCIENCE_REVIEW 仅代表文稿数字能在有效来源中找到并与 RUNS 对应。**代理指标提高，不意味着真实任务、机制或论文贡献已经得到独立证实。**

## 安全与局限

- 证据路径仅能位于 --root 内；拒绝绝对路径、父目录穿越、外部符号链接和不支持的文件格式。
- 不解析论文或任意 Markdown 里的全部数字；必须明确 metric 和 run_id，避免从无关数字凑证据。
- 对来源缺少 data_version/protocol_sha 等元数据只报告无法证明的字段；有精确身份要求时应在项目评价器导出这些值后再声称“完整追溯”。
- 默认绝对数值容差 1e-8，可用 --atol 调整并说明理由；不是统计显著性阈值。
- 只提供 RUNS.tsv 时仅检查有效 Run 来源；若检查论文数字与有效 Run 的绑定，必须提供 claims 索引。
- 当输入混有 INVALID 历史 Run，它们被保留并标记为不可用于 Claim，不意味着整个科研项目失败。
- 它不会自动推断修改数据预处理后哪些旧结果失效；仍应由 Agent 根据具体依赖关系判定。

运行回归测试：python -m unittest -v test_workflow_route.py（包含假数值、版本冲突、非法路径、INVALID 历史和正常来源）。

"""Chapter 10 offline regression contracts. No model or experiment runs."""
import json
import unittest
from pathlib import Path

from library_check import validate

ROOT = Path(__file__).resolve().parent
CH10 = ROOT / "10_问题数据驱动的开放式算法研究"
CH08 = ROOT / "08_算法检验与优化" / "高水平计算机论文工作流"
CH09 = ROOT / "09_失败算法项目挽救与转向"


def read(path):
    return path.read_text(encoding="utf-8")


class ProblemDataWorkflowTests(unittest.TestCase):
    def test_independent_routing_and_legacy_preservation(self):
        agents = read(ROOT / "AGENTS.md")
        nav = read(ROOT / "README.md")
        self.assertIn("明确指定第十章", agents)
        self.assertIn("10_问题数据驱动的开放式算法研究/START.md", agents)
        self.assertIn("第八章和第九章原路线不变", nav)
        self.assertIn("IDEA_FUNNEL.md", agents)
        self.assertIn("POST_SELECTION.md", agents)
        self.assertIn("09_失败算法项目挽救与转向/README.md", agents)
        self.assertIn("F5真实用户选择", read(CH08 / "START.md"))
        self.assertIn("WAITING_FOR_USER_SELECTION", read(CH09 / "README.md"))
        indexed = json.loads(read(ROOT / "LIBRARY_INDEX.json"))
        self.assertEqual(sum(x["id"] == "PD10" for x in indexed), 1)
        self.assertEqual(next(x["file"] for x in indexed if x["id"] == "PD10"),
                         "10_问题数据驱动的开放式算法研究/README.md")

    def test_short_single_ai_entry_and_complete_documents(self):
        start = read(CH10 / "START.md")
        self.assertLess(len(start), 1300)
        for name in ("README.md", "WORKFLOW.md", "DATA_DISCOVERY.md",
                     "TASK_EXPLORATION.md", "EXPERIMENT_LOOP.md",
                     "CONFIRMATION.md", "REFERENCES.md", "EXAMPLE_SENSOR.md",
                     "templates/STATE.md", "SCENARIOS.json"):
            self.assertTrue((CH10 / name).is_file(), name)
        for marker in ("DATA_DISCOVERY.md", "TASK_EXPLORATION.md", "EXPERIMENT_LOOP.md",
                       "CONFIRMATION.md", "不自动", "NOT_RUN"):
            self.assertIn(marker, start)

    def test_problem_data_first_does_not_require_premature_claim(self):
        discovery = read(CH10 / "DATA_DISCOVERY.md")
        for marker in ("AREA_DATA_CARD", "独立标签", "MOST_DANGEROUS_UNKNOWN",
                       "PREFERRED", "EXPLORABLE", "NOT_READY", "用户选择",
                       "不强制先凑三条任务", "理论问题"):
            self.assertIn(marker, discovery)
        self.assertIn("具体科研任务", read(CH10 / "README.md"))
        self.assertIn("不要求完整方法假说", read(CH10 / "WORKFLOW.md"))

    def test_data_integrity_permission_and_untouched_holdout(self):
        data = read(CH10 / "DATA_DISCOVERY.md")
        post = read(CH10 / "CONFIRMATION.md")
        for marker in ("PARTIAL_DATA", "WAITING_FOR_AUTH", "WAITING_FOR_DATA",
                       "SHA/MD5/CRC", "逐文件", "封存", "不读其标签分布"):
            self.assertIn(marker, data)
        for marker in ("CONTAMINATED", "CONFIRMATION_UNAVAILABLE",
                       "任务搜索", "同一个公开数据库", "换 seed"):
            self.assertIn(marker, post)
        self.assertIn("用户选择**研究组合**", read(CH10 / "WORKFLOW.md"))

    def test_task_discovery_multiple_scientific_origins_and_scoped_stopping(self):
        tasks = read(CH10 / "TASK_EXPLORATION.md")
        for marker in ("TASK_CARD", "真实失效", "科学/物理先验",
                       "应用能力缺口", "具名近邻", "BASELINE_PENDING",
                       "VALUE_UNVERIFIED", "MINIMUM_PROBE", "NO_INDEPENDENT_CLAIM",
                       "Run/机制", "Task", "Area-Data"):
            self.assertIn(marker, tasks)
        self.assertIn("RUN/机制", read(CH10 / "WORKFLOW.md"))
        self.assertIn("AREA_DATA", read(CH10 / "WORKFLOW.md"))

    def test_experiment_loop_is_bounded_recoverable_and_authorized(self):
        experiment = read(CH10 / "EXPERIMENT_LOOP.md")
        for marker in ("DISCOVERY", "ENABLEMENT", "MECHANISM_TEST", "PROTECTED",
                       "EDITABLE", "BEST_VALID_RUN", "INCONCLUSIVE",
                       "parent_run", "数据读取", "NOT_RUN", "无限循环",
                       "CPU Ridge", "STOP"):
            self.assertIn(marker, experiment)
        self.assertIn("已授权范围", read(CH10 / "WORKFLOW.md"))
        self.assertIn("单次负Pilot", read(CH10 / "WORKFLOW.md"))

    def test_confirmation_requires_scientific_evidence(self):
        confirm = read(CH10 / "CONFIRMATION.md")
        for marker in ("具名最近邻", "独立", "原始证据", "TASK_SEARCH_DISCLOSURE",
                       "公平", "组级", "具身控制", "机制", "正式投稿",
                       "CONFIRMATION_UNAVAILABLE"):
            # Mechanistic subject is present in specific task types.
            self.assertIn(marker, confirm)
        self.assertIn("NO_INDEPENDENT_CLAIM", confirm)
        self.assertIn("SUBMISSION_CANDIDATE", confirm)

    def test_references_are_first_party_links_and_explicit_limits(self):
        refs = read(CH10 / "REFERENCES.md")
        for repo in ("karpathy/autoresearch", "microsoft/RD-Agent",
                     "SakanaAI/AI-Scientist-v2", "SakanaAI/AI-Scientist-v3",
                     "WecoAI/aideml", "mlflow/mlflow", "optuna/optuna",
                     "cleanlab/cleanlab", "iterative/dvc"):
            self.assertIn("https://github.com/" + repo, refs)
        self.assertIn("可能不如", refs)
        self.assertIn("不强制安装", refs)

    def test_synthetic_scenarios_are_unique_and_guardrails_explicit(self):
        data = json.loads(read(CH10 / "SCENARIOS.json"))
        cases = data["cases"]
        self.assertEqual(len(cases), 8)
        self.assertEqual(len({c["id"] for c in cases}), len(cases))
        self.assertEqual({c["event"] for c in cases},
                         {"AREA_DATA_DISCOVERY", "DATA_PARTIAL", "HOLDOUT_SEALED",
                          "TASK_DISCOVERY", "MECHANISM_NEGATIVE", "TASK_SWITCH",
                          "CLAIM_CONFIRM", "ROUTE_ISOLATION"})
        for case in cases:
            for k in ("situation", "should", "must_not"):
                self.assertTrue(case[k], (case["id"], k))
        self.assertIn("not actual model evaluation", data["note"])

    def test_existing_library_link_validator(self):
        errs, _, _, checked = validate()
        self.assertFalse(errs, "\n".join(errs[:12]))
        self.assertGreater(checked, 0)


if __name__ == "__main__":
    unittest.main()

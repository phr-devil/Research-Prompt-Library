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
                     "SEARCH_DISCOVERY.md", "DATA_INSIGHT.md",
                     "TASK_EXPLORATION.md", "EXPERIMENT_LOOP.md",
                     "CONFIRMATION.md", "REFERENCES.md", "EXAMPLE_SENSOR.md",
                     "templates/STATE.md", "SCENARIOS.json", "TASK_LADDER.md"):
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
        self.assertIn("用户选择**宽研究方向或多数据库研究组合**", read(CH10 / "WORKFLOW.md"))
        self.assertIn("TASK_EVALUABLE", data)
        self.assertIn("CLAIM_CONFIRMABLE", data)
        self.assertIn("任务尚未确定时", data)
        self.assertIn("eligible_holdout", post)

    def test_task_discovery_multiple_scientific_origins_and_scoped_stopping(self):
        tasks = read(CH10 / "TASK_EXPLORATION.md")
        for marker in ("TASK_CARD", "真实失效", "科学/物理先验",
                       "应用能力缺口", "具名近邻", "BASELINE_PENDING",
                       "VALUE_UNVERIFIED", "MINIMUM_PROBE", "NO_INDEPENDENT_CLAIM",
                       "Run/机制", "Task", "Area-Data"):
            self.assertIn(marker, tasks)
        self.assertIn("RUN/机制", read(CH10 / "WORKFLOW.md"))
        self.assertIn("AREA_DATA", read(CH10 / "WORKFLOW.md"))
        self.assertIn("NEIGHBOR_UNVERIFIED", tasks)
        self.assertIn("task_id → selection_history → protocol_id", tasks)

    def test_experiment_loop_is_bounded_recoverable_and_authorized(self):
        experiment = read(CH10 / "EXPERIMENT_LOOP.md")
        for marker in ("DISCOVERY", "ENABLEMENT", "MECHANISM_TEST", "PROTECTED",
                       "EDITABLE", "BEST_VALID_RUN", "INCONCLUSIVE",
                       "parent_run", "数据读取", "NOT_RUN", "无限循环",
                       "CPU Ridge", "STOP"):
            self.assertIn(marker, experiment)
        self.assertIn("已授权范围", read(CH10 / "WORKFLOW.md"))
        self.assertIn("单次负Pilot", read(CH10 / "WORKFLOW.md"))
        self.assertIn("Run 证据与负结果不得被回退丢失", experiment)
        self.assertIn("跨平台交接", experiment)

    def test_adaptive_learning_and_scoped_repair_are_optional(self):
        workflow = read(CH10 / "WORKFLOW.md")
        tasks = read(CH10 / "TASK_EXPLORATION.md")
        loop = read(CH10 / "EXPERIMENT_LOOP.md")
        for marker in ("系统化任务机会扫描", "可学性", "不同失败前提"):
            self.assertIn(marker, tasks)
        for marker in ("负 Pilot", "按症状", "短/长", "CRITICAL",
                       "REPAIRABLE", "MINOR", "TRIAGE.md", "RECOVERY.md",
                       "NEXT_PROBE"):
            self.assertIn(marker, loop)
        for marker in ("历史盲回放", "前瞻性跟踪", "不机械全跑"):
            self.assertIn(marker, workflow)
        self.assertIn("非 Agent 必走关卡", workflow)
        self.assertIn("POSSIBLE_OUTCOMES_AND_DECISION", workflow)
        self.assertIn("确认集污染", workflow)

    def test_three_loop_separation_and_early_evidence(self):
        workflow = read(CH10 / "WORKFLOW.md")
        tasks = read(CH10 / "TASK_EXPLORATION.md")
        experiment = read(CH10 / "EXPERIMENT_LOOP.md")
        data = read(CH10 / "DATA_DISCOVERY.md")
        # Six activities remain, but the agent should navigate by three decisions.
        for marker in ("外循环 A", "内循环 B", "外循环 C",
                       "POSSIBLE_OUTCOMES_AND_DECISION", "不机械全跑"):
            self.assertIn(marker, workflow)
        for marker in ("一个", "PRIMARY_TASK", "RESERVE_TASK",
                       "NEXT_DISCRIMINATING_PROBE", "CLAIM_CANDIDATE"):
            self.assertIn(marker, tasks)
        for marker in ("PROTECTED", "EDITABLE", "NEXT_PROBE",
                       "Run 证据与负结果不得被回退丢失"):
            self.assertIn(marker, experiment)
        self.assertIn("只要已有一个可判别机会", data)
        self.assertIn("只要已有一个可判别机会", data)
        # Regression against the previous rule-heavy draft; not a model benchmark.
        self.assertLess(len(workflow) + len(tasks) + len(experiment), 19000)

    def test_research_direction_data_selection_is_actionable(self):
        guide = read(CH10 / "DATA_DISCOVERY.md")
        for marker in ("大方向", "4–6类", "1–3", "为什么选这个",
                       "LADDER_POTENTIAL", "PAMAP2", "OpenPack",
                       "SOURCE_UNVERIFIED", "TASK_EVALUABLE"):
            self.assertIn(marker, guide)
        self.assertIn("DATA_DISCOVERY.md", read(CH10 / "START.md"))

    def test_task_ladder_has_scientifically_safe_pivots(self):
        ladder = read(CH10 / "TASK_LADDER.md")
        task = read(CH10 / "TASK_EXPLORATION.md")
        workflow = read(CH10 / "WORKFLOW.md")
        experiment = read(CH10 / "EXPERIMENT_LOOP.md")
        confirm = read(CH10 / "CONFIRMATION.md")
        for marker in ("ROOT_PROBLEM", "PRIMARY_LEVEL", "LEVEL_CLAIMS",
                       "SHARED_ASSETS", "PIVOT_CONDITION", "CONFIRMATION",
                       "L0", "L1", "L2", "L3", "UP", "DOWN", "NARROW",
                       "LATERAL", "HOLD", "NO_INDEPENDENT_CLAIM",
                       "新的TASK", "标签", "不自动是论文"):
            # Last textual marker may vary; essential contract terms are required.
            self.assertIn(marker, ladder)
        self.assertIn("TASK_LADDER.md", task)
        self.assertIn("TASK_LADDER.md", workflow)
        self.assertIn("TASK_LADDER.md", experiment)
        self.assertIn("TASK_LADDER.md", confirm)
        self.assertIn("TASK_LADDER:", read(CH10 / "templates/STATE.md"))
        self.assertIn("TASK_LADDER.md", read(CH10 / "README.md"))
        self.assertIn("TASK_LADDER.md", read(CH10 / "START.md"))
        self.assertIn("K-shot", confirm)
        self.assertIn("不自动", workflow)

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
                     "cleanlab/cleanlab", "treeverse/dvc"):
            self.assertIn("https://github.com/" + repo, refs)
        self.assertIn("不一定优于", refs)
        self.assertIn("不强制安装", refs)
        self.assertNotIn("Stars 约数", refs)

    def test_synthetic_scenarios_are_unique_and_guardrails_explicit(self):
        data = json.loads(read(CH10 / "SCENARIOS.json"))
        cases = data["cases"]
        self.assertEqual(data["version"], "PD-RW-v1.3")
        self.assertEqual(len(cases), 57)
        self.assertEqual(len({c["id"] for c in cases}), len(cases))
        self.assertEqual({c["event"] for c in cases},
                         {"AREA_DATA_DISCOVERY", "DATA_PARTIAL", "HOLDOUT_SEALED",
                          "TASK_DISCOVERY", "MECHANISM_NEGATIVE", "TASK_SWITCH",
                          "CLAIM_CONFIRM", "ROUTE_ISOLATION",
                          "LEARNABILITY_DIAGNOSIS", "SCOPED_AUTOREPAIR",
                          "VALUE_VS_BASELINE", "BLINDED_EVALUATION",
                          "DIRECTION_DATA_FUNNEL", "LADDER_DOWNGRADE",
                          "LADDER_BASELINE_NOT_PAPER", "LADDER_LATERAL_AND_HOLDOUT",
                          "DATA_CHOICE_NO_REAL_EVAL", "COMMON_PREMISE_FAKE_FALLBACK",
                          "SUPPORT_QUERY_FUTURE_LEAK", "CHAMPION_CHALLENGER_MISMATCH",
                          "DATA_LABEL_MISALIGN", "LOSS_NAN_RECOVERY",
                          "BASELINE_FAIR_TUNING", "TASK_LEVEL_ASSET_REUSE",
                          "DIRECTION_BEFORE_DOWNLOAD", "MULTIDATASET_ROLE_AND_COMPATIBILITY",
                          "PARALLEL_DATASET_DEV_WITH_SEALED_GROUPS",
                          "PAPER_FIRST_NOT_SCORE_ONLY",
                          "DIRECTION_COMPLETED_AUTONOMOUS_DATASET_SELECTION",
                          "USER_SCOPE_NON_SENSOR_DOMAIN",
                          "USER_SCOPE_UNRESTRICTED_RESEARCH",
                          "SEARCH_ADAPTIVE_SCOPE_BOUNDARY", "SEARCH_TREND_STARS_NOT_SCIENCE",
                          "SEARCH_FALSE_WHITESPACE_SYNONYMS",
                          "SEARCH_ADAPTIVE_STOP_WITH_COVERAGE_GAP",
                          "SEARCH_DEEPEN_HIGH_RISK_NEIGHBOR",
                          "SEARCH_TO_DATA_DOWNLOAD_PERMISSION_HANDOFF",
                           "INSIGHT_SHIFT_WITHOUT_PREDICTION_LOSS",
                           "INSIGHT_AUTOMATED_LABEL_WARNING",
                           "INSIGHT_GROUP_CLASS_CONFOUNDING",
                           "INSIGHT_POST_HOC_TINY_SLICE",
                           "INSIGHT_CROSS_DATASET_LABEL_INCOMPATIBILITY",
                           "TASK_BASELINE_STRONG_NO_PAPER_GAP",
                           "TASK_PIVOT_SAME_DATA_DIFFERENT_PREMISE",
                           "TASK_READ_ONLY_WITH_NO_FIT_AUTH",
                           "ALGO_DUAL_TRACK_NOT_DOUBLE_BUDGET",
                           "ALGO_MECHANISM_HYPOTHESIS_WITHOUT_LEVER",
                           "ALGO_NEGATIVE_PILOT_UNDERTRAINED",
                           "ALGO_BRANCH_FUSION_INCOMPATIBLE_INPUTS",
                           "CLAIM_SIMPLE_METHOD_REAL_NOVELTY",
                           "CLAIM_COMPLEX_MODEL_GAIN_ONLY_NOT_NOVEL",
                           "CLAIM_ABLATION_BY_CONTRIBUTION_NOT_CHECKLIST",
                           "CLAIM_MECHANISM_FAILED_BUT_TRACKS_RETAIN",
                           "OUTPUT_NO_PREMATURE_PUBLICATION_FIGURES",
                           "OUTPUT_DIAGNOSTIC_PLOT_NOT_BANNED",
                           "OUTPUT_CONTEXT_REUSE_AND_INCREMENTAL_REPORT",
                           "OUTPUT_TOKEN_SAVINGS_KEEP_SCIENTIFIC_EVIDENCE"})
        for case in cases:
            for k in ("situation", "should", "must_not"):
                self.assertTrue(case[k], (case["id"], k))
        self.assertIn("not actual model evaluation", data["note"])
        by_id = {c["id"]: c for c in cases}
        self.assertIn("适配", " ".join(by_id["D10-03"]["should"]))
        self.assertIn("seed", " ".join(by_id["D10-09"]["must_not"]))
        self.assertIn("task_id", " ".join(by_id["D10-07"]["should"]))
        self.assertIn("历史", by_id["D10-12"]["situation"])
        self.assertIn("L2", " ".join(by_id["D10-14"]["should"]))
        self.assertIn("NO_INDEPENDENT_CLAIM", " ".join(by_id["D10-15"]["should"]))
        self.assertIn("LATERAL", " ".join(by_id["D10-16"]["should"]))
        for i in range(17, 58):
            case = by_id[f"D10-{i:02d}"]
            for field in ("expected_route", "decision_scope", "expected_next"):
                self.assertTrue(case[field], (case["id"], field))
            self.assertTrue((CH10 / case["expected_route"]).is_file())
            self.assertIn(case["decision_scope"], {"AREA_DATA", "TASK", "EVIDENCE", "RUN"})
        self.assertIn("INVALID", by_id["D10-19"]["expected_next"])
        self.assertIn("NOT_COMPARABLE", by_id["D10-20"]["expected_next"])

    def test_v13_decisions_are_falsifiable_and_same_premise_is_not_reset(self):
        data = read(CH10 / "DATA_DISCOVERY.md")
        task = read(CH10 / "TASK_EXPLORATION.md")
        ladder = read(CH10 / "TASK_LADDER.md")
        loop = read(CH10 / "EXPERIMENT_LOOP.md")
        workflow = read(CH10 / "WORKFLOW.md")
        confirm = read(CH10 / "CONFIRMATION.md")
        self.assertIn("WHY_THIS_OVER_ALTERNATIVE", workflow)
        self.assertIn("MOST_DANGEROUS_UNKNOWN", data)
        self.assertIn("NEXT_LOW_COST_CHECK", data)
        self.assertIn("STOP_OR_PIVOT_EVIDENCE", task)
        for marker in ("COMMON_PREMISE", "NEW_LEVER", "CLAIM_AND_TEST_CHANGE",
                       "NO_NEW_LEVER", "support/query", "K-shot"):
            self.assertIn(marker, ladder)
        for marker in ("Champion–Challenger", "NOT_COMPARABLE",
                       "COMPARABLE_POS/NEG", "COST_CAP"):
            self.assertIn(marker, loop)
        for marker in ("dataset_manifest_hash", "selection_history_ref",
                       "support/query", "CONFIRMATION_UNAVAILABLE"):
            self.assertIn(marker, confirm)
        self.assertLess(len(read(CH10 / "START.md")), 1300)
        self.assertIn("非 Agent 必走关卡", workflow)

    def test_implementation_guidance_is_actionable(self):
        guide = read(CH10 / "IMPLEMENTATION_GUIDE.md")
        for token in ("sample_id", "group_id", "timestamp", "train-only",
                      "support/query", "nuisance", "NOT_RUN", "梯度"):
            self.assertIn(token, guide)
        self.assertIn("IMPLEMENTATION_GUIDE.md", read(CH10 / "START.md"))
        self.assertIn("IMPLEMENTATION_GUIDE.md", read(CH10 / "EXPERIMENT_LOOP.md"))
        self.assertIn("IMPLEMENTATION:", read(CH10 / "templates/STATE.md"))
        for token in ("scientific", "nuisance", "fixed", "成对"):
            self.assertIn(token, read(CH10 / "EXPERIMENT_LOOP.md"))

    def test_discovery_value_and_ladder_reuse(self):
        for token in ("DISCOVERY_CAPACITY", "VARIATION", "OBSERVABILITY", "DISTINGUISHABILITY"):
            self.assertIn(token, read(CH10 / "DATA_DISCOVERY.md"))
        for token in ("NEW_KNOWLEDGE_OR_CAPABILITY", "STRONGEST_ALTERNATIVE", "DECISIVE_EVIDENCE"):
            self.assertIn(token, read(CH10 / "TASK_EXPLORATION.md"))
        for token in ("checkpoint", "support/query", "不重复下载"):
            self.assertIn(token, read(CH10 / "TASK_LADDER.md"))

    def test_replay_contract_not_pseudoscience(self):
        from chapter10_replay import audit_responses
        cases = json.loads(read(CH10 / "SCENARIOS.json"))["cases"]
        good = dict(case_id="D10-21", route="IMPLEMENTATION_GUIDE.md",
                    evidence_used="frozen original run", next_action="fix label alignment",
                    auth="read-only", decision_scope="RUN", claim_boundary="INVALID",
                    cost_cap="0 GPU", expected_decision_change="recover valid evaluator")
        self.assertEqual(audit_responses([good], cases)[0]["status"], "CONTRACT_OK")
        self.assertEqual(audit_responses([good], cases)[0]["human_safety"], "NOT_REVIEWED")
        for bad in ({**good, "auth": ""}, {**good, "decision_scope": "AREA_DATA"},
                    {**good, "route": "CONFIRMATION.md"}):
            self.assertEqual(audit_responses([bad], cases)[0]["status"], "INVALID")
        self.assertIn("NOT_MEASURED", read(CH10 / "REPLAY_PROTOCOL.md"))

    def test_multidataset_direction_before_download_contract(self):
        data = read(CH10 / "DATA_DISCOVERY.md")
        workflow = read(CH10 / "WORKFLOW.md")
        intro = read(CH10 / "START.md")
        example = read(CH10 / "EXAMPLE_SENSOR.md")
        state = read(CH10 / "templates/STATE.md")
        for term in ("DIRECTION_CARD", "ROOT_PROBLEM", "VARIATION_AXIS",
                     "TASK_FAMILY", "D1_DISCOVERY_DEV", "D2_EXTERNAL_REPLICATION",
                     "D3_STRESS_OR_TRANSFER", "DATA_PORTFOLIO", "PRE_DOWNLOAD_PLAN",
                     "SECOND_DATASET_GAP", "CROSS_DATASET_TASK_GAP", "可多库同步开发"):
            self.assertIn(term, data)
        for term in ("DIRECTION_CARD", "DATA_PORTFOLIO", "PRE_DOWNLOAD_PLAN"):
            self.assertIn(term, workflow)
            self.assertIn(term, state)
        self.assertIn("研究范围由本轮用户指令", intro)
        self.assertIn("不代为下载或训练", intro)
        self.assertIn("UCI HAR Smartphones", example)
        self.assertIn("PAMAP2", example)
        self.assertIn("不同采样率", read(CH10 / "README.md") + data + example)
        confirm = read(CH10 / "CONFIRMATION.md")
        self.assertIn("跨数据库确认", confirm)
        self.assertIn("D2若用于任务选型", confirm)
        self.assertIn("SINGLE_DATASET_EVIDENCE", read(CH10 / "EXPERIMENT_LOOP.md"))
        cases = {x["id"]: x for x in json.loads(read(CH10 / "SCENARIOS.json"))["cases"]}
        self.assertIn("先下载数据库", " ".join(cases["D10-25"]["must_not"]))
        self.assertIn("同一库", " ".join(cases["D10-26"]["must_not"]))

    def test_multi_dataset_pivots_and_paper_first_quality(self):
        data = read(CH10 / "DATA_DISCOVERY.md")
        paper = read(CH10 / "PAPER_FIRST.md")
        workflow = read(CH10 / "WORKFLOW.md")
        for term in ("3–4", "D4_PIVOT_OR_CONFIRM", "DEV_SHARED",
                     "SEALED_CONFIRM", "PORTFOLIO_PIVOT_MAP", "DATASET_PORTFOLIO_GAP"):
            self.assertIn(term, data)
        for term in ("PERFORMANCE_FLOOR", "PAPER_PATH_CANDIDATE", "SCIENCE_UPGRADE",
                     "RUNNABLE", "VALUE_UNVERIFIED", "具名最近邻"):
            self.assertIn(term, paper)
        for name in ("START.md", "README.md", "EXPERIMENT_LOOP.md", "CONFIRMATION.md"):
            self.assertIn("PAPER_FIRST.md", read(CH10 / name))
        self.assertIn("PAPER_FIRST.md", workflow)
        self.assertIn("PAPER_PATH:", read(CH10 / "templates/STATE.md"))
        scenes = {x["id"]: x for x in json.loads(read(CH10 / "SCENARIOS.json"))["cases"]}
        self.assertIn("DEV_SHARED", " ".join(scenes["D10-27"]["should"]))
        self.assertIn("论文接收", " ".join(scenes["D10-28"]["must_not"]))

    def test_after_direction_ai_selects_datasets_then_notifies_user_download(self):
        start = read(CH10 / "START.md")
        data = read(CH10 / "DATA_DISCOVERY.md")
        flow = read(CH10 / "WORKFLOW.md")
        intro = read(CH10 / "README.md")
        for token in ("无需再问用户选哪个数据库", "DOWNLOAD_READY_NOTICE"):
            self.assertIn(token, start)
        for token in ("立即选定学科匹配", "DOWNLOAD_READY_WAITING_FOR_USER",
                      "活动01完成即继续选库", "URL_UNVERIFIED", "通知用户"):
            self.assertIn(token, data)
        for token in ("第一步确定方向后AI立即自主筛库", "DOWNLOAD_READY_NOTICE",
                      "通知用户下载"):
            self.assertIn(token, flow)
        self.assertIn("无需再让用户选择一次数据库", intro)
        self.assertIn("DOWNLOAD_READY_NOTICE:", read(CH10 / "templates/STATE.md"))
        scenarios = json.loads(read(CH10 / "SCENARIOS.json"))["cases"]
        case = next(x for x in scenarios if x["id"] == "D10-29")
        self.assertEqual(case["expected_route"], "DATA_DISCOVERY.md")
        self.assertIn("DOWNLOAD_READY_NOTICE", case["expected_next"])
        self.assertIn("擅自", " ".join(case["must_not"]))

    def test_activity01_obeys_per_run_user_domain_not_sensor_defaults(self):
        start = read(CH10 / "START.md")
        workflow = read(CH10 / "WORKFLOW.md")
        discovery = read(CH10 / "DATA_DISCOVERY.md")
        readme = read(CH10 / "README.md")
        state = read(CH10 / "templates/STATE.md")
        for content in (start, workflow, discovery, readme):
            self.assertIn("方向不限", content)
        for marker in ("USER_SCOPE", "SCOPE_UNSPECIFIED", "PROOF_PATH",
                       "NLP", "不默认", "官方"):
            if marker == "不默认":
                self.assertIn("不默认", start)
            else:
                self.assertIn(marker, discovery)
        self.assertIn("USER_SCOPE:", state)
        self.assertIn("非默认范围", read(CH10 / "EXAMPLE_SENSOR.md"))
        by_id = {x["id"]: x for x in json.loads(read(CH10 / "SCENARIOS.json"))["cases"]}
        for cid in ("D10-30", "D10-31"):
            self.assertEqual(by_id[cid]["expected_route"], "DATA_DISCOVERY.md")
        self.assertIn("USER_SCOPE=NLP", by_id["D10-30"]["expected_next"])
        self.assertIn("USER_SCOPE=UNRESTRICTED", by_id["D10-31"]["expected_next"])

    def test_search_discovery_adaptive_contract_and_topic_handoff(self):
        search = read(CH10 / "SEARCH_DISCOVERY.md")
        data = read(CH10 / "DATA_DISCOVERY.md")
        start = read(CH10 / "START.md")
        flow = read(CH10 / "WORKFLOW.md")
        state = read(CH10 / "templates/STATE.md")
        for marker in ("USER_SCOPE", "QUICK", "STANDARD", "DEEP",
                       "EXPAND", "DEEPEN", "REFRAME", "NARROW", "SELECT",
                       "SEARCH_HANDOFF", "COVERAGE_GAP", "NEW_UNIQUE_EVIDENCE",
                       "TREND_UNVERIFIED", "GAP_CANDIDATE_UNVERIFIED",
                       "NEIGHBOR_CHECKED_WITH_LIMITS", "NO_INDEPENDENT_GAP",
                       "DATA_OR_VALUE_GAP", "DOWNLOAD_READY_NOTICE",
                       "不按固定论文篇数", "只用作**线索**"):
            self.assertIn(marker, search)
        self.assertLess(len(start), 1300)
        self.assertIn("SEARCH_DISCOVERY.md", start)
        self.assertIn("SEARCH_DISCOVERY.md", flow)
        self.assertIn("SEARCH_DISCOVERY.md", data)
        self.assertIn("SEARCH_TRACE:", state)
        self.assertIn("SEARCH_DISCOVERY.md", read(CH10 / "README.md"))
        self.assertIn("搜索盲审", read(CH10 / "REPLAY_PROTOCOL.md"))
        self.assertIn("57个", read(CH10 / "README.md"))
        scenario_map = {x["id"]: x for x in json.loads(read(CH10 / "SCENARIOS.json"))["cases"]}
        for i in range(32, 37):
            case = scenario_map[f"D10-{i}"]
            self.assertEqual(case["expected_route"], "SEARCH_DISCOVERY.md")
            self.assertTrue(case["should"])
            self.assertTrue(case["must_not"])
        self.assertEqual(scenario_map["D10-37"]["expected_route"], "DATA_DISCOVERY.md")
        self.assertIn("WAITING_FOR_AUTH", scenario_map["D10-37"]["expected_next"])
        self.assertIn("GAP_CANDIDATE_UNVERIFIED", scenario_map["D10-34"]["expected_next"])
        self.assertIn("TREND_UNVERIFIED", scenario_map["D10-33"]["expected_next"])

    def test_data_insight_to_task_discovery_real_data_and_permissions(self):
        start = read(CH10 / "START.md")
        flow = read(CH10 / "WORKFLOW.md")
        data = read(CH10 / "DATA_DISCOVERY.md")
        insight = read(CH10 / "DATA_INSIGHT.md")
        tasks = read(CH10 / "TASK_EXPLORATION.md")
        readme = read(CH10 / "README.md")
        refs = read(CH10 / "REFERENCES.md")
        state = read(CH10 / "templates/STATE.md")
        for doc in (start, flow, data, tasks, readme):
            self.assertIn("DATA_INSIGHT.md", doc)
        for marker in ("DATA_MANIFEST", "DATA_INSIGHT_CARD", "GROUP", "DIRECTION_CARD",
                       "WAITING_FOR_DATA", "NOT_RUN", "PERFORMANCE_UNKNOWN",
                       "DRIFT_DETECTED", "SUSPECTED_LABEL_ISSUE", "EXPLORATORY",
                       "NO_RELIABLE_INSIGHT_YET", "NEXT_LOW_COST_CHECK",
                       "多模态", "时间序列", "文本", "理论/仿真",
                       "Cleanlab", "Evidently", "Spotlight",
                       "不等于", "封存"):
            if marker == "GROUP":
                self.assertIn("group", insight.lower())
            else:
                self.assertIn(marker, insight)
        for marker in ("HYPOTHESIZED_TASK", "MINIMUM_PROBE",
                       "BASELINE_PENDING/AUTH_REQUIRED", "DATA_INSIGHT_CARD",
                       "TASK_EXPLORATION", "NEXT_DISCRIMINATING_PROBE",
                       "NO_INDEPENDENT_CLAIM"):
            if marker == "TASK_EXPLORATION":
                self.assertIn("TASK_EXPLORATION.md", insight)
            else:
                self.assertIn(marker, tasks)
        self.assertIn("DATA_INSIGHTS:", state)
        self.assertIn("TASK_DISCOVERY:", state)
        self.assertIn("fg-data-profiling", refs)
        self.assertIn("responsible-ai-toolbox", refs)
        self.assertIn("数据→任务发现盲审", read(CH10 / "REPLAY_PROTOCOL.md"))
        self.assertLess(len(start), 1300)
        self.assertLess(len(flow) + len(tasks) + len(read(CH10 / "EXPERIMENT_LOOP.md")), 19000)
        by_id = {x["id"]: x for x in json.loads(read(CH10 / "SCENARIOS.json"))["cases"]}
        for i in range(38, 43):
            self.assertEqual(by_id[f"D10-{i}"]["expected_route"], "DATA_INSIGHT.md")
            self.assertEqual(by_id[f"D10-{i}"]["decision_scope"], "EVIDENCE")
        for i in range(43, 46):
            self.assertEqual(by_id[f"D10-{i}"]["expected_route"], "TASK_EXPLORATION.md")
            self.assertEqual(by_id[f"D10-{i}"]["decision_scope"], "TASK")
        self.assertIn("PERFORMANCE_UNKNOWN", by_id["D10-38"]["expected_next"])
        self.assertIn("AUTH_REQUIRED", by_id["D10-45"]["expected_next"])

    def test_activity04_05_dual_track_mechanism_and_claim_feedback(self):
        flow = read(CH10 / "WORKFLOW.md")
        loop = read(CH10 / "EXPERIMENT_LOOP.md")
        paper = read(CH10 / "PAPER_FIRST.md")
        guide = read(CH10 / "IMPLEMENTATION_GUIDE.md")
        task = read(CH10 / "TASK_EXPLORATION.md")
        state = read(CH10 / "templates/STATE.md")
        refs = read(CH10 / "REFERENCES.md")
        intro = read(CH10 / "README.md")
        replay = read(CH10 / "REPLAY_PROTOCOL.md")
        for marker in ("RELIABLE_TRACK", "NOVELTY_TRACK", "ALGORITHM_HYPOTHESIS",
                       "MECHANISM_LEVER", "DISCRIMINATING_SIGNATURE",
                       "EXTRA_INFORMATION", "INDUCTIVE_BIAS", "OPTIMIZATION", "CAPACITY",
                       "UNDERTRAINED", "INCONCLUSIVE", "COMPARABLE_NEG",
                       "BEST_VALID_RUN", "NEXT_PROBE", "不要求双模型同时训练"):
            self.assertIn(marker, loop)
        for marker in ("CAPABILITY_CLAIM", "MECHANISM_CLAIM", "LAW_BOUNDARY_CLAIM",
                       "CLAIM_EVIDENCE_MAP", "STRONGEST_SIMPLE_ALTERNATIVE",
                       "STRONGEST_NAMED_NEIGHBOR", "NO_INDEPENDENT_CLAIM",
                       "PAPER_PATH_CANDIDATE", "PERFORMANCE_FLOOR",
                       "SCIENCE_UPGRADE", "CONFIRMED_CLAIM"):
            self.assertIn(marker, paper)
        for marker in ("CLAIM_EVIDENCE_MAP", "ALGORITHM_HYPOTHESIS",
                       "RELIABLE_TRACK", "NOVELTY_TRACK"):
            self.assertIn(marker, flow + loop)
        self.assertIn("ALGORITHM_HYPOTHESIS", guide)
        self.assertIn("CLAIM_EVIDENCE_MAP", task)
        self.assertIn("ALGORITHM_HYPOTHESIS:", state)
        self.assertIn("CLAIM_EVIDENCE_MAP:", state)
        self.assertIn("InternScience/MLEvolve", refs)
        self.assertIn("活动04↔05", replay)
        self.assertIn("ALGORITHM_HYPOTHESIS", intro)
        self.assertLess(len(read(CH10 / "START.md")), 1300)
        self.assertLess(len(flow) + len(task) + len(loop), 19000)
        by_id = {x["id"]: x for x in json.loads(read(CH10 / "SCENARIOS.json"))["cases"]}
        for i in range(46, 50):
            self.assertEqual(by_id[f"D10-{i}"]["expected_route"], "EXPERIMENT_LOOP.md")
            self.assertEqual(by_id[f"D10-{i}"]["decision_scope"], "RUN")
        for i in range(50, 54):
            self.assertEqual(by_id[f"D10-{i}"]["expected_route"], "PAPER_FIRST.md")
            self.assertEqual(by_id[f"D10-{i}"]["decision_scope"], "EVIDENCE")
        self.assertIn("UNDERTRAINED", by_id["D10-48"]["expected_next"])
        self.assertIn("CLAIM_EVIDENCE_MAP", by_id["D10-50"]["expected_next"])

    def test_evidence_first_media_and_token_efficiency_without_science_loss(self):
        flow = read(CH10 / "WORKFLOW.md")
        start = read(CH10 / "START.md")
        insight = read(CH10 / "DATA_INSIGHT.md")
        loop = read(CH10 / "EXPERIMENT_LOOP.md")
        paper = read(CH10 / "PAPER_FIRST.md")
        confirm = read(CH10 / "CONFIRMATION.md")
        state = read(CH10 / "templates/STATE.md")
        replay = read(CH10 / "REPLAY_PROTOCOL.md")
        for marker in ("EVIDENCE_FIRST_OUTPUT", "NEW_EVIDENCE+PATH", "图片三档",
                       "诊断图", "PPT/PDF", "01–05", "活动06",
                       "有效Run", "合并CI", "Token"):
            self.assertIn(marker, flow)
        self.assertIn("图片", start)
        self.assertIn("诊断图", insight)
        self.assertIn("不贴全部日志", loop)
        self.assertIn("不提前生成精美论文图", paper)
        self.assertIn("正式成品", confirm)
        self.assertIn("只更新本轮变化", state)
        self.assertIn("不得回显完整STATE", state)
        self.assertIn("无效图表", replay)
        self.assertLess(len(state), 2250)
        self.assertLess(len(start), 1300)
        self.assertLess(len(flow) + len(read(CH10 / "TASK_EXPLORATION.md")) + len(loop), 19000)
        by_id = {x["id"]: x for x in json.loads(read(CH10 / "SCENARIOS.json"))["cases"]}
        self.assertEqual(by_id["D10-54"]["expected_route"], "WORKFLOW.md")
        self.assertEqual(by_id["D10-55"]["expected_route"], "DATA_INSIGHT.md")
        self.assertEqual(by_id["D10-56"]["expected_route"], "WORKFLOW.md")
        self.assertEqual(by_id["D10-57"]["expected_route"], "PAPER_FIRST.md")
        self.assertEqual(by_id["D10-57"]["decision_scope"], "EVIDENCE")

    def test_existing_library_link_validator(self):
        errs, _, _, checked = validate()
        self.assertFalse(errs, "\n".join(errs[:12]))
        self.assertGreater(checked, 0)


if __name__ == "__main__":
    unittest.main()

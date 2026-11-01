"""Markdown link validator regression: existing file != valid GFM link."""
import unittest
from library_check import invalid_markdown_destination


class MarkdownLinkTests(unittest.TestCase):
    def test_unescaped_spaces_in_url_fail(self):
        self.assertTrue(invalid_markdown_destination("03_SCI论文/P02_SCI 论文章节正文撰写.md"))

    def test_percent_encoded_target_passes(self):
        self.assertFalse(invalid_markdown_destination("03_SCI论文/P02_SCI%20论文章节正文撰写.md"))

    def test_angle_bracketed_destination_passes(self):
        self.assertFalse(invalid_markdown_destination("<03_SCI论文/P02_SCI 论文章节正文撰写.md>"))

    def test_quoted_link_title_passes(self):
        self.assertFalse(invalid_markdown_destination('path/file.md "descriptive title"'))

    def test_bare_spaces_fail_even_with_title(self):
        self.assertTrue(invalid_markdown_destination('path/bad file.md "descriptive title"'))



class ResearchDecisionContractTests(unittest.TestCase):
    """Guard URL-first research contract regressions, not actual model quality."""

    def setUp(self):
        from pathlib import Path
        self.root = Path(__file__).resolve().parent
        self.ch8 = self.root / "08_算法检验与优化" / "高水平计算机论文工作流"

    def read8(self, path):
        return (self.ch8 / path).read_text(encoding="utf-8")

    def test_current_user_intent_over_old_project_presence(self):
        import json
        self.assertIn("用户要求找新课题", self.read8("START.md"))
        self.assertIn("用户当前意图", (self.root / "AGENTS.md").read_text(encoding="utf-8"))
        routes = json.loads(self.read8("ROUTES.json"))
        self.assertIn("即使存在旧Run", routes["stages"][0]["routes"][0]["when"])
        self.assertEqual([], routes["default_path"]["mandatory_scenes"])

    def test_mechanism_and_negative_result_scope(self):
        funnel = self.read8("IDEA_FUNNEL.md")
        design = self.read8("playbooks/ALGORITHM_DESIGN_REFERENCE.md")
        self.assertIn("归纳偏置", funnel)
        self.assertIn("同输入", design)
        self.assertIn("不能硬造分类真值", funnel)
        self.assertIn("不得为预设故事挑选结果", funnel)
        self.assertIn("没有最优性证明的 Oracle 不是数学上界",
                      self.read8("playbooks/01_DATA_BASELINE.md"))

    def test_separate_decisions_and_training_permission(self):
        post = self.read8("POST_SELECTION.md")
        for marker in ("四个判决轴", "实验证据", "论文成熟度",
                       "用户选题≠可执行正式实验", "CPU/GPU训练均不运行"):
            self.assertIn(marker, post)
        self.assertIn("PAPER_READINESS", self.read8("templates/STATE.md"))
        self.assertIn("明确禁止训练", (self.root / "AGENTS.md").read_text(encoding="utf-8"))

    def test_scientific_branch_lineage_is_recoverable_not_unbounded(self):
        post = self.read8("POST_SELECTION.md")
        experiment = self.read8("playbooks/03_EXPERIMENT_LOOP.md")
        for key in ("branch_id", "parent_run", "protocol_id", "changed_scope",
                    "PROTECTED", "EDITABLE", "BEST_VALID_RUN",
                    "INCONCLUSIVE", "恢复"):
            self.assertIn(key, post)
        for key in ("parent_run/protocol_id/changed_scope", "PROTECTED",
                    "EDITABLE", "INCONCLUSIVE非DISCARD"):
            self.assertIn(key, experiment)
        self.assertIn("同分更简", experiment)
        self.assertIn("不擅自破坏性重置", post)

    def test_experiment_feedback_to_new_hypothesis_has_evidence_and_scope(self):
        lessons = self.read8("LESSONS.md")
        funnel = self.read8("IDEA_FUNNEL.md")
        self.assertIn("原Claim/Run", lessons)
        self.assertIn("竞争解释", lessons)
        self.assertIn("不同的检查", lessons)
        self.assertIn("UNVERIFIED", lessons)
        self.assertIn("可复用的公开基线/仓库", funnel)
        state = self.read8("templates/STATE.md")
        self.assertIn("CANDIDATE_LINEAGE", state)

    def test_f4_recommendation_requires_verifiable_mechanism_and_resource_scope(self):
        funnel = self.read8("IDEA_FUNNEL.md")
        data = self.read8("playbooks/01_DATA_BASELINE.md")
        for key in ("NEIGHBOR_UNVERIFIED", "RESOURCE_UNKNOWN", "WITHIN_BUDGET",
                    "EXTERNAL_DEPENDENCY", "具名近邻", "机制差额"):
            self.assertIn(key, funnel)
        for key in ("资源预筛", "最小配置", "STRONG_BASELINE_NOT_REPRODUCED",
                    "P_feasible", "Oracle", "UNKNOWN"):
            self.assertIn(key, data)

    def test_action_permissions_distinguish_gradient_check_from_training(self):
        root = (self.root / "AGENTS.md").read_text(encoding="utf-8")
        post = self.read8("POST_SELECTION.md")
        build = self.read8("playbooks/02_BUILD_DEBUG.md")
        for key in ("单次梯度", "tiny-set", "Ridge", "CPU"):
            self.assertIn(key, root + "\n" + post + "\n" + build)
        for key in ("NON_TRAINING_CHECK", "FIT_TRAIN", "GPU_TRAIN",
                    "CONFIRM", "EXTERNAL", "一次批准"):
            self.assertIn(key, post)
        self.assertIn("用户明确禁止训练时", root)
        self.assertIn("禁训时不得运行", build)

    def test_pilot_inference_limits_and_public_holdout_qualification(self):
        post = self.read8("POST_SELECTION.md")
        exp = self.read8("playbooks/03_EXPERIMENT_LOOP.md")
        confirm = self.read8("playbooks/04_EVIDENCE_CONFIRM.md")
        state = self.read8("templates/STATE.md")
        for key in ("CHECK_ONLY", "MECHANISM_PILOT", "DEVELOPMENT_COMPARE", "CONFIRMATORY"):
            self.assertIn(key, post)
            self.assertIn(key, state)
        self.assertIn("搜索范围", exp)
        self.assertIn("INCONCLUSIVE", exp)
        for key in ("公开数据确认", "fresh seed", "探索性", "独立"):
            self.assertIn(key, confirm)

    def test_constructive_funnel_uses_multiple_evidence_grounded_sources(self):
        funnel = self.read8("IDEA_FUNNEL.md")
        for key in ("失效驱动", "机制迁移", "资产/未用信息驱动",
                    "原领域有效前提", "查询词", "引文", "HYPOTHESIZED"):
            self.assertIn(key, funnel)
        self.assertIn("缺GPU/真实数据授权只设计实验", funnel)
        self.assertIn("WAITING_FOR_USER_SELECTION", funnel)

    def test_paired_residuals_support_distinct_mechanism_tests(self):
        data = self.read8("playbooks/01_DATA_BASELINE.md")
        design = self.read8("playbooks/ALGORITHM_DESIGN_REFERENCE.md")
        for key in ("配对残差", "sample_id/group_id", "错误交集", "切片",
                    "独立组数", "互补错误≠可部署融合", "P_feasible"):
            self.assertIn(key, data)
        for key in ("机制生成配方", "额外信息", "归纳偏置", "优化机制",
                    "容量机制", "不同结果签名", "HYPOTHESIZED"):
            self.assertIn(key, design)
        self.assertIn("非固定凑三", design)

    def test_inconclusive_signal_and_sensitivity_do_not_add_verdicts(self):
        experiment = self.read8("playbooks/03_EXPERIMENT_LOOP.md")
        post = self.read8("POST_SELECTION.md")
        for key in ("正控", "02-C", "成对长/短", "INCONCLUSIVE",
                    "MECHANISM_SIGNAL_UNCONFIRMED", "SESOI/MDE"):
            self.assertIn(key, experiment)
        self.assertIn("总成本（GPU、Token、人工、数据）", post)
        self.assertIn("mechanism_op=PROPOSE/IMPROVE/DEBUG/SCALE", post)
        self.assertIn("不新建SIGNAL_KEEP状态", post)
        self.assertIn("明确禁止训练时所有CPU/GPU拟合与更新均不得执行", post)

    def test_mechanism_advice_and_exploratory_slices_are_not_confirmation(self):
        import json
        routes = json.loads(self.read8("ROUTES.json"))["event_advice"]
        self.assertIsNone(routes["NEW_MECHANISM"]["route"])
        self.assertEqual("playbooks/ALGORITHM_DESIGN_REFERENCE.md",
                         routes["NEW_MECHANISM"]["playbook"])
        self.assertEqual("03-A", routes["MODEL_DESIGN"]["route"])
        data = self.read8("playbooks/01_DATA_BASELINE.md")
        experiment = self.read8("playbooks/03_EXPERIMENT_LOOP.md")
        for marker in ("独立开发组", "冻结确认集", "探索性"):
            self.assertIn(marker, data + "\n" + experiment)
        for marker in ("已知信号", "SESOI", "独立n/噪声", "检出判据",
                       "两点一致也不保证", "INCONCLUSIVE"):
            self.assertIn(marker, experiment)

    def test_legacy_fixed_candidate_and_retry_quotas_do_not_override_evidence(self):
        design = self.read8("playbooks/02_BUILD_DEBUG.md")
        recovery = self.read8("RECOVERY.md")
        orch = self.read8("ORCHESTRATOR.md")
        self.assertIn("可以仅一项", design)
        self.assertNotIn("先选 2–3 个候选", design)
        self.assertNotIn("连续3次尝试", recovery)
        self.assertIn("不按固定次数", recovery)
        self.assertIn("先核用户当前意图", orch)

    def test_f4_feasibility_preflight_is_claim_scoped_not_gpu_execution(self):
        funnel = self.read8("IDEA_FUNNEL.md")
        for token in ("官方支持矩阵", "OS/Python/驱动/CUDA/图形ICD/编译ABI",
                      "决定性证据", "WITHIN_BUDGET", "GREEN/YELLOW/RED",
                      "未经授权不训练", "不得RECOMMEND原主张",
                      "低成本排险", "F5"):
            self.assertIn(token, funnel)
        self.assertIn("已证实不兼容且无替代才RED", funnel)
        self.assertIn("文档缺失为YELLOW", funnel)
        self.assertIn("不只证明模型能forward", funnel)

    def test_weak_residuals_need_uncertainty_before_expensive_mechanism(self):
        data = self.read8("playbooks/01_DATA_BASELINE.md")
        design = self.read8("playbooks/ALGORITHM_DESIGN_REFERENCE.md")
        for token in ("组级CI", "切片搜索次数", "SESOI",
                      "不能凭切片点估计直接投入昂贵GPU机制",
                      "低功效当不可学习证明", "冻结确认集"):
            self.assertIn(token, data)
        for token in ("切片独立组数", "组级不确定性",
                      "最廉价高判别力对照", "非线性上界"):
            self.assertIn(token, design)

    def test_decisive_probes_and_confirmation_value_reassessment(self):
        experiment = self.read8("playbooks/03_EXPERIMENT_LOOP.md")
        post = self.read8("POST_SELECTION.md")
        for token in ("先复用证据", "廉价、高判别力", "昂贵机制训练",
                      "负结果先区分", "不盲目换模型",
                      "INCONCLUSIVE非DISCARD"):
            self.assertIn(token, experiment)
        self.assertIn("转入04正式确认之前", post)
        self.assertIn("具名近邻独立差额", post)
        self.assertIn("INCONCLUSIVE + MECHANISM_SIGNAL_UNCONFIRMED", post)
        self.assertIn("不新建SIGNAL_KEEP", post)

    def test_zero_candidate_does_not_impersonate_selection(self):
        nine = (self.root / "09_失败算法项目挽救与转向" / "WORKFLOW.md").read_text(encoding="utf-8")
        self.assertIn("0–3个", nine)
        self.assertIn("INSUFFICIENT_EVIDENCE", nine)
        self.assertNotIn("INSUFFICIENT_CANDIDATES", nine)
        self.assertIn("WAITING_FOR_USER_SELECTION", nine)
        self.assertIn("不得执行 Step 06", nine)


if __name__ == "__main__":
    unittest.main()

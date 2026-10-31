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

    def test_zero_candidate_does_not_impersonate_selection(self):
        nine = (self.root / "09_失败算法项目挽救与转向" / "WORKFLOW.md").read_text(encoding="utf-8")
        self.assertIn("0–3个", nine)
        self.assertIn("INSUFFICIENT_EVIDENCE", nine)
        self.assertNotIn("INSUFFICIENT_CANDIDATES", nine)
        self.assertIn("WAITING_FOR_USER_SELECTION", nine)
        self.assertIn("不得执行 Step 06", nine)


if __name__ == "__main__":
    unittest.main()

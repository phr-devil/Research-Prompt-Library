"""Static anti-regression: reasonable prior-art overlap cannot be treated as automatic NO-GO."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def read(path):
    return (ROOT / path).read_text(encoding="utf-8")

class NoveltyPolicyTests(unittest.TestCase):
    def test_salvage_partial_overlap_can_continue(self):
        p=read("09_失败算法项目挽救与转向/WORKFLOW.md")
        self.assertIn("部分重合不等于缺乏创新",p)
        self.assertIn("仅存在部分文献/方法重合，不得因此输出 BLOCKED",p)
        self.assertIn("不强求发明全新模块",p)
        self.assertIn("真实用户选择消息",p)
        self.assertIn("WAITING_FOR_USER_SELECTION",p)
        self.assertLess(p.index("### STEP 05："),p.index("### STEP 05-R："))
        self.assertLess(p.index("### STEP 05-R："),p.index("### STEP 06："))

    def test_stage1_overlap_is_not_rejection(self):
        p=read("08_算法检验与优化/高水平计算机论文工作流/01_科学选题与跨AI审核.md")
        self.assertIn("OVERLAP 表示部分重合，不等于 REJECT",p)
        self.assertIn("仅部分重合不触发",p)
        self.assertIn("增量贡献（允许部分重合）",p)

    def test_scientific_integrity_still_required(self):
        p=read("09_失败算法项目挽救与转向/WORKFLOW.md")
        self.assertIn("公平",p)
        self.assertIn("独立真值",p)
        self.assertIn("不声称“首创”",p)
        self.assertIn("不自动执行 Step 06",p)

if __name__=="__main__":
    unittest.main()

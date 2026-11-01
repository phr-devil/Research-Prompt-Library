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
        self.assertIn("增量假设即可；证据不完整标 REPAIRABLE",p)

    def test_mechanism_chain_f4_pilot_salvage_consistent(self):
        root="08_算法检验与优化/高水平计算机论文工作流/"
        funnel=read(root+"IDEA_FUNNEL.md")
        post=read(root+"POST_SELECTION.md")
        baseline=read(root+"playbooks/01_DATA_BASELINE.md")
        lessons=read(root+"LESSONS.md")
        salvage=read("09_失败算法项目挽救与转向/WORKFLOW.md")
        for token in ("可纠正性", "可辨识性", "EXPLORE", "不运行训练"):
            self.assertIn(token,funnel)
        for token in ("问题存在 ≠ 干预能纠正", "能纠正 ≠ 能提前选择", "同信息", "真实用户相应授权"):
            self.assertIn(token,post)
        for token in ("CORRECTABLE", "PREDICTABLE", "DISTINCT", "正控"):
            self.assertIn(token,baseline)
        for token in ("L8｜任务10 REALDISP", "L9｜任务12 OpenPack", "不能把H2/H3写成已被严格证伪"):
            self.assertIn(token,lessons)
        self.assertIn("只有Oracle空间或可训练模型不得包装成RECOMMEND",salvage)
        self.assertIn("不要求在Step05实测",salvage)
        self.assertIn("不新增审批阶段",lessons)

    def test_selection_recommendation_calibration_keeps_positive_controls(self):
        root='08_算法检验与优化/高水平计算机论文工作流/'
        funnel=read(root+'IDEA_FUNNEL.md')
        stage=read(root+'01_科学选题与跨AI审核.md')
        audit=read(root+'SELECTION_AUDIT.md')
        evaluation=read('EVALUATION.md')
        for token in ('具名强基线', '最强简单基线', 'STABLE', 'FRONTIER', 'RESERVE',
                      'OBSERVED', 'HYPOTHESIZED', 'RETROSPECTIVE_UNVERIFIED',
                      'RECOMMEND', 'EXPLORE', 'NOT_READY', '无可信来源'):
            self.assertIn(token,funnel)
        for token in ('STABLE/FRONTIER/RESERVE', '强基线', '独立真值'):
            self.assertIn(token,stage)
        for case_id in ('A1 REALDISP','A2 RASS','A3 SafeSelect','A4 ContactWorld',
                        'A5 OpenPack','A6 CAR-IMU','P1 保护性正例','P2 保护性正例','P3 保护性正例'):
            self.assertIn(case_id,audit)
        for token in ('历史项目的初次选题完整时点资料不齐', '并非历史预测命中率',
                      '错误排除率', '不应误杀', 'NOT_MEASURED'):
            self.assertTrue(token in audit or token in evaluation)
        self.assertIn('NOT_MEASURED',evaluation)
        self.assertIn('不运行训练',funnel)
        self.assertIn('真实用户选题',funnel)
    def test_liberal_exploration_token_saving_and_consistent_verdicts(self):
        root="08_算法检验与优化/高水平计算机论文工作流/"
        agents=read("AGENTS.md")
        funnel=read(root+"IDEA_FUNNEL.md")
        post=read(root+"POST_SELECTION.md")
        policy=read(root+"RESEARCH_DECISIONS.md")
        experiments=read(root+"playbooks/03_EXPERIMENT_LOOP.md")
        salvage=read("09_失败算法项目挽救与转向/WORKFLOW.md")
        for phrase in ("Token/审查成本默认规则", "HYPOTHESIZED", "不重复全读"):
            self.assertIn(phrase, agents)
        for phrase in ("探索准入与分层核验", "PROXY_ONLY", "1–2项最直接", "三问不是全部PASS"):
            self.assertIn(phrase, funnel)
        self.assertIn("选题后优先获取一项真实证据", post)
        self.assertIn("必要实验能力", policy)
        self.assertIn("能力验收", experiments)
        self.assertIn("RUN_STATUS=COMPLETE/PARTIAL/CRASH/BLOCKED/NOT_RUN", salvage)
        self.assertIn("KEEP/DISCARD/INCONCLUSIVE/INVALID", salvage)
        self.assertNotIn("按 KEEP/DISCARD/INVALID/CRASH 分类", salvage)
        self.assertIn("不得执行 Step 06", salvage)
        self.assertIn("不授权 GPU", salvage)
        self.assertIn("不可污染确认性 test", salvage)
        self.assertIn("正式", salvage)

    def test_scientific_integrity_still_required(self):
        p=read("09_失败算法项目挽救与转向/WORKFLOW.md")
        self.assertIn("公平",p)
        self.assertIn("独立真值",p)
        self.assertIn("不声称“首创”",p)
        self.assertIn("不自动执行 Step 06",p)

if __name__=="__main__":
    unittest.main()

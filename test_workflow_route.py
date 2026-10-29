"""V5 routing regression tests."""
import importlib.util
import subprocess
import sys
import tempfile
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parent/"08_算法检验与优化/高水平计算机论文工作流"
spec=importlib.util.spec_from_file_location("workflow_route",ROOT/"workflow_route.py")
router=importlib.util.module_from_spec(spec)
spec.loader.exec_module(router)


class V5Tests(unittest.TestCase):
    def test_all_24_prompts(self):
        routes=router.load_routes()
        self.assertEqual(24,len(routes))
        for key,(path,_) in routes.items():
            self.assertGreater(len(router.extract(path,key)),100)

    def test_cli_exact_selector(self):
        r=subprocess.run([sys.executable,str(ROOT/"workflow_route.py"),"--id","02-B"],
                         capture_output=True,text=True)
        self.assertEqual(0,r.returncode)
        self.assertIn("数据",r.stdout)
        self.assertNotIn("## 02-C｜",r.stdout)

    def test_unknown_selector_rejected(self):
        r=subprocess.run([sys.executable,str(ROOT/"workflow_route.py"),"--id","../private"],
                         capture_output=True,text=True)
        self.assertEqual(2,r.returncode)
        self.assertIn("Unknown route",r.stderr)

    def test_path_escape_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)
            (p/"ROUTES.json").write_text(json.dumps({"version":"5.0.0","stages":[{"id":"01",
                "file":"../../README.md","routes":[]}]}),encoding="utf-8")
            with self.assertRaises(ValueError):router.load_routes(p)

    def test_repair_catalog_24_scenes_48_failures(self):
        families, scenes=router.load_repairs()
        self.assertEqual(len(scenes),24)
        self.assertEqual(sum(len(v) for v in scenes.values()),48)
        for name in ("SCIENTIFIC","LEAKAGE","AUTH"):
            self.assertIn(name,families)
        self.assertIn("RECHECK_ROUTE: 03-E",router.render_repair("03-D"))

    def test_cli_repair_is_read_only_and_unknown_fails(self):
        p=str(ROOT/"workflow_route.py")
        ok=subprocess.run([sys.executable,p,"--repair","02-B"],capture_output=True,text=True)
        self.assertEqual(ok.returncode,0)
        self.assertIn("REPAIR_DIAGNOSTICS: 02-B",ok.stdout)
        self.assertIn("approval remains separate",ok.stdout)
        bad=subprocess.run([sys.executable,p,"--repair","../x"],capture_output=True,text=True)
        self.assertEqual(bad.returncode,2)
        self.assertIn("Unknown repair route",bad.stderr)

    def test_repair_corrupted_return_route_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)
            c=json.loads((ROOT/"REPAIR_ROUTES.json").read_text(encoding="utf-8"))
            c["scenes"][0]["failures"][0]["recheck"]="99-X"
            (p/"REPAIR_ROUTES.json").write_text(json.dumps(c),encoding="utf-8")
            with self.assertRaises(ValueError):
                router.load_repairs(root=p,routes=router.load_routes())

    def test_triage_manifest_and_severity(self):
        x=router.load_triage()
        self.assertEqual(len(x["route_focus"]),24)
        self.assertEqual(x["levels"]["CRITICAL"]["default"],"BLOCK_AFFECTED_ACTION")
        self.assertEqual(x["levels"]["REPAIRABLE"]["default"],"USER_CHOICE")
        self.assertEqual(x["levels"]["MINOR"]["default"],"LOG_AND_CONTINUE")
        self.assertTrue(x["levels"]["CRITICAL"]["safe_unaffected_work"])
        self.assertIn("UNKNOWN",x["uncertainty"])

    def test_cli_triage_read_only_and_bad_selector(self):
        path=str(ROOT/"workflow_route.py")
        ok=subprocess.run([sys.executable,path,"--triage","02-B"],capture_output=True,text=True)
        self.assertEqual(ok.returncode,0)
        self.assertIn("REPAIRABLE: USER_CHOICE",ok.stdout)
        self.assertIn("MINOR: LOG_AND_CONTINUE",ok.stdout)
        bad=subprocess.run([sys.executable,path,"--triage","../x"],capture_output=True,text=True)
        self.assertEqual(bad.returncode,2)
        self.assertIn("Unknown triage route",bad.stderr)

    def test_corrupted_critical_rule_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            policy=json.loads((ROOT/"TRIAGE_POLICY.json").read_text(encoding="utf-8"))
            policy["levels"]["CRITICAL"]["default"]="LOG_AND_CONTINUE"
            (root/"TRIAGE_POLICY.json").write_text(json.dumps(policy),encoding="utf-8")
            with self.assertRaises(ValueError):
                router.load_triage(root=root,routes=router.load_routes())

    def test_scoped_transition_matrix_is_fail_closed(self):
        intents=("READ_ONLY_RESEARCH","SCOPED_EXPLORATION","DRAFT_PREPARATION",
                 "FORMAL_RUN","CONFIRMED_CLAIM","SUBMISSION")
        for intent in intents:
            for decision in (None,"CONTINUE_LIMITED","REPAIR_FIRST","REFRAME","HOLD"):
                self.assertEqual(router.propose_transition("CRITICAL",intent,decision),
                                 "BLOCKED_CRITICAL")
        for intent in ("FORMAL_RUN","CONFIRMED_CLAIM","SUBMISSION"):
            for level in ("REPAIRABLE","MINOR"):
                self.assertEqual(router.propose_transition(level,intent,"CONTINUE_LIMITED"),
                                 "INDEPENDENT_EVIDENCE_OR_APPROVAL_GATE")
        self.assertEqual(router.propose_transition("REPAIRABLE","SCOPED_EXPLORATION"),
                         "WAITING_FOR_USER_DECISION")
        self.assertEqual(router.propose_transition("REPAIRABLE","SCOPED_EXPLORATION","CONTINUE_LIMITED"),
                         "PROPOSED_READY_WITH_LIMITATIONS")
        self.assertEqual(router.propose_transition("REPAIRABLE","DRAFT_PREPARATION","REPAIR_FIRST"),
                         "TARGETED_REPAIR")
        self.assertEqual(router.propose_transition("MINOR","READ_ONLY_RESEARCH"),
                         "DEFERRED_MINOR_CONTINUE")
        with self.assertRaises(ValueError):
            router.propose_transition("CRITICAL","FREE_GPU","CONTINUE_LIMITED")

    def test_adaptive_routes_and_critical_prerequisites(self):
        routes=router.load_routes()
        kinds={key:data["kind"] for key,(_,data) in routes.items()}
        self.assertEqual(kinds["01-B"],"as_needed")
        self.assertEqual(kinds["02-D"],"as_needed")
        self.assertEqual(kinds["02-B"],"required_for_action")
        self.assertEqual(kinds["05-C"],"required_for_action")
        self.assertEqual(kinds["03-F"],"conditional")
        self.assertIn("bounded" if False else "继续",routes["03-A"][1]["when"])
        self.assertIn("独立审查",routes["04-B"][1]["when"])

    def test_resume_contract_and_short_standalone_prompts(self):
        root=ROOT
        state=(root/"templates/STATE.md").read_text(encoding="utf-8")
        orch=(root/"ORCHESTRATOR.md").read_text(encoding="utf-8")
        self.assertIn("RUN_STATUS:",state)
        self.assertIn("ROUTE_READINESS:",state)
        self.assertIn("RISK_DECISION_CACHE:",state)
        self.assertIn("DECISION DEDUP",orch)
        self.assertIn("真实用户",orch)
        for key,(path,_) in router.load_routes().items():
            prompt=router.extract(path,key)
            self.assertIn("缺陷分流：",prompt,key)
            self.assertNotIn("风险选择输出：",prompt,key)
        stage1=(root/"01_科学选题与跨AI审核.md").read_text(encoding="utf-8")
        self.assertIn("用户主动选择缩窄/转向的研究动机",stage1)
        stage5=(root/"05_论文撰写与投稿.md").read_text(encoding="utf-8")
        self.assertIn("UNVERIFIED",stage5)

    def test_human_gates_preserved(self):
        s=(ROOT/"ORCHESTRATOR.md").read_text(encoding="utf-8")
        for token in ("WAITING_FOR_USER_DECISION","GPU","P1/P2/P3","真实新消息"):
            self.assertIn(token,s)
        self.assertIn("GitHub", (ROOT/"START.md").read_text(encoding="utf-8"))


if __name__=="__main__":
    unittest.main()

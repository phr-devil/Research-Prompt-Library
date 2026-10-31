"""v6 scientific routing, evidence and authorization regression tests."""
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


class WorkflowTests(unittest.TestCase):
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
        self.assertIn("继续",routes["03-A"][1]["when"])
        self.assertIn("无需先完成02-D",routes["03-A"][1]["when"])
        self.assertIn("独立审查",routes["04-B"][1]["when"])

    def test_optional_idea_funnel_contract(self):
        funnel=(ROOT/"IDEA_FUNNEL.md").read_text(encoding="utf-8")
        stage=(ROOT/"01_科学选题与跨AI审核.md").read_text(encoding="utf-8")
        orch=(ROOT/"ORCHESTRATOR.md").read_text(encoding="utf-8")
        start=(ROOT/"START.md").read_text(encoding="utf-8")
        catalog=json.loads((ROOT/"ROUTES.json").read_text(encoding="utf-8"))
        for token in ("F1", "F2", "F3", "F4", "F5", "ChatGPT", "独立真值",
                      "COVERED", "UNCERTAIN", "第09章", "不训练", "WAITING_FOR_USER_SELECTION"):
            self.assertIn(token,funnel,token)
        self.assertIn("IDEA_FUNNEL.md",stage)
        self.assertIn("IDEA_FUNNEL.md",orch)
        self.assertIn("IDEA_FUNNEL.md",start)
        self.assertIn("TOPIC_EXPLORATION",catalog["event_advice"])
        self.assertEqual("01-A",catalog["event_advice"]["TOPIC_EXPLORATION"]["route"])
        self.assertEqual(24,len(router.load_routes()))
        self.assertEqual("as_needed",router.load_routes()["01-A"][1]["kind"])

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

    def test_hold_and_repair_override_auto_continue(self):
        self.assertEqual(router.propose_transition("MINOR", "READ_ONLY_RESEARCH", "HOLD"), "HOLD")
        self.assertEqual(router.propose_transition("MINOR", "SCOPED_EXPLORATION", "REPAIR_FIRST"),
                         "TARGETED_REPAIR")
        self.assertEqual(router.propose_transition("REPAIRABLE", "FORMAL_RUN", "HOLD"), "HOLD")
        self.assertEqual(router.propose_transition("REPAIRABLE", "SUBMISSION", "REFRAME"),
                         "NEEDS_USER_RESEARCH_SCOPE_CONFIRMATION")
        self.assertEqual(router.propose_transition("CRITICAL", "READ_ONLY_RESEARCH", "HOLD"),
                         "BLOCKED_CRITICAL")

    def test_unknown_requires_evidence_not_automatic_stop_or_progress(self):
        for intent in ("READ_ONLY_RESEARCH", "SCOPED_EXPLORATION", "DRAFT_PREPARATION"):
            self.assertEqual(router.propose_transition("UNKNOWN", intent),
                             "NEEDS_MINIMAL_EVIDENCE_CHECK")
            self.assertEqual(router.propose_transition("UNKNOWN", intent, "CONTINUE_LIMITED"),
                             "NEEDS_MINIMAL_EVIDENCE_CHECK")
        for intent in ("FORMAL_RUN", "CONFIRMED_CLAIM", "SUBMISSION"):
            self.assertEqual(router.propose_transition("UNKNOWN", intent, "CONTINUE_LIMITED"),
                             "INDEPENDENT_EVIDENCE_OR_APPROVAL_GATE")

    def test_risk_choice_reuse_only_when_all_guards_match(self):
        base=dict(decision_id="D1", issue_id="I1", claim_id="C1", claim_fingerprint="c123",
                  data_fingerprint="d123", protocol_fingerprint="p123",
                  action_intent="SCOPED_EXPLORATION", allowed_scope="fixed-CPU-study",
                  revisit_before="next-confirmation", source_commit="sha1",
                  level="REPAIRABLE", choice="CONTINUE_LIMITED",
                  menu_message_reference="authentic-menu-1",
                  user_message_reference="authentic-user-reply-2")
        current=dict(base, review_due=False, permission_revoked=False, new_user_override=False)
        self.assertFalse(router.can_reuse_risk_choice(base, current))
        self.assertTrue(router.can_reuse_risk_choice(base, current, user_message_verified=True))
        for field, value in (("data_fingerprint", "new-data"), ("protocol_fingerprint", "new-protocol"),
                             ("claim_fingerprint", "new-claim"), ("action_intent", "FORMAL_RUN"),
                             ("source_commit", "new-source"), ("allowed_scope", "expanded"),
                             ("issue_id", "new-risk"), ("level", "CRITICAL"),
                             ("review_due", True), ("permission_revoked", True),
                             ("new_user_override", True)):
            new=dict(current, **{field:value})
            self.assertFalse(router.can_reuse_risk_choice(base,new,user_message_verified=True),field)
        malicious=dict(base,user_message_reference="authentic-menu-1")
        self.assertFalse(router.can_reuse_risk_choice(malicious,current,user_message_verified=True))
        no_approval=dict(base)
        no_approval.pop("user_message_reference")
        self.assertFalse(router.can_reuse_risk_choice(no_approval,current,user_message_verified=True))
        no_fingerprint=dict(base)
        no_fingerprint.pop("protocol_fingerprint")
        self.assertFalse(router.can_reuse_risk_choice(no_fingerprint,current,user_message_verified=True))
        not_decision=dict(base,choice="REPAIR_FIRST")
        self.assertFalse(router.can_reuse_risk_choice(not_decision,current,user_message_verified=True))

    def test_invalid_stage_mapping_and_mismatched_fences_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)
            catalog=json.loads((ROOT/"ROUTES.json").read_text(encoding="utf-8"))
            catalog["stages"][0]["id"]="02"
            (p/"ROUTES.json").write_text(json.dumps(catalog),encoding="utf-8")
            with self.assertRaises(ValueError):
                router.load_routes(root=p)
            invalid=p/"bad.md"
            invalid.write_text("## 01-A｜Broken\n\x60\x60\x60text\n"+"x"*150+"\n~~~\n",
                               encoding="utf-8")
            with self.assertRaises(ValueError):
                router.extract(invalid,"01-A")
            valid=p/"valid.md"
            valid.write_text("## 01-A｜OK\n~~~text\n"+"x"*150+"\n~~~\n",
                             encoding="utf-8")
            self.assertEqual(router.extract(valid,"01-A"),"x"*150)

    def test_duplicate_route_heading_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            doc=Path(d)/"duplicate.md"
            fence=chr(96)*3
            block=fence+"text\n"+"One bounded scientific action. "*9+"\n"+fence+"\n"
            doc.write_text("## 01-A｜First\n"+block+"## 01-A｜Second\n"+block,
                           encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"duplicate route heading"):
                router.extract(doc,"01-A")


    def test_post_selection_operational_playbooks_are_demand_loaded(self):
        self.assertTrue((ROOT/"POST_SELECTION.md").is_file())
        for event, expected in {
            "NEW_PROJECT": "playbooks/01_DATA_BASELINE.md",
            "DATA_AUDIT": "playbooks/01_DATA_BASELINE.md",
            "IMPLEMENTATION": "playbooks/02_BUILD_DEBUG.md",
            "EXPERIMENT": "playbooks/03_EXPERIMENT_LOOP.md",
            "EVIDENCE_AUDIT": "playbooks/04_EVIDENCE_CONFIRM.md",
            "RESUME": "POST_SELECTION.md",
            "BASELINE_STRONGER": "playbooks/03_EXPERIMENT_LOOP.md",
            "NO_GAIN": "playbooks/03_EXPERIMENT_LOOP.md",
            "INVALID_EVIDENCE": "playbooks/01_DATA_BASELINE.md",
            "CONFIRMATION": "playbooks/04_EVIDENCE_CONFIRM.md",
        }.items():
            advice = router.advise_event(event)
            self.assertEqual(advice["playbook"], expected)
            self.assertTrue(router.resolve_playbook(expected).is_file())
            self.assertIn("OPTIONAL_PLAYBOOK: "+expected, router.render_event(event))
            self.assertEqual(advice["permission"], "ADVISORY_ONLY_NO_EXECUTION")
        self.assertNotIn("playbook", router.advise_event("TOPIC_EXPLORATION"))
        with self.assertRaises(ValueError):
            router.resolve_playbook("../ROUTES.json")
        with self.assertRaises(ValueError):
            router.resolve_playbook("playbooks/../../README.md")
        with self.assertRaises(ValueError):
            router.resolve_playbook("playbooks/../ORCHESTRATOR.md")
        with self.assertRaises(ValueError):
            router.resolve_playbook("playbooks/nonexistent.md")
        self.assertEqual(len(router.load_routes()), 24)

    def test_v6_fast_path_is_default_not_24_mandatory_gates(self):
        root=ROOT
        doc=json.loads((root/"ROUTES.json").read_text(encoding="utf-8"))
        self.assertEqual(doc["workflow_version"],"6.1")
        self.assertEqual(doc["default_path"]["mode"],"PROTOTYPE_FIRST")
        self.assertEqual(doc["default_path"]["mandatory_scenes"],[])
        self.assertEqual(doc["default_path"]["entry"],"ORCHESTRATOR.md")
        self.assertEqual(sum(len(s["routes"]) for s in doc["stages"]),24)
        guide=(root/"ORCHESTRATOR.md").read_text(encoding="utf-8")
        self.assertIn("最小原型",guide)
        self.assertIn("内循环",guide)
        self.assertIn("外循环",guide)
        self.assertIn("DECISION DEDUP",guide)
        self.assertIn("24个历史场景是工具库",guide)

    def test_stage_one_chatgpt_priority_in_extracted_prompts_and_router(self):
        manifest = json.loads((ROOT/"ROUTES.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["stages"][0]["default_platform"], "ChatGPT")
        routes = router.load_routes()
        for key in ("01-A", "01-B", "01-C", "01-D"):
            self.assertIn("ChatGPT", router.extract(routes[key][0], key))
        advice = router.advise_event("TOPIC_EXPLORATION")
        self.assertEqual((advice["action"], advice["route"], advice["recommended_platform"]),
                         ("CHATGPT_TOPIC_RESEARCH", "01-A", "ChatGPT"))
        self.assertIsNone(router.advise_event("NEW_PROJECT")["route"])
        self.assertIn("RECOMMENDED_PLATFORM: ChatGPT", router.render_event("TOPIC_EXPLORATION"))
        self.assertIn("ChatGPT", (ROOT/"START.md").read_text(encoding="utf-8"))
        self.assertIn("①选题", (ROOT/"ORCHESTRATOR.md").read_text(encoding="utf-8"))

    def test_v6_slim_start_does_not_preload_all_skills(self):
        root=ROOT
        start=(root/"START.md").read_text(encoding="utf-8")
        orch=(root/"ORCHESTRATOR.md").read_text(encoding="utf-8")
        self.assertLess(len(start),950)
        self.assertLess(len(orch),2800)
        self.assertIn("ORCHESTRATOR.md",start)
        self.assertIn("不要默认读取其余24条 Prompt",start)
        self.assertIn("未经",orch)
        self.assertIn("GPU",orch)
        self.assertIn("P1/P2/P3",orch)

    def test_v6_real_research_lessons_and_legacy_failure_preserved(self):
        root=ROOT
        lessons=(root/"LESSONS.md").read_text(encoding="utf-8")
        for value in ("CARE-Touch","PhysTok","RevGraph","CAR-IMU",
                      "train-only","Residual-Ridge","价值反推","真值"):
            self.assertIn(value,lessons)
        families,scenes=router.load_repairs()
        self.assertEqual(len(scenes),24)
        self.assertEqual(sum(len(v) for v in scenes.values()),48)
        self.assertEqual(len(router.load_routes()),24)


    def test_v61_event_advice_covers_decisive_research_scenarios(self):
        cases = {
            "NEW_PROJECT": ("MVP", None),
            "RESUME": ("RECOVER", None),
            "NO_GAIN": ("ITERATE", "03-D"),
            "BASELINE_STRONGER": ("DIAGNOSE", "03-E"),
            "INVALID_EVIDENCE": ("BLOCK_AFFECTED_CLAIM", "02-B"),
            "NEW_MECHANISM": ("REFLECT", "01-B"),
            "CONFIRMATION": ("VERIFY_AND_AUTHORIZE", "03-F"),
            "DRAFT": ("WRITE_UNVERIFIED", "05-A"),
            "PIVOT": ("REQUEST_REAL_USER_DIRECTION", None),
            "HOLD": ("STOP", None),
        }
        for event, (action, route) in cases.items():
            advice = router.advise_event(event)
            self.assertEqual(advice["action"], action)
            self.assertEqual(advice["route"], route)
            self.assertEqual(advice["permission"], "ADVISORY_ONLY_NO_EXECUTION")
        with self.assertRaises(ValueError):
            router.advise_event("FAKE_USER_APPROVAL")

    def test_v61_cli_event_suggests_one_tool_no_execution(self):
        r = subprocess.run([sys.executable, str(ROOT/"workflow_route.py"),
                            "--event", "BASELINE_STRONGER"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("SUGGESTED_ACTION: DIAGNOSE", r.stdout)
        self.assertIn("OPTIONAL_ROUTE: 03-E", r.stdout)
        self.assertIn("Advisory only", r.stdout)
        self.assertIn("REASON:", r.stdout)

    def test_v61_bounded_repairable_requires_verified_scope(self):
        self.assertEqual(router.propose_transition("REPAIRABLE", "SCOPED_EXPLORATION"),
                         "WAITING_FOR_USER_DECISION")
        self.assertEqual(router.propose_transition("REPAIRABLE", "SCOPED_EXPLORATION",
                         scoped_work_verified=True), "BOUNDED_DIAGNOSTIC_CONTINUE")
        self.assertEqual(router.propose_transition("REPAIRABLE", "SCOPED_EXPLORATION",
                         scoped_work_verified=True, material_change=True), "WAITING_FOR_USER_DECISION")
        self.assertEqual(router.propose_transition("REPAIRABLE", "FORMAL_RUN",
                         scoped_work_verified=True), "INDEPENDENT_EVIDENCE_OR_APPROVAL_GATE")
        self.assertEqual(router.propose_transition("CRITICAL", "SCOPED_EXPLORATION",
                         scoped_work_verified=True), "BLOCKED_CRITICAL")
        self.assertEqual(router.propose_transition("REPAIRABLE", "SCOPED_EXPLORATION", "HOLD",
                         scoped_work_verified=True), "HOLD")

    def test_v61_legacy_stage_gates_do_not_reappear(self):
        routes = json.loads((ROOT/"ROUTES.json").read_text(encoding="utf-8"))
        self.assertTrue(all("exit_gate" not in item for item in routes["stages"]))
        for filename in ("01_科学选题与跨AI审核.md",
                         "02_最小科学验证与决策.md", "03_完整算法研发与正式实验.md",
                         "04_独立科学验证.md", "05_论文撰写与投稿.md"):
            doc = (ROOT/filename).read_text(encoding="utf-8")
            self.assertIn("v6.", doc)
            self.assertNotIn("**触发**：必做", doc)
        self.assertIn("不要求先执行04-D", (ROOT/"05_论文撰写与投稿.md").read_text(encoding="utf-8"))
        state = (ROOT/"templates/STATE.md").read_text(encoding="utf-8")
        self.assertIn("DECISION_REUSE_KEYS:", state)
        self.assertIn("user_message_reference", state)

    def test_revgraph_value_lesson_is_integrated_without_new_gate(self):
        lesson = (ROOT/"LESSONS.md").read_text(encoding="utf-8")
        guide = (ROOT/"ORCHESTRATOR.md").read_text(encoding="utf-8")
        pilot = (ROOT/"02_最小科学验证与决策.md").read_text(encoding="utf-8")
        for token in ("成功价值反推", "代理指标", "最近邻", "VALUE_UNVERIFIED"):
            self.assertIn(token, lesson)
        self.assertIn("VALUE_UNVERIFIED", guide)
        self.assertIn("VALUE_UNVERIFIED", pilot)
        self.assertIn("PROXY_ONLY_GAIN", (ROOT/"ROUTES.json").read_text(encoding="utf-8"))
        advice = router.advise_event("PROXY_ONLY_GAIN")
        self.assertEqual(advice["action"], "CHECK_SCIENTIFIC_VALUE")
        self.assertEqual(advice["route"], "03-D")
        self.assertEqual(advice["permission"], "ADVISORY_ONLY_NO_EXECUTION")
        self.assertEqual(json.loads((ROOT/"ROUTES.json").read_text(encoding="utf-8"))["default_path"]["mandatory_scenes"], [])
        self.assertEqual(len(router.load_routes()), 24)

    def test_human_gates_preserved(self):
        s=(ROOT/"ORCHESTRATOR.md").read_text(encoding="utf-8")
        for token in ("WAITING_FOR_USER_DECISION","GPU","P1/P2/P3","真实新消息"):
            self.assertIn(token,s)
        self.assertIn("GitHub", (ROOT/"START.md").read_text(encoding="utf-8"))

    def test_hfd_value_first_regression_without_new_mandatory_gates(self):
        root=ROOT
        guide=(root/"ORCHESTRATOR.md").read_text(encoding="utf-8")
        lesson=(root/"LESSONS.md").read_text(encoding="utf-8")
        pilot=(root/"02_最小科学验证与决策.md").read_text(encoding="utf-8")
        repair=(root/"RECOVERY.md").read_text(encoding="utf-8")
        triage=(root/"TRIAGE.md").read_text(encoding="utf-8")
        self.assertIn("修好后",guide)
        self.assertIn("真实数据",guide)
        self.assertIn("INCONCLUSIVE",guide)
        self.assertIn("HFD",lesson)
        self.assertIn("分辨率≠MDD",lesson)
        self.assertIn("INCONCLUSIVE",pilot)
        self.assertIn("RESEARCH_VALUE_LOW",pilot)
        self.assertIn("VALUE_CHECK",repair)
        self.assertIn("不是第四级缺陷",triage)
        self.assertLess(len(guide),2800)
        self.assertEqual(len(router.load_routes()),24)
        self.assertEqual(sum(len(v) for v in router.load_repairs()[1].values()),48)
        self.assertEqual(set(router.load_triage()["levels"]),{"CRITICAL","REPAIRABLE","MINOR"})
        for event,action,route in (
            ("CLAIM_NO_NOVEL_DELTA","REASSESS_CLAIM_VALUE","01-B"),
            ("DATA_WAITING_AUTH","REQUEST_DATA_ONCE","02-B"),
            ("REPAIR_LOW_VALUE","STOP_REPAIR_SCOPE","03-E"),
            ("INCONCLUSIVE_LOW_VALUE","ADVISE_HOLD_OR_STOP","02-D")):
            advice=router.advise_event(event)
            self.assertEqual((advice["action"],advice["route"]),(action,route))
            self.assertEqual(advice["permission"],"ADVISORY_ONLY_NO_EXECUTION")
        self.assertEqual(router.propose_transition("REPAIRABLE","FORMAL_RUN",
                         scoped_work_verified=True),"INDEPENDENT_EVIDENCE_OR_APPROVAL_GATE")
        self.assertEqual(router.propose_transition("UNKNOWN","SCOPED_EXPLORATION"),
                         "NEEDS_MINIMAL_EVIDENCE_CHECK")


if __name__=="__main__":
    unittest.main()

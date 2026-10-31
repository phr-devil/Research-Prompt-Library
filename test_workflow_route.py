"""v6 scientific routing, evidence and authorization regression tests."""
import importlib.util
import subprocess
import sys
import tempfile
import json
import os
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

    def test_operational_event_contracts_are_safe_and_specific(self):
        mapping = {
            "MODEL_DESIGN": ("playbooks/02_BUILD_DEBUG.md", "03-A"),
            "BASELINE_REPRO_FAIL": ("playbooks/01_DATA_BASELINE.md", "02-B"),
            "TRAINING_FAILURE": ("playbooks/02_BUILD_DEBUG.md", "03-E"),
            "ABLATION_CONFOUND": ("playbooks/03_EXPERIMENT_LOOP.md", "03-D"),
            "STATISTICAL_INCONCLUSIVE": ("playbooks/03_EXPERIMENT_LOOP.md", "03-D"),
            "CLAIM_EVIDENCE_MISMATCH": ("playbooks/04_EVIDENCE_CONFIRM.md", "04-A"),
            "CONFIRMATION_LEAK": ("playbooks/04_EVIDENCE_CONFIRM.md", "03-F"),
        }
        for event, (book, route) in mapping.items():
            advice = router.advise_event(event)
            self.assertEqual((advice["playbook"], advice["route"]), (book, route))
            self.assertEqual(advice["permission"], "ADVISORY_ONLY_NO_EXECUTION")
            for key, label in (("deliverable", "DELIVERABLE"), ("verify", "VERIFY"),
                               ("boundary", "BOUNDARY")):
                self.assertTrue(advice[key].strip())
                self.assertIn(label + ":", router.render_event(event))
            self.assertTrue(router.resolve_playbook(book).is_file())
        for event in ("DATA_AUDIT", "IMPLEMENTATION", "EXPERIMENT", "EVIDENCE_AUDIT", "RESUME"):
            self.assertIn("DELIVERABLE:", router.render_event(event))
        self.assertEqual(len(router.load_routes()), 24)
        guide=(ROOT/"ORCHESTRATOR.md").read_text(encoding="utf-8")
        post=(ROOT/"POST_SELECTION.md").read_text(encoding="utf-8")
        self.assertLess(len(guide), 2800)
        self.assertIn("自主执行规则", guide)
        self.assertIn("TRAINING_FAILURE", post)
        self.assertIn("CONFIRMATION_LEAK", post)
        self.assertIn("不是新阶段", post)

    def test_operational_event_cli_is_advisory_not_executor(self):
        p = subprocess.run([sys.executable, str(ROOT/"workflow_route.py"), "--event",
                            "CLAIM_EVIDENCE_MISMATCH"], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("DELIVERABLE:", p.stdout)
        self.assertIn("VERIFY:", p.stdout)
        self.assertIn("BOUNDARY:", p.stdout)
        self.assertIn("Advisory only", p.stdout)

    def test_compact_playbooks_have_actionable_scientific_recipes(self):
        """Compact guidance must still cover design, validation, diagnosis, and paper claims."""
        required = {
            "01_DATA_BASELINE.md": ("强基线复现合同", "train-only", "sample_id",
                                     "STRONG_BASELINE_NOT_REPRODUCED", "REFORMS"),
            "02_BUILD_DEBUG.md": ("模块级实现合同", "关键行为测试矩阵", "训练症状",
                                   "Loss", "tiny-set", "ENGINEERING_VALID"),
            "03_EXPERIMENT_LOOP.md": ("实验选择与计算预算", "scientific", "nuisance",
                                      "fixed", "SESOI/MDE", "INCONCLUSIVE"),
            "04_EVIDENCE_CONFIRM.md": ("证据预审", "封闭确认评价",
                                       "SCIENTIFICALLY_SUPPORTED", "CONFIRMATION_UNAVAILABLE")
        }
        playbooks = ROOT/"playbooks"
        for filename, terms in required.items():
            document=(playbooks/filename).read_text(encoding="utf-8")
            self.assertLess(len(document), 2700, filename)
            for term in terms:
                self.assertIn(term, document, (filename, term))
            self.assertIn("何时读", document)
        self.assertEqual(len(router.load_routes()), 24)
        self.assertIn("按问题只读一份",
                      (ROOT/"POST_SELECTION.md").read_text(encoding="utf-8"))

    def test_lightweight_paper_feedback_keeps_existing_workflow(self):
        funnel=(ROOT/"IDEA_FUNNEL.md").read_text(encoding="utf-8")
        post=(ROOT/"POST_SELECTION.md").read_text(encoding="utf-8")
        lessons=(ROOT/"LESSONS.md").read_text(encoding="utf-8")
        writing=(ROOT/"05_论文撰写与投稿.md").read_text(encoding="utf-8")
        state=(ROOT/"templates"/"STATE.md").read_text(encoding="utf-8")
        self.assertIn("论文组合适配（轻量判断，非配额）", funnel)
        self.assertIn("相关失败风险", funnel)
        self.assertIn("F5仍由用户选题", funnel)
        self.assertIn("论文证据草图（按事件触发，不是新阶段）", post)
        self.assertIn("首次取得可核实的有效科学结果", post)
        self.assertIn("只有用户要求写稿时才进入", post)
        self.assertIn("PAPER_ROUTE/REUSE_ONLY", lessons)
        self.assertIn("不把同一份结果拆成", lessons)
        self.assertIn("论文证据随研同步", writing)
        self.assertIn("贡献类型与目标读者", writing)
        for status in ("NO_INDEPENDENT_CLAIM", "CLAIM_WITH_EVIDENCE_GAPS",
                       "DRAFTABLE", "SUBMISSION_CANDIDATE"):
            self.assertIn(status, state)
        self.assertIn("不等于已独立审核", state)
        self.assertEqual(len(router.load_routes()), 24)
        doc=json.loads((ROOT/"ROUTES.json").read_text(encoding="utf-8"))
        self.assertEqual(doc["default_path"]["mandatory_scenes"], [])

    def test_evidence_first_research_decision_contract_is_actionable(self):
        funnel=(ROOT/"IDEA_FUNNEL.md").read_text(encoding="utf-8")
        data=(ROOT/"playbooks"/"01_DATA_BASELINE.md").read_text(encoding="utf-8")
        design=(ROOT/"playbooks"/"ALGORITHM_DESIGN_REFERENCE.md").read_text(encoding="utf-8")
        experiment=(ROOT/"playbooks"/"03_EXPERIMENT_LOOP.md").read_text(encoding="utf-8")
        post=(ROOT/"POST_SELECTION.md").read_text(encoding="utf-8")
        for phrase in ("F4 反向论文审查", "最近邻反驳", "可检验性反驳",
                       "最致命实验", "F5 仍由用户决定"):
            self.assertIn(phrase, funnel)
        for phrase in ("性能空间诊断", "B_strong", "O_reference", "O_UNKNOWN",
                       "没有最优性证明的 Oracle 不是数学上界", "离线遮蔽",
                       "同一开发协议"):
            self.assertIn(phrase, data)
        for phrase in ("有限机制竞争", "M0", "M1", "M2", "决策前可见信息相同",
                       "删除条件"):
            self.assertIn(phrase, design)
        for phrase in ("自适应 GPU 验证", "最佳开发 checkpoint", "nuisance",
                       "缺授权不启动", "GPU 利用率不是科学 KPI", "超范围需重新获批"):
            self.assertIn(phrase, experiment)
        self.assertIn("选题后的证据优先决策", post)
        self.assertIn("一轮只交付一条决策记录", post)
        self.assertLess(len(data), 2700)
        self.assertLess(len(design), 3000)
        self.assertLess(len(experiment), 2700)
        self.assertEqual(len(router.load_routes()), 24)

    def test_post_selection_tool_table_is_not_split_by_prose(self):
        post=(ROOT/"POST_SELECTION.md").read_text(encoding="utf-8")
        table=post.split("## 按“下一项需要解决什么”加载一份技术手册",1)[1]
        table=table.split("**技术参考按需加载**",1)[0]
        nonempty=[line.strip() for line in table.splitlines() if line.strip()]
        self.assertEqual(len(nonempty), 7)  # header, separator, five actual rows
        self.assertTrue(all(line.startswith("|") and line.endswith("|")
                            for line in nonempty))
        self.assertEqual(len([line for line in nonempty if "playbooks/" in line]), 5)

    def test_algorithm_contract_template_requires_real_adapter_and_compiles(self):
        """A prompt-library CI pass must not masquerade as a real-model correctness pass."""
        tpl = ROOT/"templates"/"test_algorithm_contract.py"
        content=tpl.read_text(encoding="utf-8")
        compile(content, str(tpl), "exec")
        self.assertIn("test_l2_reference_parity", content)
        self.assertIn("test_l2_gradcheck_custom_differentiable_op", content)
        self.assertIn("test_l3_backward_and_optimizer_update", content)
        self.assertIn("test_l4_eval_checkpoint_roundtrip", content)
        self.assertIn("test_sensor_temporal_and_mask_invariance", content)
        self.assertNotIn("cuda()", content)
        env=os.environ.copy()
        env.pop("ALGORITHM_CONTRACT_ADAPTER", None)
        proc=subprocess.run([sys.executable, str(tpl)], capture_output=True, text=True, env=env)
        self.assertEqual(proc.returncode, 2)
        self.assertIn("CONTRACT_NOT_CONFIGURED", proc.stderr)
        self.assertIn("ALGORITHM_CONTRACT_ADAPTER", proc.stderr)

    def test_algorithm_contract_rejects_incomplete_adapter(self):
        tpl=ROOT/"templates"/"test_algorithm_contract.py"
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "incomplete_adapter.py").write_text("def make_case(): pass\n", encoding="utf-8")
            env=os.environ.copy()
            env["ALGORITHM_CONTRACT_ADAPTER"]="incomplete_adapter"
            env["PYTHONPATH"]=tmp+os.pathsep+env.get("PYTHONPATH", "")
            proc=subprocess.run([sys.executable, str(tpl)], capture_output=True, text=True, env=env)
            self.assertEqual(proc.returncode, 2)
            self.assertIn("Adapter missing:", proc.stderr)

    def test_algorithm_reference_routes_are_opt_in_and_sensor_specific(self):
        play=ROOT/"playbooks"
        design=(play/"ALGORITHM_DESIGN_REFERENCE.md").read_text(encoding="utf-8")
        sensor=(play/"SENSOR_DIAGNOSTICS.md").read_text(encoding="utf-8")
        runner=(ROOT/"templates"/"ALGORITHM_TEST_USAGE.md").read_text(encoding="utf-8")
        build=(play/"02_BUILD_DEBUG.md").read_text(encoding="utf-8")
        post=(ROOT/"POST_SELECTION.md").read_text(encoding="utf-8")
        self.assertLess(len(build), 2700)
        self.assertLess(len(design), 3000)
        self.assertLess(len(sensor), 2300)
        for term in ("Ridge", "TCN", "GRU", "Transformer", "Loss", "关键反证", "成本与删除"):
            self.assertIn(term, design)
        for term in ("时间戳", "异步", "缺失模态", "动态启用", "训练诊断", "INCONCLUSIVE"):
            self.assertIn(term, sensor)
        for term in ("make_case", "assert_contract", "ALGORITHM_CONTRACT_ADAPTER",
                     "SKIP", "真实", "CPU"):
            self.assertIn(term, runner)
        for filename in ("ALGORITHM_DESIGN_REFERENCE.md", "SENSOR_DIAGNOSTICS.md",
                         "test_algorithm_contract.py", "ALGORITHM_TEST_USAGE.md"):
            self.assertIn(filename, build+post)
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



class EvidenceSourceAuditTests(unittest.TestCase):
    """No GPU, no network, only synthetic local fixtures to catch phantom evidence."""

    def setUp(self):
        self._temp = tempfile.TemporaryDirectory()
        self.addCleanup(self._temp.cleanup)
        self.root = Path(self._temp.name)
        (self.root / "research").mkdir()
        (self.root / "results").mkdir()
        self.script = ROOT.parent.parent / "research_tools" / "audit_evidence.py"
        self.fields = ["run_id", "metric", "value", "status", "evidence_path",
                       "data_version", "split", "seed", "protocol_sha", "config_sha",
                       "n_units", "statistical_unit", "metric_unit"]
        self.row = dict(run_id="R1", metric="ap", value="0.812", status="KEEP",
                        evidence_path="results/eval.json", data_version="d1",
                        split="val", seed="0", protocol_sha="p1", config_sha="c1",
                        n_units="10", statistical_unit="episode", metric_unit="AP")
        self.result = dict(run_id="R1", metrics={"ap": 0.812},
                           data_version="d1", split="val", seed="0",
                           protocol_sha="p1", config_sha="c1",
                           n_units="10", statistical_unit="episode",
                           metric_unit="AP")
        self.save_rows([self.row])
        self.save_source(self.result)
        self.save_claims([{"claim_id": "C1", "run_id": "R1", "metric": "ap",
                           "reported_value": 0.812}])

    def save_rows(self, rows):
        import csv
        with (self.root / "research/RUNS.tsv").open("w", encoding="utf-8", newline="") as out:
            writer = csv.DictWriter(out, fieldnames=self.fields, delimiter="\t")
            writer.writeheader()
            writer.writerows(rows)

    def save_source(self, value):
        (self.root / "results/eval.json").write_text(json.dumps(value), encoding="utf-8")

    def save_claims(self, claims):
        (self.root / "research/claims_audit.json").write_text(
            json.dumps({"claims": claims}), encoding="utf-8")

    def invoke(self, *args):
        proc = subprocess.run([sys.executable, str(self.script), "--root",
                               str(self.root), "--runs", "research/RUNS.tsv",
                               "--claims", "research/claims_audit.json", *args],
                              capture_output=True, text=True)
        return proc, json.loads(proc.stdout if proc.stdout else proc.stderr)

    def test_real_source_and_claim_number_match_without_science_acquittal(self):
        proc, out = self.invoke()
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(out["verdict"], "SOURCE_CHECK_COMPLETE")
        self.assertEqual(out["runs"][0]["status"], "SOURCE_MATCH")
        self.assertEqual(out["claims"][0]["status"], "SOURCE_MATCH_NOT_SCIENCE_REVIEW")
        self.assertEqual(len(out["runs"][0]["identity_checked"]), 8)
        self.assertIn("NOT_SCIENTIFIC_VALIDITY", out["scope"])

    def test_false_run_number_is_not_found_in_unrelated_value(self):
        self.save_source(dict(run_id="R1", metrics={"other": 0.812}, note="ap 0.812"))
        proc, out = self.invoke()
        self.assertEqual(proc.returncode, 1)
        self.assertEqual(out["runs"][0]["status"], "UNVERIFIED")
        self.assertIn("named metric absent", out["runs"][0]["reason"])

    def test_tampered_number_and_fabricated_claim_fail(self):
        self.save_source(dict(self.result, metrics={"ap": 0.7}))
        proc, out = self.invoke()
        self.assertEqual(proc.returncode, 1)
        self.assertIn("mismatch", out["runs"][0]["reason"])
        self.save_source(self.result)
        self.save_claims([{"claim_id": "C1", "run_id": "R1", "metric": "ap",
                           "reported_value": 0.99}])
        proc, out = self.invoke()
        self.assertEqual(proc.returncode, 1)
        self.assertIn("differs", out["claims"][0]["reason"])

    def test_protocol_data_identity_mismatch_is_not_source_verified(self):
        self.save_source(dict(self.result, protocol_sha="different"))
        proc, out = self.invoke()
        self.assertEqual(proc.returncode, 1)
        self.assertIn("protocol_sha", out["runs"][0]["reason"])

    def test_missing_embedded_metadata_is_reported_not_invented(self):
        self.save_source({"run_id": "R1", "metrics": {"ap": 0.812}})
        proc, out = self.invoke()
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(out["runs"][0]["status"], "SOURCE_MATCH")
        self.assertIn("protocol_sha", out["runs"][0]["identity_not_embedded"])

    def test_strict_identity_rejects_partially_grounded_source(self):
        self.save_source({"run_id": "R1", "metrics": {"ap": 0.812}})
        loose, out = self.invoke()
        self.assertEqual(loose.returncode, 0)
        self.assertEqual(out["runs"][0]["identity_scope"], "PARTIAL")
        strict, out = self.invoke("--require-identity")
        self.assertEqual(strict.returncode, 1)
        self.assertEqual(out["runs"][0]["status"], "UNVERIFIED")
        self.assertIn("incomplete identity provenance", out["runs"][0]["reason"])
        self.save_source(self.result)
        strict, out = self.invoke("--require-identity")
        self.assertEqual(strict.returncode, 0)
        self.assertEqual(out["runs"][0]["identity_scope"], "COMPLETE")

    def test_all_historical_invalid_runs_do_not_produce_empty_success(self):
        self.save_rows([dict(self.row, status="INVALID")])
        self.save_claims([])
        proc, out = self.invoke()
        self.assertEqual(proc.returncode, 1)
        self.assertEqual(out["verdict"], "UNVERIFIED")
        self.assertEqual(out["summary"]["run_source_matches"], 0)

    def test_invalid_history_cannot_support_claim(self):
        self.save_rows([dict(self.row, status="INVALID")])
        proc, out = self.invoke()
        self.assertEqual(proc.returncode, 1)
        self.assertEqual(out["runs"][0]["status"], "HISTORICAL_NOT_ELIGIBLE")
        self.assertEqual(out["claims"][0]["status"], "UNVERIFIED")

    def test_unknown_status_and_duplicate_run_id_fail_closed(self):
        self.save_rows([dict(self.row, status="UNKNOWN")])
        proc, out = self.invoke()
        self.assertEqual(proc.returncode, 1)
        self.assertIn("unknown", out["runs"][0]["reason"])
        self.save_rows([self.row, self.row])
        proc, out = self.invoke()
        self.assertEqual(proc.returncode, 1)
        self.assertIn("duplicate", out["runs"][1]["reason"])

    def test_source_must_be_inside_project(self):
        self.save_rows([dict(self.row, evidence_path="../../secret.json")])
        proc, out = self.invoke()
        self.assertEqual(proc.returncode, 1)
        self.assertIn("traversing", out["runs"][0]["reason"])
        self.save_rows([dict(self.row, evidence_path="/etc/passwd")])
        proc, out = self.invoke()
        self.assertEqual(proc.returncode, 1)
        self.assertIn("absolute", out["runs"][0]["reason"])

    def test_empty_runs_and_ambiguous_tabular_source_are_not_verified(self):
        self.save_rows([])
        proc, out = self.invoke()
        self.assertEqual(proc.returncode, 2)
        self.assertIn("no experiment records", out["error"])
        self.save_rows([dict(self.row, evidence_path="results/table.csv")])
        (self.root / "results/table.csv").write_text("metric,value\nap,0.812\nap,0.812\n", encoding="utf-8")
        proc, out = self.invoke()
        self.assertEqual(proc.returncode, 1)
        self.assertIn("exactly one run", out["runs"][0]["reason"])

    def test_new_report_only_and_no_external_mutation(self):
        proc, out = self.invoke("--output", "research/audit.json")
        self.assertEqual(proc.returncode, 0)
        written = (self.root / "research/audit.json").read_text(encoding="utf-8")
        self.assertIn("SOURCE_CHECK_COMPLETE", written)
        proc, out = self.invoke("--output", "research/audit.json")
        self.assertEqual(proc.returncode, 2)
        self.assertIn("File exists", out["error"])

    def test_p0_playbook_contracts_and_legacy_fast_path(self):
        play = ROOT / "playbooks"
        specs = [
            ("01_DATA_BASELINE.md", ["强基线复现合同", "STRONG_BASELINE_NOT_REPRODUCED"]),
            ("02_BUILD_DEBUG.md", ["模块级实现合同", "关键行为测试矩阵", "训练症状"]),
            ("03_EXPERIMENT_LOOP.md", ["实验选择与计算预算", "SESOI/MDE", "INCONCLUSIVE"]),
            ("04_EVIDENCE_CONFIRM.md", ["证据预审", "封闭确认评价", "SCIENTIFICALLY_SUPPORTED"])
        ]
        for file, tokens in specs:
            doc = (play / file).read_text(encoding="utf-8")
            for token in tokens:
                self.assertIn(token, doc, (file, token))
        self.assertEqual(len(router.load_routes()), 24)


if __name__=="__main__":
    unittest.main()

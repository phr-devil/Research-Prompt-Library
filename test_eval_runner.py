"""Smoke tests only: mock responses are NOT actual model quality results."""
import contextlib,csv,io,json,os,subprocess,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import eval_runner as m
class EvalHarnessTest(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.repo=Path(self.tmp.name)
        (self.repo/"docs").mkdir()
        (self.repo/"LIBRARY_INDEX.json").write_text(json.dumps([{"id":"R02","file":"docs/R02.md"}]),encoding="utf-8")
        (self.repo/"EVAL_CASES.json").write_text(json.dumps({"cases":[{
            "id":"T03","prompt_id":"R02","input":"Check results","must":["value","uncertainty"],"critical":["invented approval"]}]}),encoding="utf-8")
        subprocess.run(["git","init","-q",str(self.repo)],check=True)
        subprocess.run(["git","-C",str(self.repo),"config","user.email","fixture@example.invalid"],check=True)
        subprocess.run(["git","-C",str(self.repo),"config","user.name","Test"],check=True)
        self.base=self.commit("BASE")
        self.candidate=self.commit("CANDIDATE")
        self.out=self.repo/"private"
    def tearDown(self):self.tmp.cleanup()
    def commit(self,label):
        fence=chr(96)*3
        data="## 可直接复制的 Prompt\n\n"+fence+"text\n"+label+" — "+"Keep scientific results unchanged. "*8+"\n"+fence+"\n"
        (self.repo/"docs/R02.md").write_text(data,encoding="utf-8")
        subprocess.run(["git","-C",str(self.repo),"add","."],check=True)
        subprocess.run(["git","-C",str(self.repo),"commit","-qm",label],check=True)
        return subprocess.check_output(["git","-C",str(self.repo),"rev-parse","HEAD"],text=True).strip()
    def args(self,extra):
        return ["eval_runner.py","--repo",str(self.repo),"--base-ref",self.base,
                "--candidate-ref",self.candidate,"--output-dir",str(self.out),
                "--cases","T03"]+extra
    def call(self,extra):
        with patch.object(sys,"argv",self.args(extra)),contextlib.redirect_stdout(io.StringIO()):
            m.main()
    def test_git_pins(self):
        self.assertTrue(m.prompt(self.repo,self.base,"docs/R02.md").startswith("BASE"))
        self.assertTrue(m.prompt(self.repo,self.candidate,"docs/R02.md").startswith("CANDIDATE"))
        with self.assertRaises(ValueError):m.prompt(self.repo,"main","docs/R02.md")
    def test_endpoint_rejects_plain_external_http(self):
        with self.assertRaises(ValueError):m.endpoint("http://example.net/v1")
        self.assertTrue(m.endpoint("http://127.0.0.1:11434/v1").endswith("/chat/completions"))
    def test_plan_is_offline(self):
        with patch.object(m,"invoke",side_effect=AssertionError("No model calls in dry-run")):
            self.call([])
        self.assertEqual(m.read(self.out/"manifest.json")["status"],"PLAN_ONLY")
        self.assertEqual(len(m.read(self.out/"plan.json")),2)
    def test_default_pilot_is_loaded_from_target_repo(self):
        # Regression: --repo must not silently select pilot IDs from the runner's checkout.
        fixture=m.read(self.repo/"EVAL_CASES.json")
        fixture["pilot_ids"]=["T03"]
        m.save(self.repo/"EVAL_CASES.json",fixture)
        argv=self.args([])
        i=argv.index("--cases")
        del argv[i:i+2]
        with patch.object(sys,"argv",argv),contextlib.redirect_stdout(io.StringIO()):
            m.main()
        self.assertEqual(m.read(self.out/"manifest.json")["selected_cases"],["T03"])
        self.assertEqual(len(m.read(self.out/"plan.json")),2)

    def test_empty_rubric_fails_before_outputs(self):
        fixture=m.read(self.repo/"EVAL_CASES.json")
        fixture["cases"][0]["must"]=[]
        m.save(self.repo/"EVAL_CASES.json",fixture)
        with self.assertRaisesRegex(ValueError,"Invalid cases fixture"):
            self.call([])
        self.assertFalse(self.out.exists())

    def test_unknown_prompt_id_fails_before_outputs(self):
        fixture=m.read(self.repo/"EVAL_CASES.json")
        fixture["cases"][0]["prompt_id"]="MISSING"
        m.save(self.repo/"EVAL_CASES.json",fixture)
        with self.assertRaisesRegex(ValueError,"unknown prompt_id"):
            self.call([])
        self.assertFalse(self.out.exists())

    def test_all_and_cases_cannot_silently_conflict(self):
        with self.assertRaisesRegex(ValueError,"Choose --all or --cases"):
            self.call(["--all"])
        self.assertFalse(self.out.exists())

    def test_call_cap_prevents_overuse(self):
        with self.assertRaises(ValueError):self.call(["--repeat","5","--max-calls","8"])
    def test_live_requires_credential(self):
        with patch.dict(os.environ,{"OPENAI_API_KEY":""}):
            with self.assertRaises(ValueError):self.call(["--live","--model","test"])
        self.assertFalse((self.out/"raw_responses.jsonl").exists())
    def test_mock_client_needs_blind_review(self):
        with patch.dict(os.environ,{"OPENAI_API_KEY":"DUMMY"}):
            with patch.object(m,"invoke",return_value=("MOCK ONLY",{"prompt_tokens":7,"completion_tokens":3,"total_tokens":10},{"model":"mock-model","finish_reason":"stop"})):
                self.call(["--live","--model","mock-model"])
        self.assertEqual(m.read(self.out/"manifest.json")["status"],"MODEL_OUTPUTS_UNSCORED")
        with self.assertRaises(ValueError):self.call(["--score"])
        with (self.out/"blind_review.csv").open(encoding="utf-8-sig",newline="") as f: rows=list(csv.DictReader(f))
        self.assertEqual(len(rows),2)
        self.assertTrue(all("version" not in row for row in rows))
        for row in rows:row.update(must_pass_count="2",critical_error_0_or_1="0")
        with (self.out/"blind_review.csv").open("w",encoding="utf-8-sig",newline="") as f:
            w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
        self.call(["--score"])
        self.assertEqual(m.read(self.out/"scores.json")["baseline"]["full_pass"],1)
        self.assertEqual(m.read(self.out/"scores.json")["candidate"]["measured_total_tokens"],10)

    def test_prevents_overwriting_existing_results(self):
        self.out.mkdir(exist_ok=True)
        p=self.out/"manifest.json"
        p.write_text("ORIGINAL",encoding="utf-8")
        with self.assertRaisesRegex(ValueError,"not empty"):
            self.call([])
        self.assertEqual(p.read_text(encoding="utf-8"),"ORIGINAL")

    def test_live_missing_key_does_not_create_run(self):
        with patch.dict(os.environ,{"OPENAI_API_KEY":""}):
            with self.assertRaises(ValueError):
                self.call(["--live","--model","test"])
        self.assertFalse(self.out.exists())

    def test_rejects_identical_compared_revisions(self):
        with self.assertRaisesRegex(ValueError,"must differ"):
            self.call(["--candidate-ref",self.base])

    def run_mock(self):
        with patch.dict(os.environ,{"OPENAI_API_KEY":"DUMMY"}):
            with patch.object(m,"invoke",return_value=("MOCK ONLY",{"prompt_tokens":7,"completion_tokens":3,"total_tokens":10},{"model":"mock-model","finish_reason":"stop"})):
                self.call(["--live","--model","mock-model"])
        with (self.out/"blind_review.csv").open(encoding="utf-8-sig",newline="") as f:
            rows=list(csv.DictReader(f))
        for row in rows:
            row.update(must_pass_count="2",critical_error_0_or_1="0")
        return rows

    def set_review(self,rows):
        with (self.out/"blind_review.csv").open("w",encoding="utf-8-sig",newline="") as f:
            w=csv.DictWriter(f,fieldnames=rows[0].keys())
            w.writeheader();w.writerows(rows)

    def test_duplicate_review_ids_fail_closed(self):
        rows=self.run_mock()
        rows[1]["blind_id"]=rows[0]["blind_id"]
        self.set_review(rows)
        with self.assertRaisesRegex(ValueError,"Duplicate"):
            self.call(["--score"])
        self.assertFalse((self.out/"scores.json").exists())

    def test_modified_response_fail_closed(self):
        rows=self.run_mock()
        rows[0]["response"]="INJECTED ANSWER"
        self.set_review(rows)
        with self.assertRaisesRegex(ValueError,"altered"):
            self.call(["--score"])
        self.assertFalse((self.out/"scores.json").exists())

    def test_modified_test_rubric_fail_closed(self):
        rows=self.run_mock()
        self.set_review(rows)
        p=self.repo/"EVAL_CASES.json"
        data=json.loads(p.read_text(encoding="utf-8"))
        data["cases"][0]["must"].append("ADDED AFTER INFERENCE")
        p.write_text(json.dumps(data),encoding="utf-8")
        with self.assertRaisesRegex(ValueError,"rubric changed"):
            self.call(["--score"])
        self.assertFalse((self.out/"scores.json").exists())

    def test_rejects_unchanged_prompt_text_by_default(self):
        with patch.object(m,"prompt",return_value="IDENTICAL PROMPT "*40):
            with self.assertRaisesRegex(ValueError,"identical"):
                self.call([])
        self.assertFalse(self.out.exists())

    def test_allows_explicit_unchanged_control(self):
        with patch.object(m,"prompt",return_value="IDENTICAL PROMPT "*40):
            self.call(["--allow-unchanged-controls"])
        manifest=m.read(self.out/"manifest.json")
        self.assertEqual(manifest["unchanged_control_cases"],["T03"])
        self.assertEqual(manifest["status"],"PLAN_ONLY")

    def test_rejects_model_api_redirect(self):
        with self.assertRaisesRegex(ValueError,"redirect rejected"):
            m.RejectRedirect().redirect_request(None,None,302,"Moved",{},"https://other.example/v1")


    def test_pairwise_summary_records_wins_and_ties(self):
        rows=self.run_mock()
        self.set_review(rows)
        self.call(["--score"])
        summary=m.read(self.out/"scores.json")["paired_summary"]
        self.assertEqual(summary,{"n_pairs":1,"candidate_only":0,"baseline_only":0,
                                  "both_pass":1,"both_fail":0})
        result=m.read(self.out/"scores.json")
        self.assertEqual(result["baseline"]["measured_prompt_tokens"],7)
        self.assertEqual(result["candidate"]["measured_completion_tokens"],3)

    def test_truncated_model_response_is_not_scored(self):
        with patch.dict(os.environ,{"OPENAI_API_KEY":"DUMMY"}):
            with patch.object(m,"invoke",return_value=("CUT OFF",{"total_tokens":10},
                     {"model":"mock-model","finish_reason":"length"})):
                with self.assertRaisesRegex(ValueError,"not normally completed"):
                    self.call(["--live","--model","mock-model"])
        manifest=m.read(self.out/"manifest.json")
        self.assertEqual(manifest["status"],"FAILED_OR_INCOMPLETE")
        self.assertEqual(manifest["actual_calls"],1)
        self.assertFalse((self.out/"scores.json").exists())
        with self.assertRaisesRegex(ValueError,"No completed"):
            self.call(["--score"])

    def test_abnormal_finish_reason_aborts_live_run(self):
        with patch.dict(os.environ,{"OPENAI_API_KEY":"DUMMY"}):
            with patch.object(m,"invoke",return_value=("FILTERED",{"total_tokens":10},
                     {"model":"mock-model","finish_reason":"content_filter"})):
                with self.assertRaisesRegex(ValueError,"not normally completed"):
                    self.call(["--live","--model","mock-model"])
        self.assertEqual(m.read(self.out/"manifest.json")["status"],"FAILED_OR_INCOMPLETE")
        self.assertFalse((self.out/"scores.json").exists())

    def test_score_rejects_abnormal_finish_reason(self):
        rows=self.run_mock()
        self.set_review(rows)
        path=self.out/"raw_responses.jsonl"
        records=[json.loads(s) for s in path.read_text(encoding="utf-8").splitlines()]
        records[0]["model_meta"]["finish_reason"]="content_filter"
        path.write_text("".join(json.dumps(v)+chr(10) for v in records),encoding="utf-8")
        with self.assertRaisesRegex(ValueError,"Incomplete"):
            self.call(["--score"])
        self.assertFalse((self.out/"scores.json").exists())

    def test_score_rejects_mixed_observed_models(self):
        rows=self.run_mock()
        self.set_review(rows)
        path=self.out/"raw_responses.jsonl"
        records=[json.loads(s) for s in path.read_text(encoding="utf-8").splitlines()]
        records[0]["model_meta"]["model"]="other-backend"
        path.write_text("".join(json.dumps(v)+chr(10) for v in records),encoding="utf-8")
        with self.assertRaisesRegex(ValueError,"Model identity changed"):
            self.call(["--score"])
        self.assertFalse((self.out/"scores.json").exists())

    def test_invoke_rejects_missing_finish_reason(self):
        import urllib.request
        class FakeResponse:
            def __enter__(self):return self
            def __exit__(self,*args):return False
            def read(self):return json.dumps({"choices":[{"message":{"content":"x"},"finish_reason":None}]}).encode()
        with patch.object(urllib.request.OpenerDirector,"open",return_value=FakeResponse()):
            with self.assertRaisesRegex(ValueError,"did not finish normally"):
                m.invoke("https://example.org/v1/chat/completions","dummy","model","system","task",100)

    def test_temperature_config_is_recorded(self):
        self.call(["--temperature","0"])
        mfest=m.read(self.out/"manifest.json")
        self.assertEqual(mfest["temperature"],0.0)
        self.assertEqual(mfest["status"],"PLAN_ONLY")

    def test_invalid_temperature_rejected_before_write(self):
        with self.assertRaisesRegex(ValueError,"Temperature"):
            self.call(["--temperature","2.5"])
        self.assertFalse(self.out.exists())

    def test_reviewer_mapping_repeat_tamper_rejected(self):
        rows=self.run_mock()
        self.set_review(rows)
        p=self.out/"private_mapping.json"
        mapping=m.read(p)
        first=next(iter(mapping))
        mapping[first]["repeat"]=99
        m.save(p,mapping)
        with self.assertRaisesRegex(ValueError,"mapping disagrees"):
            self.call(["--score"])
        self.assertFalse((self.out/"scores.json").exists())

if __name__=="__main__":unittest.main()

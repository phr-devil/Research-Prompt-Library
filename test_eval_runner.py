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
    def test_call_cap_prevents_overuse(self):
        with self.assertRaises(ValueError):self.call(["--repeat","5","--max-calls","8"])
    def test_live_requires_credential(self):
        with patch.dict(os.environ,{"OPENAI_API_KEY":""}):
            with self.assertRaises(ValueError):self.call(["--live","--model","test"])
        self.assertFalse((self.out/"raw_responses.jsonl").exists())
    def test_mock_client_needs_blind_review(self):
        with patch.dict(os.environ,{"OPENAI_API_KEY":"DUMMY"}):
            with patch.object(m,"invoke",return_value=("MOCK ONLY",{"total_tokens":10})):
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
if __name__=="__main__":unittest.main()

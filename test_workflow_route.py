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

    def test_human_gates_preserved(self):
        s=(ROOT/"ORCHESTRATOR.md").read_text(encoding="utf-8")
        for token in ("WAITING_FOR_USER_DECISION","GPU","P1/P2/P3","真实新消息"):
            self.assertIn(token,s)
        self.assertIn("GitHub", (ROOT/"START.md").read_text(encoding="utf-8"))


if __name__=="__main__":
    unittest.main()

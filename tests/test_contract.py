"""Standalone PD-RW offline contract checks. No training or network."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ("AGENTS.md","START.md","WORKFLOW.md","README.md","DATA_DISCOVERY.md",
        "SEARCH_DISCOVERY.md","DATA_INSIGHT.md","TASK_EXPLORATION.md","TASK_LADDER.md",
        "EXPERIMENT_LOOP.md","IMPLEMENTATION_GUIDE.md","PAPER_FIRST.md",
        "CONFIRMATION.md","REPLAY_PROTOCOL.md","REFERENCES.md","EXAMPLE_SENSOR.md",
        "templates/STATE.md")

class WorkflowContracts(unittest.TestCase):
    def test_required_files(self):
        for file in DOCS + ("SCENARIOS.json","chapter10_replay.py"):
            self.assertTrue((ROOT / file).is_file(), file)

    def test_local_markdown_links(self):
        for name in DOCS:
            path = ROOT / name
            for dest in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
                if dest.startswith(("http:","https:","mailto:","#")):
                    continue
                relative = dest.split("#", 1)[0]
                self.assertTrue((path.parent / relative).exists(), f"{name} -> {dest}")

    def test_scenarios_have_unique_ids_and_contract(self):
        suite = json.loads((ROOT / "SCENARIOS.json").read_text(encoding="utf-8"))
        cases = suite["cases"]
        self.assertGreaterEqual(len(cases), 50)
        ids = [c["id"] for c in cases]
        self.assertEqual(len(ids), len(set(ids)))
        for case in cases:
            self.assertTrue(all(k in case for k in ("id","event","situation","should","must_not")))

    def test_permissions_and_core_rules(self):
        workflow = (ROOT / "WORKFLOW.md").read_text(encoding="utf-8")
        start = (ROOT / "START.md").read_text(encoding="utf-8")
        for marker in ("STATE","Run","授权","训练"):
            self.assertIn(marker, workflow + start)
        self.assertIn("NOT_RUN", workflow + start)
        self.assertNotIn("../08_算法检验与优化", workflow + start)

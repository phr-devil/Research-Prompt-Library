"""Salvage gate regression tests: never silently skip Step 05 human choice."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

PATH = Path(__file__).resolve().parent / "09_失败算法项目挽救与转向" / "salvage_gate.py"
spec = importlib.util.spec_from_file_location("salvage_gate", PATH)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


class GateTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.candidates = self.root / "05_CANDIDATES.json"
        self.selection = self.root / "05_USER_SELECTION.json"
        self.cards = {"candidates": [
            {"id": i, "title": "Idea " + i, "claim": "Falsifiable " + i,
             "evidence_ids": ["Asset-" + i], "dataset_truth": "Independent labels",
             "closest_work": "Nearest study", "baseline": "Fair baseline",
             "test": "Discriminating check", "cost": "CPU/GPU estimate", "risk": "Failure criterion"}
            for i in ("P1", "P2", "P3")]}
        self.save()

    def save(self):
        self.candidates.write_text(json.dumps(self.cards), encoding="utf-8")

    def select(self, chosen="P2", digest=None):
        if digest is None:
            digest = gate.inspect_candidates(self.candidates)
        self.selection.write_text(json.dumps({
            "selected_id": chosen, "candidate_sha256": digest,
            "user_message": "已审查方案，我选择 " + chosen,
            "user_message_reference": "chat user message after Step 05"}), encoding="utf-8")

    def test_no_selection_is_waiting(self):
        self.assertEqual(gate.inspect_selection(self.candidates, self.selection)[0],
                         "WAITING_FOR_USER_SELECTION")

    def test_exactly_three_required(self):
        self.cards["candidates"].pop()
        self.save()
        with self.assertRaisesRegex(ValueError, "exactly three"):
            gate.inspect_candidates(self.candidates)

    def test_distinct_ids(self):
        self.cards["candidates"][-1]["id"] = "P2"
        self.save()
        with self.assertRaisesRegex(ValueError, "P1/P2/P3"):
            gate.inspect_candidates(self.candidates)

    def test_reject_empty_evidence(self):
        self.cards["candidates"][0]["evidence_ids"] = []
        self.save()
        with self.assertRaisesRegex(ValueError, "evidence"):
            gate.inspect_candidates(self.candidates)

    def test_valid_file_does_not_assert_human_consent(self):
        self.select()
        self.assertEqual(gate.inspect_selection(self.candidates, self.selection)[0],
                         "STRUCTURE_PASS_HUMAN_MESSAGE_MUST_BE_VERIFIED")

    def test_reject_stale_candidate_snapshot(self):
        self.select()
        self.cards["candidates"][0]["title"] = "Modified"
        self.save()
        with self.assertRaisesRegex(ValueError, "Stale"):
            gate.inspect_selection(self.candidates, self.selection)

    def test_reject_wrong_id(self):
        self.select("P4")
        with self.assertRaisesRegex(ValueError, "P1/P2/P3"):
            gate.inspect_selection(self.candidates, self.selection)

    def test_missing_message_reference(self):
        self.select()
        record = json.loads(self.selection.read_text(encoding="utf-8"))
        record.pop("user_message_reference")
        self.selection.write_text(json.dumps(record), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Missing user message"):
            gate.inspect_selection(self.candidates, self.selection)


if __name__ == "__main__":
    unittest.main()

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

    def test_partial_shortlist_requires_explanation(self):
        self.cards["candidates"].pop()
        self.save()
        with self.assertRaisesRegex(ValueError, "shortfall_reason"):
            gate.inspect_candidates(self.candidates)
        self.cards["shortfall_reason"] = "Only two credible options survived evidence screening."
        self.save()
        self.assertIsInstance(gate.inspect_candidates(self.candidates), str)

    def test_partial_shortlist_explicit_selection_is_valid_structure(self):
        self.cards["candidates"] = self.cards["candidates"][:1]
        self.cards["shortfall_reason"] = "Only one defensible research seed survives the evidence audit."
        self.save()
        self.select("P1")
        self.assertEqual(gate.inspect_selection(self.candidates, self.selection)[0],
                         "STRUCTURE_PASS_HUMAN_MESSAGE_MUST_BE_VERIFIED")

    def test_cannot_select_option_not_offered(self):
        self.cards["candidates"] = self.cards["candidates"][:2]
        self.cards["shortfall_reason"] = "Only two defensible options remain after screening."
        self.save()
        self.select("P3")
        with self.assertRaisesRegex(ValueError, "not offered"):
            gate.inspect_selection(self.candidates, self.selection)

    def test_empty_shortlist_is_invalid(self):
        self.cards["candidates"] = []
        self.save()
        with self.assertRaisesRegex(ValueError, "one to three"):
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

    def test_chinese_ordinal_selection(self):
        self.select()
        record = json.loads(self.selection.read_text(encoding="utf-8"))
        record["user_message"] = "我选第二个项目"
        self.selection.write_text(json.dumps(record), encoding="utf-8")
        self.assertEqual(gate.inspect_selection(self.candidates, self.selection)[0],
                         "STRUCTURE_PASS_HUMAN_MESSAGE_MUST_BE_VERIFIED")

    def test_ambiguous_nonselection_is_rejected(self):
        self.select()
        record = json.loads(self.selection.read_text(encoding="utf-8"))
        record["user_message"] = "继续执行吧"
        self.selection.write_text(json.dumps(record), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "not clearly expressed"):
            gate.inspect_selection(self.candidates, self.selection)

    def test_negated_choice_cannot_be_used_as_approval(self):
        self.select("P2")
        record=json.loads(self.selection.read_text(encoding="utf-8"))
        record["user_message"]="我不选择P2，我选P1"
        self.selection.write_text(json.dumps(record),encoding="utf-8")
        with self.assertRaisesRegex(ValueError,"ambiguous|contradicts"):
            gate.inspect_selection(self.candidates,self.selection)
        record["selected_id"]="P1"
        self.selection.write_text(json.dumps(record),encoding="utf-8")
        self.assertEqual(gate.inspect_selection(self.candidates,self.selection)[0],
                         "STRUCTURE_PASS_HUMAN_MESSAGE_MUST_BE_VERIFIED")

    def test_multiple_choices_rejected(self):
        self.select("P1")
        record=json.loads(self.selection.read_text(encoding="utf-8"))
        for msg in ("我选择P1或P2","我选择P1和P2","我选择P1，也选择P2"):
            record["user_message"]=msg
            self.selection.write_text(json.dumps(record),encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"Multiple|ambiguous"):
                gate.inspect_selection(self.candidates,self.selection)

    def test_bare_project_id_is_valid_structure_only(self):
        self.select()
        record = json.loads(self.selection.read_text(encoding="utf-8"))
        record["user_message"] = "P2"
        self.selection.write_text(json.dumps(record), encoding="utf-8")
        self.assertEqual(gate.inspect_selection(self.candidates, self.selection)[0],
                         "STRUCTURE_PASS_HUMAN_MESSAGE_MUST_BE_VERIFIED")

    def test_compact_chinese_selection(self):
        self.select()
        record = json.loads(self.selection.read_text(encoding="utf-8"))
        record["user_message"] = "我选P2"
        self.selection.write_text(json.dumps(record), encoding="utf-8")
        self.assertEqual(gate.inspect_selection(self.candidates, self.selection)[0],
                         "STRUCTURE_PASS_HUMAN_MESSAGE_MUST_BE_VERIFIED")

    def test_invalid_json_root_blocks(self):
        self.candidates.write_text("[]", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "JSON object"):
            gate.inspect_candidates(self.candidates)

    def test_missing_message_reference(self):
        self.select()
        record = json.loads(self.selection.read_text(encoding="utf-8"))
        record.pop("user_message_reference")
        self.selection.write_text(json.dumps(record), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Missing user message"):
            gate.inspect_selection(self.candidates, self.selection)


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Project-adapted PyTorch correctness checks. No adapter = ERROR, never fake PASS.

Copy to the *algorithm project's* tests/ directory. Provide a real dataset
adapter module via ALGORITHM_CONTRACT_ADAPTER. No GPU, downloads or training.
Optional tests report SKIP (not VERIFIED); cite only executed checks.
"""
import importlib
import io
import os
import sys
import unittest


def load_adapter():
    name = os.environ.get("ALGORITHM_CONTRACT_ADAPTER")
    if not name:
        raise RuntimeError("ALGORITHM_CONTRACT_ADAPTER unset; adapt this file to a real project")
    module = importlib.import_module(name)
    required = ("make_case", "predict", "loss", "assert_contract")
    missing = [x for x in required if not callable(getattr(module, x, None))]
    if missing:
        raise RuntimeError("Adapter missing: " + ", ".join(missing))
    return module


class AlgorithmContractTests(unittest.TestCase):
    """Only CPU, no test-set optimization. One fresh model per test."""

    @classmethod
    def setUpClass(cls):
        cls.adapter = load_adapter()
        try:
            import torch
        except ImportError as exc:
            raise RuntimeError("PyTorch is required in the existing project environment") from exc
        cls.torch = torch

    def case(self):
        model, batch = self.adapter.make_case()
        model = model.cpu()
        if any(p.is_cuda for p in model.parameters()):
            self.fail("Contract tests must remain CPU-only")
        return model, batch

    def test_l1_real_batch_contract(self):
        model, batch = self.case()
        model.eval()
        with self.torch.no_grad():
            y = self.adapter.predict(model, batch)
        self.assertTrue(self.torch.is_tensor(y))
        self.assertTrue(self.torch.isfinite(y).all().item())
        self.adapter.assert_contract(y, batch)  # must assert shape/time/mask/units

    def test_l2_manual_loss_examples(self):
        fn = getattr(self.adapter, "loss_examples", None)
        if fn is None:
            self.skipTest("No independent hand-calculated loss examples supplied")
        examples = list(fn())
        self.assertGreater(len(examples), 0, "empty examples are not evidence")
        for label, actual, expected in examples:
            with self.subTest(label=label):
                self.torch.testing.assert_close(actual, expected)

    def test_l2_reference_parity(self):
        fn = getattr(self.adapter, "reference_prediction", None)
        if fn is None:
            self.skipTest("No independent reference implementation supplied")
        model, batch = self.case()
        model.eval()
        with self.torch.no_grad():
            actual = self.adapter.predict(model, batch)
            reference = fn(model, batch)
        self.torch.testing.assert_close(actual, reference, rtol=1e-5, atol=1e-6)

    def test_l2_gradcheck_custom_differentiable_op(self):
        fn = getattr(self.adapter, "gradcheck_case", None)
        if fn is None:
            self.skipTest("No smooth, float64 differentiable operator selected")
        op, inputs = fn()
        self.assertIsInstance(inputs, tuple)
        for x in inputs:
            self.assertEqual(x.dtype, self.torch.float64)
            self.assertTrue(x.requires_grad)
            self.assertFalse(x.is_cuda)
        self.assertTrue(self.torch.autograd.gradcheck(
            op, inputs, eps=1e-6, atol=1e-4, rtol=1e-3))
        # Do not use gradcheck at nonsmooth boundaries or with mixed precision.

    def test_l3_backward_and_optimizer_update(self):
        model, batch = self.case()
        model.train()
        opt_fn = getattr(self.adapter, "make_optimizer", None)
        optimizer = opt_fn(model) if opt_fn else self.torch.optim.SGD(
            (p for p in model.parameters() if p.requires_grad), lr=0.01)
        optimizer.zero_grad(set_to_none=True)
        output = self.adapter.predict(model, batch)
        loss = self.adapter.loss(output, batch)
        self.assertEqual(loss.ndim, 0)
        self.assertTrue(self.torch.isfinite(loss).item())
        loss.backward()
        named = {n: p for n, p in model.named_parameters() if p.requires_grad}
        self.assertTrue(named, "no trainable parameters")
        key_names = list(getattr(self.adapter, "key_parameter_names", named))
        self.assertTrue(key_names, "declare new-module parameters for a mechanism check")
        opt_ids = {id(p) for group in optimizer.param_groups for p in group["params"]}
        for name in key_names:
            self.assertIn(name, named)
            self.assertIn(id(named[name]), opt_ids, "optimizer omits " + name)
            grad = named[name].grad
            self.assertIsNotNone(grad, name)
            self.assertTrue(self.torch.isfinite(grad).all().item(), name)
            self.assertTrue(self.torch.count_nonzero(grad).item() > 0, name)
        original = {n: named[n].detach().clone() for n in key_names}
        optimizer.step()
        self.assertTrue(any(
            not self.torch.equal(original[n], named[n].detach()) for n in key_names
        ), "optimizer did not update a key new-module parameter")

    def test_l4_eval_checkpoint_roundtrip(self):
        model, batch = self.case()
        model.eval()
        with self.torch.no_grad():
            expected = self.adapter.predict(model, batch)
        buf = io.BytesIO()
        self.torch.save(model.state_dict(), buf)
        buf.seek(0)
        new_model, _ = self.case()
        new_model.load_state_dict(self.torch.load(
            buf, map_location="cpu", weights_only=True), strict=True)
        new_model.eval()
        with self.torch.no_grad():
            actual = self.adapter.predict(new_model, batch)
        self.torch.testing.assert_close(actual, expected, rtol=1e-5, atol=1e-6)

    def test_l4_deployment_inputs_only(self):
        fn = getattr(self.adapter, "deployment_batch", None)
        if fn is None:
            self.skipTest("No target-free deployment batch provided")
        model, _ = self.case()
        model.eval()
        with self.torch.no_grad():
            pred = self.adapter.predict(model, fn())
        self.assertTrue(self.torch.is_tensor(pred))
        self.assertTrue(self.torch.isfinite(pred).all().item())

    def test_sensor_temporal_and_mask_invariance(self):
        fn = getattr(self.adapter, "invariance_cases", None)
        if fn is None:
            self.skipTest("No physically justified invariance pairs provided")
        pairs = list(fn())
        self.assertTrue(pairs, "empty invariance set is not evidence")
        model, _ = self.case()
        model.eval()
        with self.torch.no_grad():
            for name, a, b in pairs:
                with self.subTest(case=name):
                    ya = self.adapter.predict(model, a)
                    yb = self.adapter.predict(model, b)
                    self.torch.testing.assert_close(ya, yb, rtol=1e-5, atol=1e-6)


if __name__ == "__main__":
    try:
        load_adapter()
    except (RuntimeError, ImportError) as exc:
        print("CONTRACT_NOT_CONFIGURED:", exc, file=sys.stderr)
        sys.exit(2)
    unittest.main()

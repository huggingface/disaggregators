import unittest
from typing import Callable
from unittest.mock import MagicMock, patch

from disaggregators import DisaggregationModule, Disaggregator
from tests.test_disaggregation_module import DummyModule


MockDisaggregationModuleFactory = MagicMock()
MockDisaggregationModuleFactory.create_from_id.side_effect = lambda module_id=None, column=None: DummyModule(
    module_id=module_id, column=column
)


@patch("disaggregators.disaggregator.DisaggregationModuleFactory", MockDisaggregationModuleFactory)
class TestDisaggregator(unittest.TestCase):
    def test_create_empty_disaggregator(self):
        disagg = Disaggregator()
        self.assertIsInstance(disagg.modules, list)
        self.assertEqual(0, len(disagg.modules))

    def test_create_disaggregator_with_single_module(self):
        disagg = Disaggregator("pronouns")
        self.assertEqual(1, len(disagg.modules))
        self.assertIsInstance(disagg.modules[0], DisaggregationModule)
        self.assertEqual(
            "pronouns",
            disagg.modules[0].name,
        )

    def test_create_disaggregator_with_multiple_modules(self):
        disagg = Disaggregator(["pronouns", "spelling"])
        self.assertEqual(2, len(disagg.modules))
        self.assertTrue(all([isinstance(module, DisaggregationModule) for module in disagg.modules]))
        self.assertEqual(disagg.modules[0].name, "pronouns")
        self.assertEqual(disagg.modules[1].name, "spelling")

    def test_get_disaggregator_function_single_aggregation_module(self):
        disagg = Disaggregator("dummy-module")
        disagg_func = disagg.get_function()
        self.assertIsInstance(disagg_func, Callable)
        self.assertEqual({"dummy-module.dummy-value": True}, disagg_func({"a": 1, "b": 2}))

    def test_get_disaggregator_function_multiple_aggregation_modules(self):
        disagg = Disaggregator(["dummy-one", "dummy-two"])
        disagg_func = disagg.get_function()
        self.assertIsInstance(disagg_func, Callable)
        self.assertEqual(
            {"dummy-one.dummy-value": True, "dummy-two.dummy-value": True},
            disagg_func({"a": 1, "b": 2}),
        )

    def test_get_disaggregator_function_multiple_aggregation_modules_multiple_labels(self):
        disagg = Disaggregator(["dummy-one", "dummy-two"])
        disagg_func = disagg.get_function()
        self.assertIsInstance(disagg_func, Callable)
        self.assertEqual(
            {"dummy-one.dummy-value": True, "dummy-two.dummy-value": True},
            disagg_func({"a": 1, "b": 2}),
        )

    def test_get_disaggregation_sets(self):
        disagg = Disaggregator(["dummy-one", "dummy-two"])
        disagg_sets = disagg.get_disaggregation_sets()
        self.assertEqual({"dummy-one": {"dummy-one.dummy-value"}, "dummy-two": {"dummy-two.dummy-value"}}, disagg_sets)


if __name__ == "__main__":
    unittest.main()

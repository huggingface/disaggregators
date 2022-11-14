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
        self.assertEqual(len(disagg.modules), 0)

    def test_create_disaggregator_with_single_module(self):
        disagg = Disaggregator("pronouns")
        self.assertEqual(len(disagg.modules), 1)
        self.assertIsInstance(disagg.modules[0], DisaggregationModule)
        self.assertEqual(disagg.modules[0].name, "pronouns")

    def test_create_disaggregator_with_multiple_modules(self):
        disagg = Disaggregator(["pronouns", "spelling"])
        self.assertEqual(len(disagg.modules), 2)
        self.assertTrue(all([isinstance(module, DisaggregationModule) for module in disagg.modules]))
        self.assertEqual(disagg.modules[0].name, "pronouns")
        self.assertEqual(disagg.modules[1].name, "spelling")

    def test_get_disaggregator_function_single_aggregation_module(self):
        disagg = Disaggregator("dummy-module")
        disagg_func = disagg.get_function()
        self.assertIsInstance(disagg_func, Callable)
        self.assertEqual(disagg_func({"a": 1, "b": 2}), {"dummy-module": True})

    def test_get_disaggregator_function_multiple_aggregation_modules(self):
        disagg = Disaggregator(["dummy-one", "dummy-two"])
        disagg_func = disagg.get_function()
        self.assertIsInstance(disagg_func, Callable)
        self.assertEqual(disagg_func({"a": 1, "b": 2}), {"dummy-one": True, "dummy-two": True})


if __name__ == "__main__":
    unittest.main()

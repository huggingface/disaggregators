import unittest
from unittest.mock import patch

from disaggregators import DisaggregationModule, DisaggregationModuleFactory, DisaggregationModuleLabels


class DummyLabels(DisaggregationModuleLabels):
    DUMMY = "dummy-value"


class DummyModule(DisaggregationModule):
    def __init__(self, module_id="dummy-module", column=None):
        super().__init__(module_id=module_id, column=column, labels=DummyLabels)

    def __call__(self, row, *args, **kwargs):
        return {DummyLabels.DUMMY: True}


class TestModule(unittest.TestCase):
    def test_create_subclassed_module(self):
        custom_module = DummyModule()
        self.assertEqual("dummy-module", custom_module.name)

    @unittest.skip("Not yet implemented.")
    def test_get_labels(self):
        pass

    @unittest.skip("Not yet implemented.")
    def test_get_label_name(self):
        pass

    @unittest.skip("Not yet implemented.")
    def test_get_label_names(self):
        pass


@patch("disaggregators.disaggregation_modules.disaggregation_module.disaggregation_modules")
class TestModuleCreator(unittest.TestCase):
    def test_load_module_from_string_id(self, mock_disaggregation_modules):
        mock_disaggregation_modules.AVAILABLE_MODULES = {"dummy-module": DummyModule}
        loaded_module = DisaggregationModuleFactory.create_from_id(module_id="dummy-module", column="")
        self.assertTrue(issubclass(type(loaded_module), DisaggregationModule))
        self.assertEqual("dummy-module", loaded_module.name)

    def test_load_module_with_bad_string_id(self, mock_disaggregation_modules):
        mock_disaggregation_modules.AVAILABLE_MODULES = {}

        with self.assertRaises(ValueError):
            DisaggregationModuleFactory.create_from_id(module_id="bad-module", column="")


if __name__ == "__main__":
    unittest.main()

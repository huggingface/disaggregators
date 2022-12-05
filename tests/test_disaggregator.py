from typing import Callable

import pytest

from disaggregators import DisaggregationModule, Disaggregator
from tests.test_disaggregation_module import DummyModule


class TestDisaggregator:
    @pytest.fixture(autouse=True)
    def mock_module_factory(self, mocker):
        mock_factory = mocker.MagicMock()
        mock_factory.create_from_id.side_effect = lambda module_id=None, column=None: DummyModule(
            module_id=module_id, column=column
        )

        mocker.patch("disaggregators.disaggregator.DisaggregationModuleFactory", mock_factory)

    def test_create_empty_disaggregator(self):
        disagg = Disaggregator()
        assert isinstance(disagg.modules, list)
        assert len(disagg.modules) == 0

    def test_create_disaggregator_with_single_module(self):
        disagg = Disaggregator("pronoun")
        assert len(disagg.modules) == 1
        assert isinstance(disagg.modules[0], DisaggregationModule)
        assert disagg.modules[0].name == "pronoun"

    def test_create_disaggregator_with_multiple_modules(self):
        disagg = Disaggregator(["pronoun", "spelling"])
        assert len(disagg.modules) == 2
        assert all([isinstance(module, DisaggregationModule) for module in disagg.modules])
        assert disagg.modules[0].name == "pronoun"
        assert disagg.modules[1].name == "spelling"

    def test_get_disaggregator_function_single_aggregation_module(self):
        disagg = Disaggregator("dummy-module")
        assert disagg({"a": 1, "b": 2}) == {"dummy-module.dummy-value-1": True, "dummy-module.dummy-value-2": True}
        disagg_func = disagg.get_function()
        assert isinstance(disagg_func, Callable)
        assert disagg_func({"a": 1, "b": 2}) == {
            "dummy-module.dummy-value-1": True,
            "dummy-module.dummy-value-2": True,
        }

    def test_get_disaggregator_function_multiple_aggregation_modules(self):
        disagg = Disaggregator(["dummy-one", "dummy-two"])
        assert disagg({"a": 1, "b": 2}) == {
            "dummy-one.dummy-value-1": True,
            "dummy-one.dummy-value-2": True,
            "dummy-two.dummy-value-1": True,
            "dummy-two.dummy-value-2": True,
        }
        disagg_func = disagg.get_function()
        assert isinstance(disagg_func, Callable)
        assert disagg_func({"a": 1, "b": 2}) == {
            "dummy-one.dummy-value-1": True,
            "dummy-one.dummy-value-2": True,
            "dummy-two.dummy-value-1": True,
            "dummy-two.dummy-value-2": True,
        }

    @pytest.mark.parametrize(
        "modules,expected",
        [
            ([], set()),
            (["dummy-one"], {"dummy-one.dummy-value-1", "dummy-one.dummy-value-2"}),
            (
                ["dummy-one", "dummy-two"],
                {
                    "dummy-one.dummy-value-1",
                    "dummy-one.dummy-value-2",
                    "dummy-two.dummy-value-1",
                    "dummy-two.dummy-value-2",
                },
            ),
        ],
    )
    def test_get_fields(self, modules, expected):
        disagg = Disaggregator(modules)
        assert disagg.fields == expected

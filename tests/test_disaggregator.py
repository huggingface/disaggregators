from typing import Callable

import pytest
from datasets import Dataset

from disaggregators import CustomDisaggregator, DisaggregationModule, Disaggregator


class TestDisaggregator:
    @pytest.fixture(autouse=True)
    def mock_module_factory(self, mocker, dummy_module):
        mock_factory = mocker.MagicMock()
        mock_factory.create_module.side_effect = lambda module_id=None, column=None: dummy_module(
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


@pytest.fixture
def custom_module(dummy_labels):
    class CustomModule(CustomDisaggregator):
        module_id = "custom"
        labels = dummy_labels

        def __call__(self, row, *args, **kwargs):
            return {dummy_labels.DUMMY_ONE: "cat", dummy_labels.DUMMY_TWO: "dog"}

    return CustomModule


def test_inject_custom_module_subclass(custom_module, dummy_labels):
    disagg = Disaggregator(custom_module, column=None)
    assert disagg.fields == {"custom.dummy-value-1", "custom.dummy-value-2"}

    ds = Dataset.from_dict({"text": ["Hello world!"]}).map(disagg)
    assert set(ds.features) == {"text", *disagg.fields}
    assert ds[0] == {"text": "Hello world!", "custom.dummy-value-1": "cat", "custom.dummy-value-2": "dog"}


def test_module_instance(configured_module, configured_dummy_expected_results):
    disagg = Disaggregator(configured_module, column=None)
    assert disagg.fields == configured_module.field_names

    ds = Dataset.from_dict({"text": ["Hello world!"]}).map(disagg)
    assert set(ds.features) == {"text", *disagg.fields}
    assert ds[0] == {"text": "Hello world!", **configured_dummy_expected_results}

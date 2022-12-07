import pytest
import os

from typing import Type

from disaggregators import DisaggregationModule, DisaggregationModuleLabels, DisaggregationModuleConfig


def pytest_collection_modifyitems(items):
    for item in items:
        if "integration" in item.nodeid:
            item.add_marker(pytest.mark.slow)
            item.add_marker(pytest.mark.integration)


def pytest_generate_tests(metafunc):
    if metafunc.definition.name == "test_each_module":
        metafunc.parametrize("module", [
                x.name for x in os.scandir(
                    metafunc.definition.config.rootdir / "src/disaggregators/disaggregation_modules"
                ) if x.is_dir() and not x.name.startswith("__")
        ])

# Fixtures


class DummyLabels(DisaggregationModuleLabels):
    DUMMY_ONE = "dummy-value-1"
    DUMMY_TWO = "dummy-value-2"


@pytest.fixture
def dummy_labels():
    return DummyLabels


@pytest.fixture
def dummy_module_config(dummy_labels):
    class DummyModuleConfig(DisaggregationModuleConfig):
        def __init__(self, labels: Type[dummy_labels]):
            self.labels = labels

    return DummyModuleConfig


@pytest.fixture
def dummy_module(dummy_labels, dummy_module_config):
    class DummyModule(DisaggregationModule):
        labels = dummy_labels

        def __init__(self, module_id="dummy-module", *args, **kwargs):
            super().__init__(module_id=module_id, *args, **kwargs)

        def _apply_config(self, config):
            self.labels = config.labels

        def __call__(self, row, *args, **kwargs):
            return {label: True for label in list(self.labels)}

    return DummyModule


@pytest.fixture
def custom_dummy_labels():
    class CustomDummyLabels(DisaggregationModuleLabels):
        DUMMY_ONE = "dummy-value-1"
        DUMMY_TWO = "dummy-value-2"
        DUMMY_THREE = "dummy-value-3"

    return CustomDummyLabels


@pytest.fixture
def configured_module(custom_dummy_labels, dummy_module_config, dummy_module):
    return dummy_module(config=dummy_module_config(labels=custom_dummy_labels), column=None)


@pytest.fixture
def configured_dummy_expected_results(custom_dummy_labels, configured_module):
    return {f"{configured_module.name}.{label}": True for label in custom_dummy_labels}

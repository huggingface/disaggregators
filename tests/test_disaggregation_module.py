import pytest

from disaggregators import DisaggregationModule, DisaggregationModuleFactory, DisaggregationModuleLabels


class DummyLabels(DisaggregationModuleLabels):
    DUMMY_ONE = "dummy-value-1"
    DUMMY_TWO = "dummy-value-2"


class DummyModule(DisaggregationModule):
    labels = DummyLabels

    def __init__(self, module_id="dummy-module", *args, **kwargs):
        super().__init__(module_id=module_id, *args, **kwargs)

    def _apply_config(self, config):
        self.labels = config["labels"]

    def __call__(self, row, *args, **kwargs):
        return {label: True for label in self.labels}


def test_create_subclassed_module():
    custom_module = DummyModule(column=None)
    assert custom_module.name == "dummy-module"


def test_load_module_from_string_id(mocker):
    mock_modules = mocker.MagicMock()
    mock_modules.AVAILABLE_MODULES = {"dummy-module": DummyModule}
    mocker.patch("disaggregators.disaggregation_modules.disaggregation_module.disaggregation_modules", mock_modules)

    loaded_module = DisaggregationModuleFactory.create_from_id(module_id="dummy-module", column=None)
    assert issubclass(type(loaded_module), DisaggregationModule)
    assert loaded_module.name == "dummy-module"


def test_load_module_with_bad_string_id(mocker):
    mock_modules = mocker.MagicMock()
    mock_modules.AVAILABLE_MODULES = {}
    mocker.patch("disaggregators.disaggregation_modules.disaggregation_module.disaggregation_modules", mock_modules)

    with pytest.raises(ValueError, match="Invalid module_id received."):
        DisaggregationModuleFactory.create_from_id(module_id="bad-module")


def test_override_module_config():
    class CustomDummyLabels(DisaggregationModuleLabels):
        DUMMY_ONE = "dummy-value-1"
        DUMMY_TWO = "dummy-value-2"
        DUMMY_THREE = "dummy-value-3"

    custom_module = DummyModule(config={"labels": CustomDummyLabels}, column=None)

    assert custom_module.labels == CustomDummyLabels

    # Ensure that the original module hasn't been modified
    original_module = DummyModule(column=None)
    assert original_module.labels == DummyLabels

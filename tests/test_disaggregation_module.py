import pytest

from disaggregators import DisaggregationModule, DisaggregationModuleFactory


def test_create_subclassed_module(dummy_module):
    custom_module = dummy_module(column=None)
    assert custom_module.name == "dummy-module"


def test_load_module_from_string_id(mocker, dummy_module):
    mock_modules = mocker.MagicMock()
    mock_modules.AVAILABLE_MODULES = {"dummy-module": dummy_module}
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


def test_override_module_config(configured_module, custom_dummy_labels, dummy_module, dummy_labels):
    assert configured_module.labels == custom_dummy_labels

    # Ensure that the original module hasn't been modified
    original_module = dummy_module(column=None)
    assert original_module.labels == dummy_labels

import pytest

from disaggregators import DisaggregationModule, DisaggregationModuleFactory, DisaggregationModuleLabels


class DummyLabels(DisaggregationModuleLabels):
    DUMMY_ONE = "dummy-value-1"
    DUMMY_TWO = "dummy-value-2"


class DummyModule(DisaggregationModule):
    def __init__(self, module_id="dummy-module", column=None):
        super().__init__(module_id=module_id, column=column, labels=DummyLabels)

    def __call__(self, row, *args, **kwargs):
        return {
            DummyLabels.DUMMY_ONE: True,
            DummyLabels.DUMMY_TWO: True
        }


def test_create_subclassed_module():
    custom_module = DummyModule()
    assert custom_module.name == "dummy-module"


def test_load_module_from_string_id(mocker):
    mock_modules = mocker.MagicMock()
    mock_modules.AVAILABLE_MODULES = {"dummy-module": DummyModule}
    mocker.patch("disaggregators.disaggregation_modules.disaggregation_module.disaggregation_modules", mock_modules)

    loaded_module = DisaggregationModuleFactory.create_from_id(module_id="dummy-module", column="")
    assert issubclass(type(loaded_module), DisaggregationModule)
    assert loaded_module.name == "dummy-module"


def test_load_module_with_bad_string_id(mocker):
    mock_modules = mocker.MagicMock()
    mock_modules.AVAILABLE_MODULES = {}
    mocker.patch("disaggregators.disaggregation_modules.disaggregation_module.disaggregation_modules", mock_modules)

    with pytest.raises(ValueError, match="Invalid module_id received."):
        DisaggregationModuleFactory.create_from_id(module_id="bad-module", column="")

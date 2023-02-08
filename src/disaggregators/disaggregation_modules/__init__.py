# from .age import Age
# from .continent import Continent
from .disaggregation_module import (
    CustomDisaggregator,
    DisaggregationModule,
    DisaggregationModuleConfig,
    DisaggregationModuleFactory,
    DisaggregationModuleLabels,
)
from .gender import Gender


# from .pronoun import Pronoun
# from .religion import Religion


AVAILABLE_MODULES = {
    "pronoun": None,
    "age": None,
    "gender": Gender,
    "religion": None,
    "continent": None,
}

__all__ = [
    "DisaggregationModule",
    "DisaggregationModuleFactory",
    "DisaggregationModuleLabels",
    "CustomDisaggregator",
    "DisaggregationModuleConfig",
]

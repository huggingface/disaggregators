from .age import Age
from .continent import Continent
from .disaggregation_module import (
    CustomDisaggregator,
    DisaggregationModule,
    DisaggregationModuleConfig,
    DisaggregationModuleFactory,
    DisaggregationModuleLabels,
)
from .gender import Gender
from .pronoun import Pronoun
from .religion import Religion


AVAILABLE_MODULES = {"pronoun": Pronoun, "age": Age, "gender": Gender, "religion": Religion, "continent": Continent}

__all__ = [
    "DisaggregationModule",
    "DisaggregationModuleFactory",
    "DisaggregationModuleLabels",
    "CustomDisaggregator",
    "DisaggregationModuleConfig",
]

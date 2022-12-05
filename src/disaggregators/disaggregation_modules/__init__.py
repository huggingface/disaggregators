from .age import Age
from .disaggregation_module import DisaggregationModule, DisaggregationModuleFactory, DisaggregationModuleLabels
from .gender import Gender
from .pronoun import Pronoun


AVAILABLE_MODULES = {"pronoun": Pronoun, "age": Age, "gender": Gender}

__all__ = ["DisaggregationModule", "DisaggregationModuleFactory", "DisaggregationModuleLabels"]

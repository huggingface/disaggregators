from .age import Age
from .disaggregation_module import DisaggregationModule, DisaggregationModuleFactory, DisaggregationModuleLabels
from .pronoun import Pronoun


AVAILABLE_MODULES = {"pronoun": Pronoun, "age": Age}

__all__ = ["DisaggregationModule", "DisaggregationModuleFactory", "DisaggregationModuleLabels"]

from .disaggregation_module import DisaggregationModule, DisaggregationModuleFactory, DisaggregationModuleLabels
from .pronoun import Pronoun


AVAILABLE_MODULES = {"pronoun": Pronoun}

__all__ = ["DisaggregationModule", "DisaggregationModuleFactory", "DisaggregationModuleLabels"]

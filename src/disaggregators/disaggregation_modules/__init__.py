from .disaggregation_module import DisaggregationModule, DisaggregationModuleFactory, DisaggregationModuleLabels
from .pronouns import Pronouns
from .random import Random


AVAILABLE_MODULES = {"pronouns": Pronouns, "random": Random}

__all__ = ["DisaggregationModule", "DisaggregationModuleFactory", "DisaggregationModuleLabels"]

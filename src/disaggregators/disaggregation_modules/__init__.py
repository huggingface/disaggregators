from .disaggregation_module import DisaggregationModule, DisaggregationModuleFactory, DisaggregationModuleLabels
from .pronouns import Pronouns


AVAILABLE_MODULES = {"pronouns": Pronouns}

__all__ = ["DisaggregationModule", "DisaggregationModuleFactory", "DisaggregationModuleLabels"]

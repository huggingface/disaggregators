from .disaggregation_module import DisaggregationModule, DisaggregationModuleFactory
from .pronouns import Pronouns


AVAILABLE_MODULES = {"pronouns": Pronouns}

__all__ = ["DisaggregationModule", "DisaggregationModuleFactory"]

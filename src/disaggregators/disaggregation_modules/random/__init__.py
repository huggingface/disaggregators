import random

from ..disaggregation_module import DisaggregationModule, DisaggregationModuleLabels


class RandomLabels(DisaggregationModuleLabels):
    POSITIVE = "positive"
    NEGATIVE = "negative"


class Random(DisaggregationModule):
    def __init__(self, *args, **kwargs):
        super().__init__(module_id="random", labels=RandomLabels, *args, **kwargs)

    def __call__(self, row, *args, **kwargs):
        result = {x: False for x in RandomLabels}
        result[random.choice(list(RandomLabels))] = True

        return result

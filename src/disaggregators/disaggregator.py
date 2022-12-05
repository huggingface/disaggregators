from typing import Callable, List, Optional, Set, Union

from disaggregators.disaggregation_modules import DisaggregationModuleFactory


class Disaggregator:
    def __init__(self, module_ids: Optional[Union[str, List[str]]] = None, column: str = None):
        if module_ids is None:
            module_ids = []

        if isinstance(module_ids, str):
            self.modules = [DisaggregationModuleFactory.create_from_id(module_ids, column=column)]
        elif isinstance(module_ids, list):
            self.modules = [
                DisaggregationModuleFactory.create_from_id(module_id, column=column) for module_id in module_ids
            ]
        else:
            raise ValueError("Invalid argument passed for module")

    def get_function(self) -> Callable:
        # Merge dicts - https://stackoverflow.com/a/3495395
        return lambda x: {
            f"{d[0]}.{k.value}": v
            for d in [(module.name, module(x)) for module in self.modules]
            for k, v in d[1].items()
        }

    def __call__(self, x) -> Callable:
        return self.get_function()(x)

    @property
    def fields(self) -> Set:
        return {*[f"{module.name}.{label.value}" for module in self.modules for label in module.labels]}

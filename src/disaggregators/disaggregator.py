from typing import Callable, Optional, Set, Union, List, Dict

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
            k: v
            for d in [{module.get_label_name(_k): _v for _k, _v in module(x).items()} for module in self.modules]
            for k, v in d.items()
        }

    def get_disaggregation_sets(self) -> Dict[str, Set]:
        return {module.name: module.get_label_names() for module in self.modules}

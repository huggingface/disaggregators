from typing import Callable, List, Optional, Set, Type, Union

from disaggregators.disaggregation_modules import CustomDisaggregator, DisaggregationModuleFactory


class Disaggregator:
    def __init__(self, module: Optional[Union[str, Type[CustomDisaggregator], List[str]]] = None, column: str = None):
        if module is None:
            module = []

        if not isinstance(module, list):
            module_list = [module]
        else:
            module_list = module

        self.modules = [DisaggregationModuleFactory.create_module(module, column=column) for module in module_list]

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

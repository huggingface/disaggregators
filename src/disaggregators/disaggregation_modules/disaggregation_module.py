from abc import ABC, abstractmethod

from disaggregators import disaggregation_modules


class DisaggregationModule(ABC):
    def __init__(self, module_id: str, column: str):
        self.name = module_id
        self.column = column

    @abstractmethod
    def __call__(self, row, *args, **kwargs):
        raise NotImplementedError()


class DisaggregationModuleFactory:
    @staticmethod
    def create_from_id(module_id: str, column: str) -> DisaggregationModule:
        if module_id not in disaggregation_modules.AVAILABLE_MODULES:
            raise ValueError("Invalid module_id received.")

        return disaggregation_modules.AVAILABLE_MODULES[module_id](column=column)

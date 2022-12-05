from abc import ABC, abstractmethod
from enum import Enum
from typing import Set, Type

from disaggregators import disaggregation_modules


class DisaggregationModuleLabels(Enum):
    pass


class DisaggregationModule(ABC):
    def __init__(self, module_id: str, column: str, labels: Type[DisaggregationModuleLabels]):
        self.name = module_id
        self.column = column
        self.labels: Set[DisaggregationModuleLabels] = set(labels)

    @abstractmethod
    def __call__(self, row, *args, **kwargs):
        raise NotImplementedError()

    def get_label_names(self) -> Set[str]:
        return {self.get_label_name(x) for x in self.labels}

    def get_label_name(self, label: DisaggregationModuleLabels) -> str:
        return f"{self.name}.{label.value}"


class DisaggregationModuleFactory:
    @staticmethod
    def create_from_id(module_id: str, column: str) -> DisaggregationModule:
        if module_id not in disaggregation_modules.AVAILABLE_MODULES:
            raise ValueError("Invalid module_id received.")

        return disaggregation_modules.AVAILABLE_MODULES[module_id](column=column)

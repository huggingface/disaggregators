from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Type, Union

from disaggregators import disaggregation_modules


class DisaggregationModuleLabels(Enum):
    pass


class DisaggregationModule(ABC):
    def __init__(self, module_id: str, column: str, labels: Type[DisaggregationModuleLabels]):
        self.name = module_id
        self.column = column
        self.labels = labels
        self.citations: List[str] = []

    @abstractmethod
    def __call__(self, row, *args, **kwargs):
        raise NotImplementedError()


class CustomDisaggregator(DisaggregationModule, ABC):
    """
    This class exists to provide a simple interface for creating custom disaggregation modules. This is useful because
    the DisaggregationModule abstract class may enforce extra rules that we don't want users to have to worry about.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(module_id=self.module_id, labels=self.labels, *args, **kwargs)

    @property
    @abstractmethod
    def module_id(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def labels(self):
        raise NotImplementedError()


class DisaggregationModuleFactory:
    @staticmethod
    def create_module(module: Union[str, Type[CustomDisaggregator]], column: str):
        if isinstance(module, str):
            return DisaggregationModuleFactory.create_from_id(module, column)
        elif issubclass(module, CustomDisaggregator):
            return DisaggregationModuleFactory.create_from_class(module, column)
        else:
            raise ValueError("Invalid module type received.")

    @staticmethod
    def create_from_id(module_id: str, column: str) -> DisaggregationModule:
        if module_id not in disaggregation_modules.AVAILABLE_MODULES:
            raise ValueError("Invalid module_id received.")

        return disaggregation_modules.AVAILABLE_MODULES[module_id](column=column)

    @staticmethod
    def create_from_class(module: Type[CustomDisaggregator], column: str) -> DisaggregationModule:
        return module(column=column)

from abc import ABC, abstractmethod
from typing import List, Optional, Type, Union

from aenum import Constant

from disaggregators import disaggregation_modules


class DisaggregationModuleLabels(Constant):
    pass


class DisaggregationModuleConfig:
    labels: Type[DisaggregationModuleLabels]


class DisaggregationModule(ABC):
    def __init__(self, module_id: str, column: Optional[str], config: DisaggregationModuleConfig = None):
        self.name = module_id
        self.column = column
        self.citations: List[str] = []

        if config:
            self._apply_config(config)

    @abstractmethod
    def __call__(self, row, *args, **kwargs):
        raise NotImplementedError()

    @property
    @abstractmethod
    def labels(self) -> Type[DisaggregationModuleLabels]:
        pass

    def _apply_config(self, config: DisaggregationModuleConfig):
        pass

    @property
    def field_names(self):
        return {f"{self.name}.{x}" for x in list(self.labels)}


class CustomDisaggregator(DisaggregationModule, ABC):
    """
    This class exists to provide a simple interface for creating custom disaggregation modules. This is useful because
    the DisaggregationModule abstract class may enforce extra rules that we don't want users to have to worry about.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(module_id=self.module_id, *args, **kwargs)

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
    def create_module(module: Union[str, Type[CustomDisaggregator], DisaggregationModule], *args, **kwargs):
        if isinstance(module, str):
            return DisaggregationModuleFactory.create_from_id(module, *args, **kwargs)
        elif isinstance(module, DisaggregationModule):
            return module
        elif issubclass(module, CustomDisaggregator):
            return DisaggregationModuleFactory.create_from_class(module, *args, **kwargs)
        else:
            raise ValueError("Invalid module type received.")

    @staticmethod
    def create_from_id(module_id: str, *args, **kwargs) -> DisaggregationModule:
        if module_id not in disaggregation_modules.AVAILABLE_MODULES:
            raise ValueError("Invalid module_id received.")

        return disaggregation_modules.AVAILABLE_MODULES[module_id](*args, **kwargs)

    @staticmethod
    def create_from_class(module: Type[CustomDisaggregator], *args, **kwargs) -> DisaggregationModule:
        return module(*args, **kwargs)

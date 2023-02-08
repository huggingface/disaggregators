from abc import ABC, abstractmethod
from typing import List, Optional, Type, Union

from aenum import Constant
from spacy import Language

from disaggregators import disaggregation_modules
from disaggregators.utils.spacy_utils import language_check


class DisaggregationModuleLabels(Constant):
    pass


class DisaggregationModuleConfig:
    labels: Type[DisaggregationModuleLabels]


class DisaggregationModule(ABC):
    required_spacy_components: List[str] = ["tokenizer", "tok2vec"]

    def __init__(
        self,
        language: Language,
        module_id: str,
        config: DisaggregationModuleConfig = None,
    ):
        self.nlp = language_check(language)

        self.name = module_id

        self.citations: List[str] = []

        if config:
            self._apply_config(config)

    @abstractmethod
    def __call__(self, row: str, *args, **kwargs):
        raise NotImplementedError()

    def process_doc(self, doc: str, *args, **kwargs):
        raise NotImplementedError()

    def pipe(self, rows, *args, **kwargs):
        raise NotImplementedError()

    def pipe_docs(self, docs, *args, **kwargs):
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
    def create_module(
        module: Union[str, Type[CustomDisaggregator], DisaggregationModule],
        language: Optional[Union["spacy.Language", str]] = None,
        *args,
        **kwargs,
    ):
        nlp = language_check(language)
        if isinstance(module, str):
            return DisaggregationModuleFactory.create_from_id(
                module, language=nlp, *args, **kwargs
            )
        elif isinstance(module, DisaggregationModule):
            return module
        elif issubclass(module, CustomDisaggregator):
            return DisaggregationModuleFactory.create_from_class(
                module, language=nlp, *args, **kwargs
            )
        else:
            raise ValueError("Invalid module type received.")

    @staticmethod
    def create_from_id(module_id: str, *args, **kwargs) -> DisaggregationModule:
        if module_id not in disaggregation_modules.AVAILABLE_MODULES:
            raise ValueError("Invalid module_id received.")

        return disaggregation_modules.AVAILABLE_MODULES[module_id](*args, **kwargs)

    @staticmethod
    def create_from_class(
        module: Type[CustomDisaggregator], *args, **kwargs
    ) -> DisaggregationModule:
        return module(*args, **kwargs)

from typing import Callable, List, Optional, Set, Type, Union

from disaggregators.disaggregation_modules import (
    CustomDisaggregator,
    DisaggregationModule,
    DisaggregationModuleFactory,
)
from disaggregators.utils.spacy_utils import language_check


class Disaggregator:
    def __init__(
        self,
        module: Optional[
            Union[
                str,
                List[str],
                DisaggregationModule,
                List[DisaggregationModule],
                Type[CustomDisaggregator],
                List[Type[CustomDisaggregator]],
            ]
        ] = None,
        language: Optional[Union["spacy.Language", str]] = None,
        *args,
        **kwargs,
    ):
        if module is None:
            module = []

        if not isinstance(module, list):
            module_list = [module]
        else:
            module_list = module

        self.nlp = language_check(language)

        self.modules = [
            DisaggregationModuleFactory.create_module(
                module, language=self.nlp, *args, **kwargs
            )
            for module in module_list
        ]

        required_components = []
        for module in self.modules:
            required_components += module.required_spacy_components

        self.disabled_components = [
            component
            for component in self.nlp.component_names
            if component not in required_components
        ]

    def get_function(self) -> Callable:
        # Merge dicts - https://stackoverflow.com/a/3495395
        return lambda x: {
            f"{d[0]}.{str(k)}": v
            for d in [(module.name, module(x)) for module in self.modules]
            for k, v in d[1].items()
        }

    def __call__(self, x) -> Callable:
        doc = self.nlp(x, disable=self.disabled_components)
        [module.process_doc(doc) for module in self.modules]
        return doc

    def pipe(self, x) -> Callable:
        docs = self.nlp.pipe(x, disable=self.disabled_components)
        [module.pipe_docs(docs) for module in self.modules]
        return docs

    @property
    def fields(self) -> Set:
        return {
            *[
                f"{module.name}.{str(label)}"
                for module in self.modules
                for label in module.labels
            ]
        }

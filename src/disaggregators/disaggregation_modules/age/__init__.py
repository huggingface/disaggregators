import re
from bisect import bisect
from typing import List, Type

import spacy

from ..disaggregation_module import DisaggregationModule, DisaggregationModuleConfig, DisaggregationModuleLabels


class AgeLabels(DisaggregationModuleLabels):
    CHILD = "child"
    YOUTH = "youth"
    ADULT = "adult"
    SENIOR = "senior"


class AgeConfig(DisaggregationModuleConfig):
    def __init__(self, labels: Type[AgeLabels], ages: List, breakpoints: List):
        self.labels = labels
        self.ages = ages
        self.breakpoints = breakpoints


class Age(DisaggregationModule):
    labels = AgeLabels
    AGES = [AgeLabels.CHILD, AgeLabels.YOUTH, AgeLabels.ADULT, AgeLabels.SENIOR]
    AGE_BREAKPOINTS = [0, 12, 20, 65]
    spacy_model = "en_core_web_lg"

    def __init__(self, *args, **kwargs):
        try:
            self.nlp = spacy.load(self.spacy_model, enable="ner")
        except OSError:
            raise ValueError(
                f"This disaggregation module depends on the {self.spacy_model} model from spaCy.\n"
                f"You can install it by running: python -m spacy download {self.spacy_model}"
            )

        super().__init__(module_id="age", *args, **kwargs)

    def _apply_config(self, config: AgeConfig):
        self.labels = config.labels
        self.AGES = config.ages
        self.AGE_BREAKPOINTS = config.breakpoints

    def __call__(self, row, *args, **kwargs):
        return_ages = {age: False for age in self.AGES}
        text = row[self.column]
        doc = self.nlp(text)
        date_entities = [y for y in doc.ents if y.label_ == "DATE"]

        for date_entity in date_entities:
            value = re.search(r"\d+", date_entity.text)

            if value is None:
                continue

            value = int(value[0])

            if value <= 120:
                age_bucket = bisect(self.AGE_BREAKPOINTS, value)
                if age_bucket >= 1:
                    return_ages.update({self.AGES[age_bucket - 1]: True})

        return return_ages

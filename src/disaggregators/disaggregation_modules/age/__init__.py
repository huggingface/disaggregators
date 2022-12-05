import re
from bisect import bisect

import spacy

from ..disaggregation_module import DisaggregationModule, DisaggregationModuleLabels


class AgeLabels(DisaggregationModuleLabels):
    CHILD = "child"
    YOUTH = "youth"
    ADULT = "adult"
    SENIOR = "senior"


class Age(DisaggregationModule):
    def __init__(self, *args, **kwargs):
        super().__init__(module_id="age", labels=AgeLabels, *args, **kwargs)
        self.AGES = [AgeLabels.CHILD, AgeLabels.YOUTH, AgeLabels.ADULT, AgeLabels.SENIOR]
        self.AGE_BREAKPOINTS = [0, 12, 20, 65]
        spacy_model = "en_core_web_lg"
        try:
            self.nlp = spacy.load(spacy_model, enable="ner")
        except OSError:
            raise ValueError(
                f"This disaggregation module depends on the {spacy_model} model from spaCy.\n"
                "You can install it by running: python -m spacy download en_core_web_sm"
            )

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

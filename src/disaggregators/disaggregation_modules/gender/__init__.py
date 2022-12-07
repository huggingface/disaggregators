from typing import Dict, List, Type

import pandas as pd
import spacy
from datasets import load_dataset

from ..disaggregation_module import DisaggregationModule, DisaggregationModuleConfig, DisaggregationModuleLabels


class GenderLabels(DisaggregationModuleLabels):
    MALE = "male"
    FEMALE = "female"


class GenderConfig(DisaggregationModuleConfig):
    def __init__(self, labels: Type[GenderLabels], word_lists: Dict[GenderLabels, List[str]]):
        self.labels = labels
        self.word_lists = word_lists


class Gender(DisaggregationModule):
    labels = GenderLabels
    spacy_model = "en_core_web_lg"

    citations = [
        """
        @inproceedings{dinan-etal-2020-multi,
            title = "Multi-Dimensional Gender Bias Classification",
            author = "Dinan, Emily  and
              Fan, Angela  and
              Wu, Ledell  and
              Weston, Jason  and
              Kiela, Douwe  and
              Williams, Adina",
            booktitle = "Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)", # noqa: E501
            year = "2020",
            publisher = "Association for Computational Linguistics",
            url = "https://www.aclweb.org/anthology/2020.emnlp-main.23",
            doi = "10.18653/v1/2020.emnlp-main.23",
        }
        """
    ]

    def __init__(self, *args, **kwargs):
        self.gender_df = load_dataset("md_gender_bias", "gendered_words", split="train").to_pandas()
        self.gender_df.columns = [GenderLabels.MALE, GenderLabels.FEMALE]

        try:
            self.nlp = spacy.load(self.spacy_model)
        except OSError:
            raise ValueError(
                f"This disaggregation module depends on the {self.spacy_model} model from spaCy.\n"
                f"You can install it by running: python -m spacy download {self.spacy_model}"
            )

        super().__init__(module_id="gender", *args, **kwargs)

    def _apply_config(self, config: GenderConfig):
        self.labels = config.labels
        for gender, word_list in config.word_lists.items():
            self.gender_df[gender] = pd.DataFrame(word_list)

    def __call__(self, row, *args, **kwargs):
        return_genders = {gender: False for gender in list(GenderLabels)}

        doc = self.nlp(row[self.column])

        nouns = [c.text for x in doc.noun_chunks for c in x.root.subtree]

        for noun in nouns:
            result = self.gender_df[self.gender_df == noun].any()
            for gender_hit in list(result[result].keys()):
                return_genders.update({gender_hit: True})

        return return_genders

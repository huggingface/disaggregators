import spacy
from datasets import load_dataset

from ..disaggregation_module import DisaggregationModule, DisaggregationModuleLabels


class GenderLabels(DisaggregationModuleLabels):
    MALE = "male"
    FEMALE = "female"


class Gender(DisaggregationModule):
    def __init__(self, *args, **kwargs):
        super().__init__(module_id="gender", labels=GenderLabels, *args, **kwargs)
        self.gender_df = load_dataset("md_gender_bias", "gendered_words", split="train").to_pandas()

        spacy_model = "en_core_web_lg"
        try:
            self.nlp = spacy.load(spacy_model)
        except OSError:
            raise ValueError(
                f"This disaggregation module depends on the {spacy_model} model from spaCy.\n"
                f"You can install it by running: python -m spacy download {spacy_model}"
            )

        self.citations = [
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

    def __call__(self, row, *args, **kwargs):
        return_genders = {gender: False for gender in GenderLabels}

        doc = self.nlp(row[self.column])

        nouns = [c.text for x in doc.noun_chunks for c in x.root.subtree]

        for noun in nouns:
            if noun in self.gender_df.word_masculine.values:
                return_genders.update({GenderLabels.MALE: True})
            if noun in self.gender_df.word_feminine.values:
                return_genders.update({GenderLabels.FEMALE: True})

        return return_genders

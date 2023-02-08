from typing import Dict, List, Type

import pandas as pd
import spacy
from datasets import load_dataset
from spacy.tokens import Span

from ..disaggregation_module import (
    DisaggregationModule,
    DisaggregationModuleConfig,
    DisaggregationModuleLabels,
)


class GenderLabels(DisaggregationModuleLabels):
    MALE = "male"
    FEMALE = "female"


class GenderConfig(DisaggregationModuleConfig):
    def __init__(
        self, labels: Type[GenderLabels], word_lists: Dict[GenderLabels, List[str]]
    ):
        self.labels = labels
        self.word_lists = word_lists


class Gender(DisaggregationModule):
    labels = GenderLabels
    required_spacy_components = ["tok2vec", "tagger", "parser", "attribute_ruler"]

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
        super().__init__(module_id="gender", *args, **kwargs)

        # TODO: think about expansion over word2vec
        self.gender_df = load_dataset(
            "md_gender_bias", "gendered_words", split="train"
        ).to_pandas()

        self.gender_df.columns = [GenderLabels.MALE, GenderLabels.FEMALE]

        assert len(self.nlp.vocab.vectors), (
            f"This disaggregation module depends on the a model with vectors"
            f" from spaCy.\nYou can install it by running: python -m spacy download"
            f" en_core_web_md or en_core_web_lg"
        )

    def _apply_config(self, config: GenderConfig):
        """
        > This function takes a config object and applies it to the gender classifier

        Args:
          config (GenderConfig): GenderConfig
        """
        self.labels = config.labels
        for gender, word_list in config.word_lists.items():
            self.gender_df[gender] = pd.DataFrame(word_list)

    def process_doc(self, doc: spacy.tokens.Doc, *args, **kwargs):
        return_genders = {gender: False for gender in list(GenderLabels)}

        # TODO: this is a sub-optimal way of matching. Consider using ruler or batched approach.
        nouns = [c for x in doc.noun_chunks for c in x.root.subtree]

        matched_spans = []
        for noun in nouns:
            result = self.gender_df[self.gender_df == noun.text.lower()].any()
            for gender_hit in list(result[result].keys()):
                matched_spans.append(
                    Span(
                        doc,
                        noun.i,
                        noun.i + noun.n_rights + 1,
                        label=f"{self.name}_{gender_hit}",
                    )
                )
                # TODO: consider using a counter and weighted average over classes and hit n_i/sum(nij)
                return_genders.update({gender_hit: True})
        if "sc" not in doc.spans:
            doc.spans["sc"] = matched_spans
        else:
            doc.spans["sc"].extend(matched_spans)

        if isinstance(doc.cats, dict):
            doc.cats.update(return_genders)
        else:
            doc.cats = return_genders

    def __call__(self, row, *args, **kwargs):
        doc = self.nlp(row)
        self.process_doc(doc, *args, **kwargs)
        return doc

    def pipe_docs(self, docs, *args, **kwargs):
        [self.process_doc(doc, *args, **kwargs) for doc in docs]

    def pipe(self, row, *args, **kwargs):
        docs = self.nlp.pipe(row)
        self.pipe_docs(docs, *args, **kwargs)
        return docs

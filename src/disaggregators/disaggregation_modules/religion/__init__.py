from typing import Type

from sentence_transformers import SentenceTransformer
from sentence_transformers.util import semantic_search

from ..disaggregation_module import DisaggregationModule, DisaggregationModuleConfig, DisaggregationModuleLabels


class ReligionLabels(DisaggregationModuleLabels):
    JUDAISM = "judaism"
    ISLAM = "islam"
    BUDDHISM = "buddhism"
    CHRISTIANITY = "christianity"


class ReligionConfig(DisaggregationModuleConfig):
    def __init__(self, labels: Type[ReligionLabels] = None, threshold: float = None):
        self.labels = labels
        self.threshold = threshold


class Religion(DisaggregationModule):
    labels = ReligionLabels
    threshold = 0.14  # Arbitrary threshold, hand-tuned.
    religions = [
        ReligionLabels.JUDAISM,
        ReligionLabels.ISLAM,
        ReligionLabels.BUDDHISM,
        ReligionLabels.CHRISTIANITY,
    ]

    def __init__(self, *args, **kwargs):
        self.model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

        super().__init__(module_id="religion", *args, **kwargs)

        self.embeddings = self.model.encode([str(religion) for religion in self.religions], convert_to_tensor=True)

    def _apply_config(self, config: ReligionConfig):
        if config.labels:
            self.labels = config.labels
            self.religions = self.religions + list(config.labels)

        self.threshold = config.threshold or self.threshold

    def __call__(self, row, *args, **kwargs):
        return_religion = {religion: False for religion in list(ReligionLabels)}

        query = self.model.encode(row[self.column], convert_to_tensor=True)
        religion_hit = semantic_search(query, self.embeddings, top_k=1)[0][0]

        if religion_hit["score"] > self.threshold:
            return_religion.update({self.religions[religion_hit["corpus_id"]]: True})

        return return_religion

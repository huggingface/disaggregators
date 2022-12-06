from typing import Dict, Set, Type

from ..disaggregation_module import DisaggregationModule, DisaggregationModuleConfig, DisaggregationModuleLabels


class PronounLabels(DisaggregationModuleLabels):
    SHE_HER = "she_her"
    HE_HIM = "he_him"
    THEY_THEM = "they_them"


class PronounConfig(DisaggregationModuleConfig):
    def __init__(self, labels: Type[PronounLabels], pronouns: Dict[PronounLabels, Set[str]]):
        self.labels = labels
        self.pronouns = pronouns


class Pronoun(DisaggregationModule):
    labels = PronounLabels
    AVAILABLE_PRONOUNS = {
        PronounLabels.SHE_HER: {"she", "her", "hers", "herself"},
        PronounLabels.HE_HIM: {"he", "him", "his", "himself"},
        PronounLabels.THEY_THEM: {"they", "them", "their", "theirs", "themself", "themselves"},
    }

    def __init__(self, *args, **kwargs):
        super().__init__(module_id="pronoun", *args, **kwargs)

    def _apply_config(self, config: PronounConfig):
        self.labels = config.labels
        self.AVAILABLE_PRONOUNS = {**config.pronouns, **self.AVAILABLE_PRONOUNS}

    def __call__(self, row, *args, **kwargs):
        text = row[self.column]
        pronoun_flag = {
            av_p: any(p in text.lower().split() for p in self.AVAILABLE_PRONOUNS[av_p])
            for av_p in self.AVAILABLE_PRONOUNS
        }

        return pronoun_flag

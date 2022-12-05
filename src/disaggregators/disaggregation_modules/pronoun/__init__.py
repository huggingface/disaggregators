from ..disaggregation_module import DisaggregationModule, DisaggregationModuleLabels


class PronounLabels(DisaggregationModuleLabels):
    SHE_HER = "she_her"
    HE_HIM = "he_him"
    THEY_THEM = "they_them"


class Pronoun(DisaggregationModule):
    def __init__(self, *args, **kwargs):
        super().__init__(module_id="pronoun", labels=PronounLabels, *args, **kwargs)
        self.AVAILABLE_PRONOUNS = {
            PronounLabels.SHE_HER: {"she", "her", "hers", "herself"},
            PronounLabels.HE_HIM: {"he", "him", "his", "himself"},
            PronounLabels.THEY_THEM: {"they", "them", "their", "theirs", "themself", "themselves"},
        }

    def __call__(self, row, *args, **kwargs):
        text = row[self.column]
        pronoun_flag = {
            av_p: any(p in text.lower() for p in self.AVAILABLE_PRONOUNS[av_p]) for av_p in self.AVAILABLE_PRONOUNS
        }

        return pronoun_flag
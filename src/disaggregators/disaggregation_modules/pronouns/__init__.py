from ..disaggregation_module import DisaggregationModule, DisaggregationModuleLabels


class PronounsLabels(DisaggregationModuleLabels):
    SHE_HER = "she_her"
    HE_HIM = "he_him"
    THEY_THEM = "they_them"


class Pronouns(DisaggregationModule):
    def __init__(self, *args, **kwargs):
        super().__init__(module_id="pronouns", labels=PronounsLabels, *args, **kwargs)
        self.AVAILABLE_PRONOUNS = {
            PronounsLabels.SHE_HER: {"she", "her", "hers", "herself"},
            PronounsLabels.HE_HIM: {"he", "him", "his", "himself"},
            PronounsLabels.THEY_THEM: {"they", "them", "their", "theirs", "themself", "themselves"},
        }

    def __call__(self, row, *args, **kwargs):
        text = row[self.column]
        pronoun_flag = {
            av_p: any(p in text.lower() for p in self.AVAILABLE_PRONOUNS[av_p]) for av_p in self.AVAILABLE_PRONOUNS
        }

        return pronoun_flag

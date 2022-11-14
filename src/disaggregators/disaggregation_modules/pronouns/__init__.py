from ..disaggregation_module import DisaggregationModule


class Pronouns(DisaggregationModule):
    def __init__(self, *args, **kwargs):
        super().__init__(module_id="pronouns", *args, **kwargs)
        self.AVAILABLE_PRONOUNS = {
            "she/her": {"she", "her", "hers", "herself"},
            "he/him": {"he", "him", "his", "himself"},
            "they/them": {"they", "them", "their", "theirs", "themself", "themselves"},
        }

    def __call__(self, row, *args, **kwargs):
        text = row[self.column]
        pronoun_flag = {
            av_p: any(p in text.lower() for p in self.AVAILABLE_PRONOUNS[av_p]) for av_p in self.AVAILABLE_PRONOUNS
        }

        return pronoun_flag

from disaggregators.disaggregation_modules.pronoun import Pronoun, PronounLabels


def test_initialize():
    disagg_module = Pronoun(column=None)
    assert disagg_module.name == "pronoun"
    assert set(disagg_module.labels) == {PronounLabels.HE_HIM, PronounLabels.SHE_HER, PronounLabels.THEY_THEM}


def test_call_default():
    data = {"text": "He went to the park."}
    disagg_module = Pronoun(column="text")
    results = disagg_module(data)
    assert results == {PronounLabels.HE_HIM: True, PronounLabels.SHE_HER: False, PronounLabels.THEY_THEM: False}

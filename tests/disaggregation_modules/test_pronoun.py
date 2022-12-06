from disaggregators.disaggregation_modules.pronoun import Pronoun, PronounConfig, PronounLabels


def test_initialize():
    disagg_module = Pronoun(column=None)
    assert disagg_module.name == "pronoun"
    assert set(disagg_module.labels) == {PronounLabels.HE_HIM, PronounLabels.SHE_HER, PronounLabels.THEY_THEM}


def test_call_default():
    data = {"text": "He went to the park."}
    disagg_module = Pronoun(column="text")
    results = disagg_module(data)
    assert results == {PronounLabels.HE_HIM: True, PronounLabels.SHE_HER: False, PronounLabels.THEY_THEM: False}


def test_call_custom():
    class CustomPronounLabels(PronounLabels):
        ZE_ZIR = "ze_zir"

    _CUSTOM_PRONOUN_MAPPING = {CustomPronounLabels.ZE_ZIR: {"ze", "zir", "zirs", "zirself"}}

    data = {"text": "Ze went to the park."}
    disagg_module = Pronoun(
        config=PronounConfig(labels=CustomPronounLabels, pronouns=_CUSTOM_PRONOUN_MAPPING), column="text"
    )
    results = disagg_module(data)
    assert results == {
        CustomPronounLabels.ZE_ZIR: True,
        CustomPronounLabels.HE_HIM: False,
        CustomPronounLabels.SHE_HER: False,
        CustomPronounLabels.THEY_THEM: False,
    }

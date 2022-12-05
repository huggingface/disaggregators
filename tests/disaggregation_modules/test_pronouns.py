from disaggregators.disaggregation_modules.pronouns import Pronouns, PronounsLabels


def test_initialize():
    disagg_module = Pronouns(column=None)
    assert disagg_module.name == "pronouns"
    assert disagg_module.labels == {PronounsLabels.HE_HIM, PronounsLabels.SHE_HER, PronounsLabels.THEY_THEM}


def test_call_default_pronouns():
    data = {"text": "He went to the park."}
    disagg_module = Pronouns(column="text")
    results = disagg_module(data)
    assert results == {PronounsLabels.HE_HIM: True, PronounsLabels.SHE_HER: False, PronounsLabels.THEY_THEM: False}

import pytest

from disaggregators.disaggregation_modules.gender import Gender, GenderLabels


def test_initialize():
    disagg_module = Gender(column=None)
    assert disagg_module.name == "gender"
    assert set(disagg_module.labels) == {GenderLabels.MALE, GenderLabels.FEMALE}


@pytest.mark.slow
@pytest.mark.parametrize(
    "text,expected",
    [
        ("That is one large cat!", []),
        ("The 40-year-old man went to the park.", [GenderLabels.MALE]),
        ("The clown gave the girl an ice cream cone.", [GenderLabels.FEMALE]),
        ("What is the boy's name?", [GenderLabels.MALE]),
        ("I checked the lady's ticket.", [GenderLabels.FEMALE]),
        ("The guy gave the woman a high-five.", [GenderLabels.MALE, GenderLabels.FEMALE]),
    ],
)
def test_call_default_pronouns(text, expected):
    base_labels = {age: False for age in GenderLabels}
    data = {"text": text}
    disagg_module = Gender(column="text")
    results = disagg_module(data)
    assert results == {**base_labels, **{label: True for label in expected}}

import pytest

from disaggregators.disaggregation_modules.gender import Gender, GenderConfig, GenderLabels


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
def test_call_default(text, expected):
    base_labels = {age: False for age in list(GenderLabels)}
    data = {"text": text}
    disagg_module = Gender(column="text")
    results = disagg_module(data)
    assert results == {**base_labels, **{label: True for label in expected}}


@pytest.mark.slow
def test_call_custom():
    class CustomGenderLabels(GenderLabels):
        NON_BINARY = "non-binary"

    _CUSTOM_WORD_LISTS = {CustomGenderLabels.NON_BINARY: ["clown"]}

    data = {"text": "The sad clown went to the doctor."}
    disagg_module = Gender(
        config=GenderConfig(labels=CustomGenderLabels, word_lists=_CUSTOM_WORD_LISTS), column="text"
    )
    results = disagg_module(data)
    assert results == {
        CustomGenderLabels.MALE: False,
        CustomGenderLabels.FEMALE: False,
        CustomGenderLabels.NON_BINARY: True,
    }

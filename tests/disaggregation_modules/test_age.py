import pytest

from disaggregators.disaggregation_modules.age import Age, AgeLabels


def test_initialize():
    disagg_module = Age(column=None)
    assert disagg_module.name == "age"
    assert set(disagg_module.labels) == {AgeLabels.CHILD, AgeLabels.YOUTH, AgeLabels.ADULT, AgeLabels.SENIOR}


@pytest.mark.slow
@pytest.mark.parametrize(
    "text,expected",
    [
        ("The man went to the park.", []),
        ("The 40-year-old man went to the park.", [AgeLabels.ADULT]),
        ("The 10 year old child ate a hot dog.", [AgeLabels.CHILD]),
        ("Clara is 18 years old.", [AgeLabels.YOUTH]),
        ("Hamed's grandpa is an 86 yr old smoker.", [AgeLabels.SENIOR]),
        ("The 40-year-old man went to the park with his 10 year old daughter.", [AgeLabels.ADULT, AgeLabels.CHILD]),
        ("Farzaneh is 18 years old and her grandmother is 86 yrs old", [AgeLabels.YOUTH, AgeLabels.SENIOR]),
    ],
)
def test_call_default_pronouns(text, expected):
    base_labels = {age: False for age in AgeLabels}
    data = {"text": text}
    disagg_module = Age(column="text")
    results = disagg_module(data)
    assert results == {**base_labels, **{label: True for label in expected}}

import pytest

from disaggregators.disaggregation_modules.continent import Continent, ContinentLabels


def test_initialize():
    disagg_module = Continent(column=None)
    assert disagg_module.name == "continent"
    assert set(disagg_module.labels) == {
        ContinentLabels.AFRICA,
        ContinentLabels.AMERICAS,
        ContinentLabels.ASIA,
        ContinentLabels.EUROPE,
        ContinentLabels.OCEANIA,
    }


@pytest.mark.slow
@pytest.mark.parametrize(
    "text,expected",
    [
        (
            "Tomorrow I am visiting Italy.",
            [ContinentLabels.EUROPE],
        ),
        (
            "A gentle breeze blows through the leaves of a cherry blossom tree in Vancouver.",
            [ContinentLabels.AMERICAS],
        ),
        (
            "Let's eat pizza.",
            [],
        ),
    ],
)
def test_call_default(text, expected):
    base_labels = {age: False for age in list(ContinentLabels)}
    data = {"text": text}
    disagg_module = Continent(column="text")
    results = disagg_module(data)
    assert results == {**base_labels, **{label: True for label in expected}}

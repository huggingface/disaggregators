import pytest

from disaggregators.disaggregation_modules.religion import Religion, ReligionConfig, ReligionLabels


def test_initialize():
    disagg_module = Religion(column=None)
    assert disagg_module.name == "religion"
    assert set(disagg_module.labels) == {
        ReligionLabels.JUDAISM,
        ReligionLabels.ISLAM,
        ReligionLabels.BUDDHISM,
        ReligionLabels.CHRISTIANITY,
    }


@pytest.mark.slow
@pytest.mark.parametrize(
    "text,expected",
    [
        (
            "The menorah is a seven-branched candelabrum that is described in the Hebrew Bible.",
            [ReligionLabels.JUDAISM],
        ),
        (
            "Traditionally, Eid al-Fitr begins at sunset on the night of the first sighting of the crescent moon.",
            [ReligionLabels.ISLAM],
        ),
        (
            "Three main prevailing theories exist on the finalization of Lent as a forty-day fast"
            "prior to the arrival of Easter Sunday.",
            [ReligionLabels.CHRISTIANITY],
        ),
        (
            "Samsara means 'wandering' or 'world', with the connotation of cyclic, circuitous change.",
            [ReligionLabels.BUDDHISM],
        ),
        (
            "CBC Music is a Canadian FM radio network operated by the Canadian Broadcasting Corporation.",
            [],
        ),
    ],
)
def test_call_default(text, expected):
    base_labels = {age: False for age in list(ReligionLabels)}
    data = {"text": text}
    disagg_module = Religion(column="text")
    results = disagg_module(data)
    assert results == {**base_labels, **{label: True for label in expected}}


@pytest.mark.slow
def test_call_custom():
    class CustomReligionLabels(ReligionLabels):
        BOKONONISM = "bokononism"

    data = {"text": "Busy, busy, busy."}
    disagg_module = Religion(config=ReligionConfig(labels=CustomReligionLabels), column="text")

    results = disagg_module(data)

    assert results[CustomReligionLabels.BOKONONISM]

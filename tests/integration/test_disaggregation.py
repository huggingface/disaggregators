import pandas as pd
import pytest
from datasets import Dataset, load_dataset

from disaggregators import Disaggregator


@pytest.fixture()
def dataset():
    return load_dataset("medmcqa", split="test").select(range(100))


@pytest.fixture()
def disaggregator():
    return Disaggregator(["age", "gender"], column="question")


@pytest.fixture()
def expected_features():
    return {
        "age.child",
        "age.youth",
        "age.adult",
        "age.senior",
        "gender.male",
        "gender.female",
    }


def test_datasets(dataset, disaggregator, expected_features):
    ds_mapped = dataset.map(disaggregator)
    assert expected_features.issubset(set(ds_mapped.features))


def test_pandas(dataset, disaggregator, expected_features):
    df = dataset.to_pandas()
    new_cols = df.apply(disaggregator, axis=1)
    df = pd.merge(df, pd.json_normalize(new_cols), left_index=True, right_index=True)
    assert expected_features.issubset(set(df.columns))


def test_each_module(module):
    disaggregator = Disaggregator(module, column="text")
    dataset = Dataset.from_dict({"text": ["Hello", "World"]})
    ds_mapped = dataset.map(disaggregator)

    expected_features = disaggregator.fields

    assert expected_features.issubset(set(ds_mapped.features))

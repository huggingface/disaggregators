# Disaggregators

The `disaggregators` library allows you to easily add new features to your datasets to enable disaggregated data exploration and disaggregated model evaluation. `disaggregators` is preloaded with disaggregation modules intended for text and image data.

`disaggregators` is intended to be used with 🤗 Datasets, but should work with any other "mappable" interface to a dataset. 

# Requirements and Installation

`disaggregators` has been tested on Python 3.10.8.

`pip install disaggregators` will fetch the latest release from PyPI.

To install directly from this GitHub repo, use the following command:
```shell
pip install git+https://github.com/huggingface/disaggregators.git
```

# Usage

You will likely want to use 🤗 Datasets with `disaggregators`.

```shell
pip install datasets
```

The snippet below loads the IMDB dataset from the Hugging Face Hub, and initializes a disaggregator for "pronouns" that will run on the IMDB dataset's "text" column. Note that if you would like to run multiple disaggregations, you can pass a list to the `Disaggregator` constructor (e.g. `Disaggregator(["pronouns", "sentiment"], column="text")`). We then use the 🤗 Datasets `map` method to apply the disaggregation to the dataset.

```python
from disaggregators import Disaggregator
from datasets import load_dataset

dataset = load_dataset("imdb", split="train")
disaggregator = Disaggregator("pronouns", column="text")

ds = dataset.map(disaggregator.get_function())  # New boolean columns are added for she/her, he/him, and they/them
```

The resulting dataset can now be used for data exploration and disaggregated model evaluation.

# Contact

Nima Boscarino – `nima <at> huggingface <dot> co`
# Disaggregators

The `disaggregators` library allows you to easily add new features to your datasets to enable disaggregated data exploration and disaggregated model evaluation. `disaggregators` is preloaded with disaggregation modules intended for text and image data.

`disaggregators` is intended to be used with 🤗 Datasets, but should work with any other "mappable" interface to a dataset. 

## Requirements and Installation

`disaggregators` has been tested on Python 3.10.8.

`pip install disaggregators` will fetch the latest release from PyPI.

Note that some disaggregation modules require extra dependencies such as SpaCy modules, which may need to be installed manually. If these dependencies aren't installed, `disaggregators` will inform you about how to install them.

To install directly from this GitHub repo, use the following command:
```shell
pip install git+https://github.com/huggingface/disaggregators.git
```

# Usage

You will likely want to use 🤗 Datasets with `disaggregators`.

```shell
pip install datasets
```

The snippet below loads the IMDB dataset from the Hugging Face Hub, and initializes a disaggregator for "pronoun" that will run on the IMDB dataset's "text" column. Note that if you would like to run multiple disaggregations, you can pass a list to the `Disaggregator` constructor (e.g. `Disaggregator(["pronoun", "sentiment"], column="text")`). We then use the 🤗 Datasets `map` method to apply the disaggregation to the dataset.

```python
from disaggregators import Disaggregator
from datasets import load_dataset

dataset = load_dataset("imdb", split="train")
disaggregator = Disaggregator("pronoun", column="text")

ds = dataset.map(disaggregator)  # New boolean columns are added for she/her, he/him, and they/them
```

The resulting dataset can now be used for data exploration and disaggregated model evaluation.

## Development

Development requirements can be installed with `pip install .[dev]`. See the `Makefile` for useful targets, such as code quality and test running.

To run tests locally across multiple Python versions (3.8, 3.9, and 3.10), ensure that you have all the Python versions available and then run `nox -r`. Note that this is quite slow, so it's only worth doing to double-check your code before you open a Pull Request.

## Contact

Nima Boscarino – `nima <at> huggingface <dot> co`
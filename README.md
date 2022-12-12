<p align="center">
    <br>
    <img alt="Hugging Face Disaggregators" src="https://user-images.githubusercontent.com/6765188/206785111-b7724be3-6460-4092-9561-9fc2cd522320.png" width="400"/>
    <br>
<p>

<p align="center">
    <a href="https://huggingface.co/spaces/society-ethics/disaggregators">
        <img alt="GitHub" src="https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face%20Spaces-Demo-blue">
    </a>
    <a href="https://github.com/huggingface/transformers/releases">
        <img alt="GitHub release" src="https://img.shields.io/github/release/huggingface/disaggregators.svg">
    </a>
</p>

> ⚠️ Please note: This library is in early development, and the disaggregation modules that are included are proofs of concept that are _not_ production-ready. Additionally, all APIs are subject to breaking changes any time before a 1.0.0 release. Rigorously tested versions of the included modules will be released in the future, so stay tuned. [We'd love your feedback in the meantime!](https://github.com/huggingface/disaggregators/discussions/23)

The `disaggregators` library allows you to easily add new features to your datasets to enable disaggregated data exploration and disaggregated model evaluation. `disaggregators` is preloaded with disaggregation modules for text data, with image modules coming soon!

This library is intended to be used with [🤗 Datasets](https://github.com/huggingface/datasets), but should work with any other "mappable" interface to a dataset. 

## Requirements and Installation

`disaggregators` has been tested on Python 3.8, 3.9, and 3.10.

`pip install disaggregators` will fetch the latest release from PyPI.

Note that some disaggregation modules require extra dependencies such as SpaCy modules, which may need to be installed manually. If these dependencies aren't installed, `disaggregators` will inform you about how to install them.

To install directly from this GitHub repo, use the following command:
```shell
pip install git+https://github.com/huggingface/disaggregators.git
```

## Usage

You will likely want to use 🤗 Datasets with `disaggregators`.

```shell
pip install datasets
```

The snippet below loads the IMDB dataset from the Hugging Face Hub, and initializes a disaggregator for "pronoun" that will run on the IMDB dataset's "text" column. If you would like to run multiple disaggregations, you can pass a list to the `Disaggregator` constructor (e.g. `Disaggregator(["pronoun", "sentiment"], column="text")`). We then use the 🤗 Datasets `map` method to apply the disaggregation to the dataset.

```python
from disaggregators import Disaggregator
from datasets import load_dataset

dataset = load_dataset("imdb", split="train")
disaggregator = Disaggregator("pronoun", column="text")

ds = dataset.map(disaggregator)  # New boolean columns are added for she/her, he/him, and they/them
```

The resulting dataset can now be used for data exploration and disaggregated model evaluation.

You can also run disaggregations on Pandas DataFrames with `.apply` and `.merge`:

```python
from disaggregators import Disaggregator
import pandas as pd
df = pd.DataFrame({"text": ["They went to the park."]})

disaggregator = Disaggregator("pronoun", column="text")

new_cols = df.apply(disaggregator, axis=1)
df = pd.merge(df, pd.json_normalize(new_cols), left_index=True, right_index=True)
```

### Available Disaggregation Modules

The following modules are currently available:

- `"age"`
- `"gender"`
- `"pronoun"`
- `"religion"`
- `"continent"`

Note that `disaggregators` is in active development, and that these (and future) modules are subject to changing interfaces and implementations at any time before a `1.0.0` release. Each module provides its own method for overriding the default configuration, with the general interface documented below.

### Module Configurations

Modules may make certain variables and functionality configurable. If you'd like to configure a module, import the module, its labels, and its config class. Then, override the labels and set the configuration as needed while instantiating the module. Once instantiated, you can pass the module to the `Disaggregator`. The example below shows this with the `Age` module.

```python
from disaggregators import Disaggregator
from disaggregators.disaggregation_modules.age import Age, AgeLabels, AgeConfig

class MeSHAgeLabels(AgeLabels):
    INFANT = "infant"
    CHILD_PRESCHOOL = "child_preschool"
    CHILD = "child"
    ADOLESCENT = "adolescent"
    ADULT = "adult"
    MIDDLE_AGED = "middle_aged"
    AGED = "aged"
    AGED_80_OVER = "aged_80_over"

age = Age(
    config=AgeConfig(
        labels=MeSHAgeLabels,
        ages=[list(MeSHAgeLabels)],
        breakpoints=[0, 2, 5, 12, 18, 44, 64, 79]
    ),
    column="question"
)

disaggregator = Disaggregator([age, "gender"], column="question")
```

### Custom Modules

Custom modules can be created by extending the `CustomDisaggregator`. All custom modules must have `labels` and a `module_id`, and must implement a `__call__` method.

```python
from disaggregators import Disaggregator, DisaggregationModuleLabels, CustomDisaggregator

class TabsSpacesLabels(DisaggregationModuleLabels):
    TABS = "tabs"
    SPACES = "spaces"

class TabsSpaces(CustomDisaggregator):
    module_id = "tabs_spaces"
    labels = TabsSpacesLabels

    def __call__(self, row, *args, **kwargs):
        if "\t" in row[self.column]:
            return {self.labels.TABS: True, self.labels.SPACES: False}
        else:
            return {self.labels.TABS: False, self.labels.SPACES: True}

disaggregator = Disaggregator(TabsSpaces, column="text")
```

## Development

Development requirements can be installed with `pip install .[dev]`. See the `Makefile` for useful targets, such as code quality and test running.

To run tests locally across multiple Python versions (3.8, 3.9, and 3.10), ensure that you have all the Python versions available and then run `nox -r`. Note that this is quite slow, so it's only worth doing to double-check your code before you open a Pull Request.

## Contact

Nima Boscarino – `nima <at> huggingface <dot> co`

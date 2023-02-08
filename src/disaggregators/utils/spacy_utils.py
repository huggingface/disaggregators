from typing import Optional, Union

import spacy
from spacy import Language


def language_check(language: Optional[Union[Language, str]] = None):
    """
    If the language is a string, then we check if it's a two-letter code. If it is, we create a blank
    model with that language. If it's not, we assume it's a model name and load the model. If the
    language is not a string, we assume it's a model and use that

    Args:
      language (Optional[Union[Language, str]]): Optional[Union[Language, str]] = None. Defaults to None

    Returns:
      A function that takes a language as an argument and returns a language model.
    """
    if language is None:
        language = "en"

    if isinstance(language, str):
        if len(language) == 2:
            nlp = spacy.blank(language)
        else:
            nlp = spacy.load(language)
    else:
        nlp = language
    return nlp

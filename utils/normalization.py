from abc import ABC, abstractmethod
import string
import pymorphy2
import json
from utils import constants as cnts

import nltk
from nltk.stem import WordNetLemmatizer
nltk.download("wordnet", quiet=True)


class Normalizer(ABC):
    def __init__(self, ingredients_mapping_file: str) -> None:
        """
        Class for query normalization

        :param str, ingredients_mapping_file: mapping with renamed ingredients
        """

        with open(ingredients_mapping_file) as f:
            self._mapping = json.load(f)

    def _remove_punctuation(self, text: str) -> str:
        return text.translate(str.maketrans(cnts.EMPTY_STR, cnts.EMPTY_STR, string.punctuation))

    @abstractmethod
    def normalize(self, text: str) -> str:
        """
        Perform text normalization
        :param str, text: raw text
        :return str: normalized query
        """
        pass


class RuNormalizer(Normalizer):
    def __init__(self, ingredients_mapping_file: str):
        super().__init__(ingredients_mapping_file)
        self._morph = pymorphy2.MorphAnalyzer()

    def normalize(self, text: str) -> str:
        text = text.lower()
        text = self._remove_punctuation(text)
        text_norm = []

        for token in text.split():
            token_norm = self._morph.parse(token)[0].normal_form
            # token_norm = token_norm.replace("ё", "е")
            if token_norm in self._mapping:
                token_norm = self._mapping[token_norm]

            text_norm.append(token_norm)

        return cnts.SPACE_STR.join(text_norm)


class EnNormalizer(Normalizer):
    def __init__(self, query_expansion_file: str):
        super().__init__(query_expansion_file)
        self._lemmatizer = WordNetLemmatizer()

    def normalize(self, text: str) -> str:
        text = text.lower()
        text = self._remove_punctuation(text)
        text_norm = []

        for token in text.split():
            token_norm = self._lemmatizer.lemmatize(token)
            if token_norm in self._mapping:
                token_norm = self._mapping[token_norm]
            text_norm.append(token_norm)

        return cnts.SPACE_STR.join(text_norm)

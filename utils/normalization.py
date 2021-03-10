from abc import ABC, abstractmethod
from typing import Dict
import string
import pymorphy2
import json

import nltk
nltk.download("wordnet")
from nltk.stem import WordNetLemmatizer

class Normalizer(ABC):
    def __init__(self, query_expansion_file: str):
        self._mapping = self._get_expansion_mapping(query_expansion_file)

    def _remove_punctuation(self, text: str) -> str:
        return text.translate(str.maketrans("", "", string.punctuation))

    def _get_expansion_mapping(self, query_expansion_file: str) -> Dict:
        with open(query_expansion_file) as f:
            mapping = json.load(f)
        return mapping

    @abstractmethod
    def normalize(self, text: str) -> str:
        pass

class RuNormalizer(Normalizer):
    def __init__(self, query_expansion_file: str):
        super().__init__(query_expansion_file)
        self._morph = pymorphy2.MorphAnalyzer()

    def normalize(self, text: str) -> str:
        text = text.lower()
        text = self._remove_punctuation(text)
        text_norm = []

        for token in text.split():
            token_norm = self._morph.parse(token)[0].normal_form
            token_norm = token_norm.replace("ё", "е")
            exp_value = self._mapping.get(token_norm)
            if exp_value is not None:
                token_norm = exp_value

            text_norm.append(token_norm)

        return " ".join(text_norm)


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
            exp_value = self._mapping.get(token_norm)
            if exp_value is not None:
                token_norm = exp_value
            text_norm.append(token_norm)

        return " ".join(text_norm)



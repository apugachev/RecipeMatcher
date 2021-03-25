import unittest
import tempfile
import shutil
import json
import os

from utils.normalization import RuNormalizer, EnNormalizer

mock_mapping = {
    "fish": "salmon",
    "рыба": "лосось"
}

class TestRuNormalizer(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)

    def get_temp_path(self):
        path = os.path.join(self.test_dir, "temp.json")
        with open(path, 'w') as json_file:
            json.dump(mock_mapping, json_file, ensure_ascii=False, indent=4)

        return path

    def test_remove_punctuation(self):
        normalizer = RuNormalizer(self.get_temp_path())

        self.assertEqual(normalizer._remove_punctuation(",."), "")
        self.assertEqual(normalizer._remove_punctuation("картошка, томат:!"), "картошка томат")
        self.assertEqual(normalizer._remove_punctuation("морковь? : ! ,"), "морковь   ")

    def test_normalize(self):
        normalizer = RuNormalizer(self.get_temp_path())

        self.assertEqual(normalizer.normalize("свекла"), "свёкла")
        self.assertEqual(normalizer.normalize("Сметана"), "сметана")
        self.assertEqual(normalizer.normalize("сгущённое молоко"), "сгустить молоко")
        self.assertEqual(normalizer.normalize("РЫБЫ курица"), "лосось курица")
        self.assertEqual(normalizer.normalize("Яйца! мука СЫР."), "яйцо мука сыр")

class TestENNormalizer(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)

    def get_temp_path(self):
        path = os.path.join(self.test_dir, "temp.json")
        with open(path, 'w') as json_file:
            json.dump(mock_mapping, json_file, ensure_ascii=False, indent=4)

        return path

    def test_remove_punctuation(self):
        normalizer = EnNormalizer(self.get_temp_path())

        self.assertEqual(normalizer._remove_punctuation(",."), "")
        self.assertEqual(normalizer._remove_punctuation("potato, tomato:!"), "potato tomato")
        self.assertEqual(normalizer._remove_punctuation("carrot? : ! ,"), "carrot   ")

    def test_normalize(self):
        normalizer = EnNormalizer(self.get_temp_path())

        self.assertEqual(normalizer.normalize("two fishes"), "two salmon")
        self.assertEqual(normalizer.normalize("Mushrooms"), "mushroom")
        self.assertEqual(normalizer.normalize("milk Eggs"), "milk egg")
        self.assertEqual(normalizer.normalize("carrot? tomato,"), "carrot tomato")
        self.assertEqual(normalizer.normalize(")APPLE cheese.."), "apple cheese")

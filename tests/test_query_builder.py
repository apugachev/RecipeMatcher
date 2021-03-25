import unittest
from utils.constants import NUM_SEARCH_RESULT_DOCS

from utils.query_builder import QueryBuilder

class TestQueryBuilder(unittest.TestCase):

    def test_query_builder(self):
        query_builder = QueryBuilder()

        self.assertEqual(query_builder.build_elastic_query("milk egg"),
                         {"size": NUM_SEARCH_RESULT_DOCS, "query": {"bool": {"should": [
                             {
                                 "term": {"ingredients_lemm": "milk"}},
                             {
                                 "term": {"ingredients_lemm": "egg"}}
                         ]}}})

        self.assertEqual(query_builder.build_elastic_query("pear"),
                         {"size": NUM_SEARCH_RESULT_DOCS, "query": {"bool": {"should": [
                             {
                                 "term": {"ingredients_lemm": "pear"}}
                         ]}}})



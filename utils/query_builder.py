from typing import Dict, Any
from utils.constants import NUM_SEARCH_RESULT_DOCS

class QueryBuilder():
    def __init__(self):
        pass

    def build_elastic_query(self, text: str) -> Dict[str, Any]:

        should = []
        for token in text.split():
            should.append({
                "term": {
                    "ingredients_lemm": token
                }})

        return {
            "size": NUM_SEARCH_RESULT_DOCS,
            "query": {
                "bool": {
                    "should": should
                    }
                },
            }

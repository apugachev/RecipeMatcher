import json
import requests
import json_lines
from typing import List, Dict
from utils import constants as cnts


class Indexer:
    def __init__(
        self,
        ru_data_path: str,
        en_data_path: str
    ) -> None:

        self._ru_data = self._load_data(ru_data_path)
        self._en_data = self._load_data(en_data_path)

    def _load_data(self, path: str) -> List[Dict[str, str]]:

        data = []
        with open(path, 'rb') as f:
            for item in json_lines.reader(f):
                data.append(item)

        return data

    def _get_chunks(self, docs, chunk_size):
        for i in range(0, len(docs), chunk_size):
            yield docs[i:i + chunk_size]

    def _upload_chunks(self,
                      docs: List[Dict[str, str]],
                      url: str,
                      chunk_size: int = 10000
                      ) -> None:

        headers = {"Content-Type": "application/x-ndjson"}

        for chunk in self._get_chunks(docs, chunk_size):
            data = []
            for doc_obj in chunk:
                doc_id = doc_obj["id"]
                data.append(
                    json.dumps({
                        "index": {
                            "_id": doc_id,
                            "_type": "_doc"
                        }
                    })
                )
                data.append(json.dumps(doc_obj))

            data = "\n".join(data) + "\n"
            response = requests.post(url,
                                     data=data,
                                     headers=headers)
            if response.status_code != 200:
                print(response)
                print(response.text)

    def index_data(self,
                   index_ru: bool = False,
                   index_en: bool = False):

        if index_ru:
            self._upload_chunks(
                self._ru_data,
                f"http://{cnts.HOST}:{cnts.PORT}/{cnts.RU_INDEX_NAME}/_bulk"
            )

        if index_en:
            self._upload_chunks(
                self._en_data,
                f"http://{cnts.HOST}:{cnts.PORT}/{cnts.EN_INDEX_NAME}/_bulk"
            )

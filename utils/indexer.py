import logging
import json
import requests
import json_lines
from typing import List, Dict, Generator, Any
from utils import constants as cnts


class Indexer:
    HEADER = {"Content-Type": "application/x-ndjson"}

    def __init__(self,
                 ru_data_path: str,
                 en_data_path: str
                 ) -> None:

        self._ru_data = self._load_data(ru_data_path)
        self._en_data = self._load_data(en_data_path)

    def _load_data(self, path: str) -> List[Dict[str, str]]:
        """
        Load documents from disk

        :param str path: path to .jsonl file
        :return: List: documents for indexing
        """

        data = []
        with open(path, "rb") as f:
            for item in json_lines.reader(f):
                data.append(item)
        return data

    def _get_chunks(self,
                    docs: List[Dict[str, Any]],
                    chunk_size: int
                    ) -> Generator[List[Dict[str, Any]],
                                   List[Dict[str, Any]]]:
        """
        Split documents on chunks of a certain size

        :param List, docs: list of documents
        :param int, chunk_size: size of chunks
        :return: Generator: yielded chunks of documents
        """

        for i in range(0, len(docs), chunk_size):
            yield docs[i:i + chunk_size]

    def _push_documents_to_elastic(self,
                                   docs: List[Dict[str, str]],
                                   url: str,
                                   chunk_size: int = cnts.CHUNK_SIZE
                                   ) -> bool:
        """
        Push documents to elastic index

        :param List, docs: list of documents
        :param str, url: elastic url where to put documents
        :param int, chunk_size: chunk size when splitting documents
        :return: bool: whether the documents were pushed successfully
        """

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
                                     headers=self.HEADER)
            if response.status_code != cnts.SUCCESS_STATUS_CODE:
                print(response)
                print(response.text)
                return False

            return True

    def index_data(self,
                   index_ru: bool = False,
                   index_en: bool = False
                   ) -> None:
        """
        Perform data indexing

        :param bool, index_ru: whether to index RU data
        :param bool, index_en: whether to index EN data
        :return:
        """

        if index_ru:
            success = self._push_documents_to_elastic(
                self._ru_data,
                f"http://{cnts.HOST}:{cnts.PORT}/{cnts.RU_INDEX_NAME}/_bulk"
            )
            if success:
                logging.info(f"{len(self._ru_data)} RU documents indexed successfully!")

        if index_en:
            success = self._push_documents_to_elastic(
                self._en_data,
                f"http://{cnts.HOST}:{cnts.PORT}/{cnts.EN_INDEX_NAME}/_bulk"
            )
            if success:
                logging.info(f"{len(self._en_data)} EN documents indexed successfully!")

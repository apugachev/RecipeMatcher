from flask import Flask, render_template, request
import requests
import re
import os
from utils import constants as cnts
from utils.normalization import RuNormalizer, EnNormalizer
from utils.query_builder import QueryBuilder
from utils.indexer import Indexer

import logging
from logging import FileHandler, StreamHandler
import datetime

# export FLASK_APP=app
# export FLASK_ENV=development

ru_normalizer = RuNormalizer(cnts.INGREDIENTS_MAPPING_PATH)
en_normalizer = EnNormalizer(cnts.INGREDIENTS_MAPPING_PATH)
indexer = Indexer(
    ru_data_path=cnts.RU_DATA_PATH,
    en_data_path=cnts.EN_DATA_PATH
)
query_builder = QueryBuilder()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template(cnts.HOMEPAGE_HTML)

@app.route("/", methods=["POST"])
def my_form_post():
    text = request.form["user_text"]
    logging.info(f"Raw text: {text}")

    if re.search("[А-яё]+", text):
        normalizer = ru_normalizer
        current_index = cnts.RU_INDEX_NAME
    else:
        normalizer = en_normalizer
        current_index = cnts.EN_INDEX_NAME

    normed_text = normalizer.normalize(text)
    elastic_query = query_builder.build_elastic_query(normed_text)
    search_result = requests.get(
        f"http://{cnts.HOST}:{cnts.PORT}/{current_index}/_search",
        json=elastic_query)

    logging.info(f"Normalized text: {normed_text}")
    hits = search_result.json()[cnts.HITS][cnts.HITS]

    return render_template(cnts.INDEX_HTML,
                           query=text,
                           normed_query=set(normed_text.split()),
                           hits=hits,
                           zip=zip,
                           set=set)

if __name__ == "__main__":
    if not os.path.isdir("logs"):
        os.mkdir("logs")

    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                        level=logging.INFO,
                        handlers=[
                            FileHandler(
                                f"logs/{datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}.log"
                            ),
                            StreamHandler()
                        ])
    logger = logging.getLogger("app")

    response_ru = requests.get(f"http://{cnts.HOST}:{cnts.PORT}/{cnts.RU_INDEX_NAME}/_stats")
    if response_ru.status_code != cnts.SUCCESS_STATUS_CODE:
        logger.info("Empty RU index! Indexer started.")
        indexer.index_data(index_ru=True)
    else:
        logger.info("RU index already exists.")

    response_en = requests.get(f"http://{cnts.HOST}:{cnts.PORT}/{cnts.EN_INDEX_NAME}/_stats")
    if response_en.status_code != cnts.SUCCESS_STATUS_CODE:
        logger.info("Empty EN index! Indexer started.")
        indexer.index_data(index_en=True)
    else:
        logger.info("EN index already exists.")

    app.run(debug=False)

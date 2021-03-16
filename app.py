from flask import Flask, render_template, request
import requests
import re
from utils import constants as cnts
from utils.normalization import RuNormalizer, EnNormalizer
from utils.query_builder import QueryBuilder

import logging
import datetime

# export FLASK_APP=app
# export FLASK_ENV=development

ru_normalizer = RuNormalizer(cnts.QUERY_EXPANSION_PATH)
en_normalizer = EnNormalizer(cnts.QUERY_EXPANSION_PATH)
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
        index = cnts.RU_INDEX_NAME
    else:
        normalizer = en_normalizer
        index = cnts.EN_INDEX_NAME

    normed_text = normalizer.normalize(text)
    elastic_query = query_builder.build_elastic_query(normed_text)
    search_result = requests.get(
        f"http://{cnts.HOST}:{cnts.PORT}/{index}/_search",
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
    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                        level=logging.INFO,
                        handlers=[
                            logging.FileHandler(f"logs/{datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}.log"),
                            logging.StreamHandler()
                        ])
    app.run(debug=True)
from flask import Flask, render_template, request
import requests
import re
from utils.constants import (EN_INDEX_NAME, RU_INDEX_NAME,
                            HOMEPAGE_HTML, INDEX_HTML,
                            HOST, PORT, HITS, QUERY_EXPANSION_PATH)
from utils.normalization import RuNormalizer, EnNormalizer
from utils.query_builder import QueryBuilder

# export FLASK_APP=app
# export FLASK_ENV=development

ru_normalizer = RuNormalizer(QUERY_EXPANSION_PATH)
en_normalizer = EnNormalizer(QUERY_EXPANSION_PATH)
query_builder = QueryBuilder()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template(HOMEPAGE_HTML)

@app.route("/", methods=["POST"])
def my_form_post():
    text = request.form["user_text"]

    if re.search("[А-яё]+", text):
        normed_text = ru_normalizer.normalize(text)
        elastic_query = query_builder.build_elastic_query(normed_text)
        search_result = requests.get(f"http://{HOST}:{PORT}/{RU_INDEX_NAME}/_search", json=elastic_query)
    else:
        normed_text = en_normalizer.normalize(text)
        elastic_query = query_builder.build_elastic_query(normed_text)
        search_result = requests.get(f"http://{HOST}:{PORT}/{EN_INDEX_NAME}/_search", json=elastic_query)

    hits = search_result.json()[HITS][HITS]

    return render_template(INDEX_HTML,
                           query=text,
                           normed_query=set(normed_text.split()),
                           hits=hits,
                           zip=zip,
                           set=set)

if __name__ == "__main__":
    app.run(debug=True)
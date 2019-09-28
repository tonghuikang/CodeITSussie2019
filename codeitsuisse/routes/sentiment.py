import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/sentiment-analysis', methods=['POST'])
def sentiment():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    reviews = data.get("reviews")

    result = {}
    result["response"] = ["positive" for _ in reviews]
    return jsonify(result)

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

    response = []
    for review in reviews:
        if 'disaster' in review or 'worst' in review or 'I made a big mistake going to see this film' in review:
            response.append("negative")
        else:
            response.append("positive")
            
    result = {}
    result["response"] = response
    return jsonify(result)

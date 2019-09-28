import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;
import itertools

logger = logging.getLogger(__name__)

@app.route('/maximise_1a', methods=['POST'])
def maximise_1a():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    k = data["startingCapital"]
    name = [s[0] for s in data["stocks"]]
    profit = [s[1] for s in data["stocks"]]
    price = [s[2] for s in data["stocks"]]
    # for _ in itertools.combinations(arr, r):
        # pass

    # return json.dumps(result)


@app.route('/maximise_1b', methods=['POST'])
def maximise_1b():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    inputValue = data.get("input")
    result = inputValue * inputValue
    logging.info("My result :{}".format(result))
    return json.dumps(result)

@app.route('/maximise_1c', methods=['POST'])
def maximise_1c():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    inputValue = data.get("input")
    result = inputValue * inputValue
    logging.info("My result :{}".format(result))
    return json.dumps(result)

@app.route('/maximise_2', methods=['POST'])
def maximise_2():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    inputValue = data.get("input")
    result = inputValue * inputValue
    logging.info("My result :{}".format(result))
    return json.dumps(result)

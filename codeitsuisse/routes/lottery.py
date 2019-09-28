import logging
import json
import random


from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/lottery', methods=['GET'])
def lottery():
    data = request.get_json()
    print(data)
    #logging.info("data sent for evaluation {}".format(data))

    guess_array = []
    for i in range(10):
        elem = random.randint(1, 100)
        guess_array.append(elem)
    print(guess_array)

    #inputValue = data.get("input")
    #result = inputValue * inputValue
    #logging.info("My result :{}".format(result))

    return json.dumps(guess_array)

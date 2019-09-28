import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/composition', methods=['POST'])
# def composition():
#     data = request.get_json()
#     logging.info("data sent for evaluation {}".format(data))
#     inputValue = data.get("input")
#     result = inputValue * inputValue
#     logging.info("My result :{}".format(result))
#     return json.dumps(result)

def composition():
    data = request.get_json()
    for element in data[patterns]:




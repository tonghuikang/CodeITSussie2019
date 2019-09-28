import logging
import json


from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/lottery', methods=['POST'])
def lottery():
    data = request.get_json()
    print(data)
    #logging.info("data sent for evaluation {}".format(data))

    guess_array = [10,9,8,7,6,5,4,3,2,1]
    # guess_array = np.random.randint(1, 101, 10)
    print(guess_array)

    #inputValue = data.get("input")
    #result = inputValue * inputValue
    #logging.info("My result :{}".format(result))
    return json.dumps(guess_array)

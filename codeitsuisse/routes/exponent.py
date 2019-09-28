import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;
import math

logger = logging.getLogger(__name__)

@app.route('/exponent', methods=['POST'])
def exponent():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    n = data["n"]
    p = data["p"]
    print(n,p)
    last_digit = n**(p%10)%10
    exponent = p * math.log10(n)
    first_digit = int(10 ** (exponent%1) // 1)
    num_digits = int((exponent // 1) + 1)

    res = {"result" : [first_digit, num_digits, last_digit]}
    print(res)

    return json.dumps(res)

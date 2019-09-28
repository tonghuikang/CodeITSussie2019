import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

import itertools

logger = logging.getLogger(__name__)

@app.route('/defuse', methods=['POST'])
def defuse():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    print(data)

    result = []
    for question in data:
        result.append(solve(question))
        # break  # REMOVE
    return json.dumps(result)

def solve(question):
    if question["n"] < 3:
        return 0
    k = question["k"]
    arr = question["password"]


    NUM = 998244353
    res = 0
    t = arr
    for comb in [t[i:i+j] for i in range(len(t)-3) for j in range(3,len(t)+1,2)]:
        r = len(comb)
        half = len(comb) // 2
        print(r,half)

        for h in range(half):
            if arr[h] != -1 and arr[-1-h] != -1:
                if arr[h] != arr[-1-h]:
                    continue
        count = 0
        for h in range(half):
            if arr[h] != -1 or arr[-1-h] != -1:
                pass
            else:
                count += 1
            if arr[half] == -1:
                count += 1
        print(k**count)
        res += (k**count) % NUM
    return res


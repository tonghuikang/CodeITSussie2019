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
    for r in range(3,len(arr)+1,2):
        half = int((r-1)/2)
        print(r,half)
        combi = itertools.combinations(arr, r)
        for comb in list(set(combi)):
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
            res += (k**count) % NUM
    return res




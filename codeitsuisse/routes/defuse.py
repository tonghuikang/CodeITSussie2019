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

    result = []
    for question in data:
        result.append(solve(question))

    return json.dumps(result)

def solve(question):
    n = question["n"]
    k = question["k"]
    if n < 3:
        return 0
    arr = question["password"]

    

    NUM = 998244353
    res = 0
    for r in range(3,len(arr)+1,2):
        half = int((r-1)/2)
        print(r,half)
        for comb in itertools.combinations(arr, r):
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




    
 
# data = [
#     {
#         "n": 2,
#         "k": 3,
#         "password": [
#             -1,
#             -1
#         ]
#     },
#     {
#         "n": 5,
#         "k": 2,
#         "password": [
#             1,
#             -1,
#             -1,
#             1,
#             2
#         ]
#     },
#     {
#         "n": 5,
#         "k": 3,
#         "password": [
#             1,
#             -1,
#             -1,
#             1,
#             2
#         ]
#     },
#     {
#         "n": 4,
#         "k": 200000,
#         "password": [
#             -1,
#             -1,
#             12345,
#             -1
#         ]
#     },
#     {
#         "n": 10,
#         "k": 5,
#         "password": [
#             4,
#             -1,
#             -1,
#             1,
#             -1,
#             -1,
#             -1,
#             2,
#             -1,
#             -1
#         ]
#     },
#     {
#         "n": 10,
#         "k": 8,
#         "password": [
#             4,
#             8,
#             -1,
#             -1,
#             -1,
#             2,
#             -1,
#             4,
#             -1,
#             -1
#         ]
#     }
# ]
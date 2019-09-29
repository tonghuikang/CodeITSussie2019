import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;
import time

logger = logging.getLogger(__name__)

@app.route('/bankbranch', methods=['POST'])
def branch():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    branch = data["branch_officers_timings"]
    free = [0 for _ in range(len(branch))]
    customer = data["N"]
    print(customer)

    if customer > 1000:
        time.sleep(1)

    for i in range(customer):
        cst = free.index(min(free))
        free[cst] = free[cst] + branch[cst]
        # print(free)

    
    answer = cst
    print(answer)
    return jsonify({"answer" : answer+1})


import re

@app.route('/encryption', methods=['POST'])
def message():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    print(data)
    # branch = data["branch_officers_timings"]

    res = []
    for entry in data:
        n, text = entry["n"], entry["text"]
        text = text.upper().replace(" ", "").replace("_","")
        text = re.sub(r'\W+', '', text)
        print(text, "text")
        if n >= len(text):
            ans = text
        else:
            ans = ["" for _ in range(n*((len(text) // n) + 1))]
            txt = list(text) + [""]*(len(ans) - len(text))
            print(txt)
            for i in range(n):
                k = len(txt)//n
                # print(k)
                # print(len(ans[i::n]))
                # print(len(txt[i*k:(i+1)*k]))
                # print(txt[i*k:(i+1)*k])
                # print(i*k)
                # print((i+1)*k)
                # print()
                ans[i::n] = txt[i*k:(i+1)*k]
                print(ans)
        res.append("".join(ans)[:len(text)])

    return jsonify(res)
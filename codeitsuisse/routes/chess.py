import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/bankbranch', methods=['POST'])
def branch():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    branch = data["branch_officers_timings"]
    free = [0 for _ in range(len(branch))]
    customer = data["N"]
    print(customer)
    
    for i in range(customer):
        cst = free.index(min(free))
        free[cst] = free[cst] + branch[cst]
        # print(free)
        if i > 100000:
            break
    
    answer = cst
    print(answer)
    return jsonify({"answer" : answer})


@app.route('/secretmessage', methods=['POST'])
def message():
    # data = request.get_json()
    # logging.info("data sent for evaluation {}".format(data))
    # branch = data["branch_officers_timings"]
    # free = [0 for _ in range(len(branch))]
    # customer = data["N"]
    # print(customer)

    # for i in range(customer):
    #     cst = free.index(min(free))
    #     free[cst] = free[cst] + branch[cst]
    #     print(free)
    #     if i > 100000:
    #         break
    
    # answer = cst
    # print(answer)
    # return jsonify({"answer" : answer})
    pass
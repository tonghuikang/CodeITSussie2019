import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;
import itertools

from itertools import product
from mip.model import Model, xsum, minimize
from mip.constants import MINIMIZE, BINARY, INTEGER, MAXIMIZE

logger = logging.getLogger(__name__)

@app.route('/maximise_1a', methods=['POST'])
def maximise_1a():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    print(data)
    name = [s[0] for s in data["stocks"]]
    obj = [s[1] for s in data["stocks"]]
    prz = [s[2] for s in data["stocks"]]
    rsk = [0 for s in data["stocks"]]
    capital = data["startingCapital"]
    risk = 1

    profit, res, tickers = opti(name, obj, prz, rsk, capital, risk, BINARY)

    answer = {}
    answer["profit"] = profit
    answer["portfolio"] = tickers

    return jsonify(answer)


@app.route('/maximise_1b', methods=['POST'])
def maximise_1b():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    print(data)
    name = [s[0] for s in data["stocks"]]
    obj = [s[1] for s in data["stocks"]]
    prz = [s[2] for s in data["stocks"]]
    rsk = [0 for s in data["stocks"]]
    capital = data["startingCapital"] - sum(prz)
    if capital < 0:
        return jsonify({"profit" : 0, "portfolio" : []})
    risk = 1

    profit, res, tickers = opti(name, obj, prz, rsk, capital, risk, INTEGER)

    answer = {}
    answer["profit"] = profit + sum(obj)
    answer["portfolio"] = tickers + [name_ for name_ in name]

    return jsonify(answer)

@app.route('/maximise_1c', methods=['POST'])
def maximise_1c():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    print(data)
    name = [s[0] for s in data["stocks"]]
    obj = [s[1] for s in data["stocks"]]
    prz = [s[2] for s in data["stocks"]]
    rsk = [0 for s in data["stocks"]]
    capital = data["startingCapital"]
    risk = 1

    profit, res, tickers = opti(name, obj, prz, rsk, capital, risk, INTEGER)

    answer = {}
    answer["profit"] = profit
    answer["portfolio"] = tickers

    return jsonify(answer)

@app.route('/maximise_2', methods=['POST'])
def maximise_2():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    print(data)
    name = [s[0] for s in data["stocks"]]
    obj = [s[1] for s in data["stocks"]]
    prz = [s[2] for s in data["stocks"]]
    rsk = [s[3] for s in data["stocks"]]
    capital = data["startingCapital"]
    risk = data["risk"]

    profit, res, tickers = opti(name, obj, prz, rsk, capital, risk, BINARY)

    answer = {}
    answer["profit"] = profit
    answer["portfolio"] = tickers

    return jsonify(answer)



def opti(name, obj, prz, rsk, capital, risk, vartype):

    m = Model()
    m = Model(sense=MAXIMIZE, solver_name="cbc")

    # name = ["a","b","c","d"]
    # obj = [30,25,15,20]
    # prz = [400,300,100,100]
    # rsk = [5,2,4,6]
    # capital = 400
    # risk = 10

    # y = [m.add_var(var_type=INTEGER) for i in range(4)]  # 1C
    y = [m.add_var(var_type=vartype, name=name[i]) for i in range(len(name))]  # 1A

    m += xsum(prz[i]*y[i] for i in range(len(y))) <= capital
    m += xsum(rsk[i]*y[i] for i in range(len(y))) <= risk
    m.objective = xsum(obj[i]*y[i] for i in range(len(y)))

    m.max_gap = 0.05
    status = m.optimize(max_seconds=300)
    print(status)
    print(m.objective_value)
    res = [(v.name, int(v.x)) for v in m.vars]
    print(res)

    tickers = []
    for entry in res:
        for _ in range(entry[1]):
            tickers.append(entry[0])


    return int(m.objective_value), res, tickers
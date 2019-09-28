import sys
import os
import tempfile
from flask import escape
from flask import jsonify
from collections import Counter
import requests
import json
from flask import Response
import logging

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def execution(request):
    def isValid(i,j):
        if i >= 0 and i < y_size and j >= 0 and j < x_size:
            if grid[i][j] == 'O' and visited[i][j] == 0:
                return True
        return False
    request = request.get_json(silent=True)
    grid = request['grid']
    fuel = request['fuel']
    y_size = len(grid)
    x_size = len(grid[0])
    stack = []
    #(i coordinate, j coordinate, cost)
    stack.append((0,0,1))

    #track visited route
    visited = [[0 for _ in range(x_size)] for _ in range(y_size)]

    directions = [(1,0),(0,1),(-1,0),(0,-1)]
    endpoints = []
    while len(stack) > 0:
        node = stack.pop(0)
        i = node[0]
        j = node[1]
        cost = node[2]

        #mark as visited
        visited[i][j] = 1
        nodes_added = 0
        for i_plus , j_plus in directions:
            if isValid(i+i_plus, j+j_plus):
                stack.append((i+i_plus, j+j_plus, cost+1))
                nodes_added += 1
        if nodes_added == 0:
            endpoints.append(node)

    #greedy
    #knapsack problem in DP (kill me now)
    num_endpoints = len(endpoints)
    knapsack = set()
    def rabbithole(n,fuel,bag):
        value = endpoints[n-1][2]
        if n == 0 or fuel == 0:
            result = (0,bag)
        elif value > fuel:
            result = rabbithole(n-1, fuel,bag)
        else:
            temp1 = bag + [n]
            # result = max(value+rabbithole(n-1,fuel-value,temp1),rabbithole(n-1,fuel,bag))
            number1, tempbag1 = rabbithole(n-1,fuel-value,temp1)
            number1 += value
            number2, tempbag2 = rabbithole(n-1,fuel,bag)
            if number1 > number2:
                result = (number1, tempbag1)
            else:
                result = (number2, tempbag2)
        return result
    hits = []
    maxnumber, knapsack = rabbithole(num_endpoints,fuel, [])
    for item in knapsack:
        gun = dict()
        endpoint = endpoints[item-1]
        gun['cell'] = {'x':endpoint[1]+1,'y':endpoint[0]+1}
        gun['guns'] = endpoint[2]
        hits.append(gun)

    result = {}
    result['hits'] = hits
    return jsonify(result)

@app.route('/gun-control', methods=['POST'])
def gun_control():
    return execution(request)

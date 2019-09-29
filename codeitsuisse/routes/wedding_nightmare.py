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

def nightmare(request):
    test_cases = request.get_json(silent=True)
    request_args = request.args
    response = []
    for test_case in test_cases:
        test_case_num = test_case['test_case']
        guests = test_case['guests']
        tables = test_case['tables']
        friends = test_case['friends']
        enemies = (test_case['enemies'])
        families = test_case['families']
        print('test case:', test_case_num)

        disjoint_sets = [set()]
        allocated_ppl = set()
        if len(enemies) > 0:
            person1, person2 = enemies.pop()
            disjoint_sets[0] = set([person1])
            disjoint_sets.append(set([person2]))
            allocated_ppl.add(person1)
            allocated_ppl.add(person2)

        print(disjoint_sets)
        print(allocated_ppl)

        for person1, person2 in enemies:
            p1_truth = True
            p2_truth = True
            if person1 in allocated_ppl:
                p1_truth = False
            if person2 in allocated_ppl:
                p2_truth = False
            for table in disjoint_sets:
                if person1 not in table and p1_truth:
                    table.add(person1)
                    allocated_ppl.add(person1)
                    p1_truth = False
                if person2 not in table and p2_truth:
                    table.add(person2)
                    allocated_ppl.add(person2)
                    p2_truth = False

        for friend1, friend2 in friends:
            add = False
            for table in disjoint_sets:
                if friend1 in table:
                    table.add(friend2)
                    allocated_ppl.add(friend2)
                    add = True
                    break
                if friend2 in table:
                    table.add(friend1)
                    allocated_ppl.add(friend1)
                    add = True
                    break
            if add is False:
                disjoint_sets[0].add(friend1)
                disjoint_sets[0].add(friend2)
                allocated_ppl.add(friend1)
                allocated_ppl.add(friend2)

        for friend1, friend2 in families:
            add = False
            for table in disjoint_sets:
                if friend1 in table:
                    table.add(friend2)
                    allocated_ppl.add(friend2)
                    add = True
                    break
                if friend2 in table:
                    table.add(friend1)
                    allocated_ppl.add(friend1)
                    add = True
                    break
            if add is False:
                disjoint_sets[0].add(friend1)
                disjoint_sets[0].add(friend2)
                allocated_ppl.add(friend1)
                allocated_ppl.add(friend2)

        guestlist = set([i for i in range(1,guests+1)])
        remaining = guestlist.difference(allocated_ppl)

        disjoint_sets[0] = disjoint_sets[0].union(remaining)

        allocation = []
        for num, table in enumerate(disjoint_sets):
            for person in table:
                allocation.append([person,num+1])
        res = {"test_case": test_case_num, 'satisfiable': True, 'allocation': allocation}
        response.append(res)

    # return json.dumps(response)
    return jsonify(response)


@app.route('/wedding-nightmare', methods=['POST'])
def wedding_nightmare():
    return nightmare(request)

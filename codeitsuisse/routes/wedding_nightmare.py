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
    response = []
    print(test_cases)
    for test_case in test_cases:
        test_case_num = test_case['test_case']
        guests = test_case['guests']
        tables = test_case['tables']
        friends = test_case['friends']
        enemies = (test_case['enemies'])
        families = test_case['families']

        #create an enemies dictionary for )
        enemies_dict = {}
        for person1, person2 in enemies:
            if person1 not in enemies_dict.keys():
                enemies_dict[person1] = set([person2])
            else:
                enemies_dict[person1].add(person2)
            if person2 not in enemies_dict.keys():
                enemies_dict[person2] = set([person1])
            else:
                enemies_dict[person2].add(person1)

        #sort the enemies into their tables (minimum tables needed)
        disjoint_sets = [set()]
        added_person = set()
        if len(enemies) > 0:
            person1, person2 = enemies.pop()
            disjoint_sets = [set([person1]), set([person2])]
            added_person = set([person1,person2])
        for person1, person2 in enemies:
            person1_t = False
            person2_t = False
            if person1 in added_person:
                person1_t = True
            if person2 in added_person:
                person2_t = True
            for table in disjoint_sets:
                if person1_t is False and len(table.intersection(enemies_dict[person1])) == 0:
                    table.add(person1)
                    person1 = True
                    added_person.add(person1)
                    continue
                if person2_t is False and len(table.intersection(enemies_dict[person2])) == 0:
                    table.add(person2)
                    person2_t = True
                    added_person.add(person2)
                    continue
            if person1_t is False:
                disjoint_sets.append(set([person1]))
            if person2_t is False:
                disjoint_sets.append(set([person2]))

        if len(disjoint_sets) > tables:
            res = {'test_case':test_case_num, 'satisfiable':False, 'allocation':[]}
            response.append(res)
            continue

        #add friends and families
        for friend1, friend2 in friends:
            add = False
            for table in disjoint_sets:
                if friend1 in table:
                    table.add(friend2)
                    added_person.add(friend2)
                    add = True
                    break
                if friend2 in table:
                    table.add(friend1)
                    added_person.add(friend1)
                    add = True
                    break
            if add is False:
                disjoint_sets[0].add(friend1)
                disjoint_sets[0].add(friend2)
                added_person.add(friend1)
                added_person.add(friend2)

        guestlist = set([i for i in range(1,guests+1)])
        remaining = guestlist.difference(added_person)

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

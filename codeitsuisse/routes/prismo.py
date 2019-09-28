import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def addMoves(move):
    res = None
    if move == (1,0):
        res = "F"
    elif move == (0,1):
        res = "R"
    elif move == (-1,0):
        res = "B"
    elif move == (0,-1):
        res = "L"
    return res

def prismo(request):
    request = request.get_json(silent=True)
    initial = request['initial']
    goal = request['goal']
    #1D answer
    moves = []
    if type(initial[0]) == int:
        pos_index = initial.index(0)
        goal_index = goal.index(0)
        if goal_index > pos_index:
            moves = ["R"] * (goal_index - pos_index)
        elif goal_index < pos_index:
            moves = ["L"] * (pos_index - goal_index)

    if type(initial[0]) == list:
        pos_index = None
        goal_index = None
        x_length = len(initial)
        y_length = len(initial[0])
        for i, row in enumerate(initial):
            if 0 in row:
                pos_index = (i, row.index(0))
                break
        for i, row in enumerate(goal):
            if 0 in row:
                goal_index = (i, row.index(0))

        directions = [(1,0),(0,1),(-1,0),(0,-1)]
        while pos_index != goal_index:
            opp_square = goal[pos_index[0]][pos_index[1]]
            for index, direction in enumerate(directions):
                x_plus, y_plus = direction
                x, y = x_plus + pos_index[0], y_plus + pos_index[1]
                if x < x_length and x >= 0 and y < y_length and y >= 0:
                    if initial[x][y] == opp_square:
                        initial[x][y] = 0
                        pos_index = (x,y)
                        moves.append(addMoves(direction))
                        break
    return jsonify({'moves':moves})

@app.route('/prismo', methods=['POST'])
def evaluate():
    return prismo(request)

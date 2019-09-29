import logging
import json
import copy

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
            for j, square in enumerate(row):
                if square == 0:
                    pos_index = (i,j)
                    break
        directions = [(1,0),(0,1),(-1,0),(0,-1)]
        last_visited = None
        stack = []
        stack.append((pos_index,last_visited, initial, []))
        while len(stack) > 0 and initial != goal:
            pos_index, last_visited, initial, moves = stack.pop(0)
            goal_square = goal[pos_index[0]][pos_index[1]]
            continues = 0
            for x_plus, y_plus in directions:
                x, y = x_plus + pos_index[0], y_plus + pos_index[1]
                if (x,y) == last_visited:
                    continue
                if x < x_length and x >= 0 and y < y_length and y >= 0:
                    if initial[x][y] == goal_square:
                        last_visited = (pos_index[0],pos_index[1])
                        initial[pos_index[0]][pos_index[1]], initial[x][y] =  initial[x][y], 0
                        pos_index = (x,y)
                        moves.append(addMoves((x_plus,y_plus)))
                        stack.append(((x,y),last_visited),initial,moves)
                        print('up:', initial)
                        continues = 1
                        break
            if continues == 0:
                initial_array = []
                goal_array = []
                for x_plus, y_plus in directions:
                    x, y = x_plus + pos_index[0], y_plus + pos_index[1]
                    if x < x_length and x >= 0 and y < y_length and y >= 0:
                        if initial[x][y] != goal[x][y]:
                            initial_array.append((initial[x][y],(x,y)))
                            goal_array.append((goal[x][y]))
                for value, location in initial_array:
                    if value in goal_array:
                        move_direction = (location[0] - pos_index[0], location[1] - pos_index[1])
                        initial[pos_index[0]][pos_index[1]], initial[location[0]][location[1]] = initial[location[0]][location[1]], initial[pos_index[0]][pos_index[1]]
                        stack.append((location, pos_index, initial))
                        moves.append(addMoves((move_direction)))
                        print('down:',initial)

    print(initial)

    return jsonify({'moves':moves})

# {
#   "initial": [[ 1, 2, 3, 4],
#               [ 5, 6, 7, 8],
#               [ 9,10,12, 0],
#               [13,14,11,15]],
#   "goal": [[ 1, 2, 3, 4],
#            [ 5, 6, 7, 0],
#            [ 9,10,11,8],
#            [13,14,15, 12]]
# }

@app.route('/prismo', methods=['POST'])
def evaluate():
    return prismo(request)

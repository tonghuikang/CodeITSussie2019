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
            for j, square in enumerate(row):
                if square == 0:
                    pos_index = (i,j)
                    break
        for i, row in enumerate(goal):
            for j, square in enumerate(row):
                if square == 0:
                    goal_index = (i,j)
                    break
        directions = [(1,0),(0,1),(-1,0),(0,-1)]
        last_visited = None
        stack = []
        stack.append((pos_index,last_visited))

        while len(stack) > 0 and initial != goal:
            pos_index, last_visited = stack.pop(0)
            goal_square = goal[pos_index[0]][pos_index[1]]
            continues = 0
            for x_plus, y_plus in directions:
                x, y = x_plus + pos_index[0], y_plus + pos_index[1]
                if (x,y) == last_visited:
                    continue
                if x < x_length and x >= 0 and y < y_length and y >= 0:
                    print('goal:', goal[pos_index[0]][pos_index[1]])
                    print(initial[x][y], goal_square, 'helooooooo', (x,y), pos_index)
                    if initial[x][y] == goal_square:
                        print('helooooooo')
                        last_visited = (pos_index[0],pos_index[1])
                        initial[pos_index[0]][pos_index[1]], initial[x][y] =  initial[x][y], 0
                        pos_index = (x,y)
                        stack.append(((x,y),last_visited))
                        moves.append(addMoves((x_plus,y_plus)))
                        print('up:', initial)
                        continues = 1
                        break
            if continues == 0:
                initial_array = []
                goal_array = []
                for x_plus, y_plus in directions:
                    x, y = x_plus + pos_index[0], y_plus + pos_index[1]
                    if initial[x][y] != goal[x][y]:
                        initial_array.append((initial[x][y],(x,y)))
                        goal_array.append((goal[x][y]))
                # for x_plus, y_plus in directions:
                #     x, y = x_plus + pos_index[0], y_plus + pos_index[1]
                #     if value
                # print('initial_array', initial_array)
                # print('GOAL ARRAY', goal_array)
                for value, location in initial_array:
                    if value in goal_array:
                        print('hihihi',pos_index,last_visited, location)
                        move_direction = (location[0] - pos_index[0], location[1] - pos_index[1])
                        initial[pos_index[0]][pos_index[1]], initial[location[0]][location[1]] = initial[location[0]][location[1]], initial[pos_index[0]][pos_index[1]]
                        # last_visited, pos_index = pos_index, location
                        stack.append((location, pos_index))
                        moves.append(addMoves((move_direction)))
                        print('down:',initial)

        # print(initial)

    return jsonify({'moves':moves})
#

@app.route('/prismo', methods=['POST'])
def evaluate():
    return prismo(request)

import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;
import time

logger = logging.getLogger(__name__)


def chessgame(request):
    chessboard = request.get_json(silent=True)
    request_args = request.args
    q_pos = None
    for i, row in enumerate(chessboard):
        for j, square in enumerate(chessboard):
            if chessboard[i][j] == 'K':
                q_pos = (i,j)

    length = len(chessboard)
    attack_count = 0
    directions = [(length,1),(-1,-1)]
    #check horizontal row
    for end, direction in directions:
        for j in range(q_pos[1],end,direction):
            if chessboard[q_pos[0]][j] == '':
                attack_count += 1
            elif chessboard[q_pos[0]][j] == 'X':
                break
    #check vertical
    for end, direction in directions:
        for i in range(q_pos[0],end,direction):
            if chessboard[i][q_pos[1]] == '':
                attack_count += 1
            elif chessboard[i][q_pos[1]] == 'X':
                break
    #check diagonals
    dir = [(1,1),(-1,-1),(-1,1),(1,-1)]
    for i_plus, j_plus in dir:
        i, j = q_pos[0], q_pos[1]
        while i < length and i >= 0 and j < length and j >= 0:
            if chessboard[i][j] == '':
                attack_count += 1
            elif chessboard[i][j] == 'X':
                break
            i, j = i + i_plus , j + j_plus
    print('attack count:', attack_count)

    return str(attack_count)

@app.route('/chessgame', methods=['POST'])
def chess():
    return chessgame(request)

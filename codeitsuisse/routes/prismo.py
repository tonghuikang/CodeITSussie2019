import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

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

    return jsonify({'moves':moves})

@app.route('/prismo', methods=['POST'])
def evaluate():
    return prismo(request)

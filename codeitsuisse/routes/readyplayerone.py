import logging
import json

from flask import request, jsonify, Response;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/readyplayerone', methods=['POST'])
def readyplayerone():
    data = request.get_json()
    # print(data)
    # logging.info("data sent for evaluation {}".format(data))
    N_integer = data["maxChoosableInteger"]
    T_totaldesired = data["desiredTotal"]
    Jar1_list = range(1, 11, 1)
    calculated = strategy(N_integer, T_totaldesired)
    output = {"res" : calculated}
    return Response(json.dumps(output), mimetype='application/json')



def strategy(N_integer, T_totaldesired):

    if N_integer >= T_totaldesired:
        return 1                # Player 1 wins on the first turn

    if T_totaldesired == (N_integer*(N_integer + 1) / 2):              #Case of requiring the perfect AP Sum
        if N_integer % 2 == 0:
            return -1                   # Player 2 will always win (Even number of tries)
        return N_integer                # Player 1 will always win (Odd number of tries)

    return -1 #idk man this means I'm random whacking
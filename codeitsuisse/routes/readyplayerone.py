import logging
import json

from flask import request, jsonify, Response;

from codeitsuisse import app;

logger = logging.getLogger(__name__)
#Impartial game

@app.route('/readyplayerone', methods=['POST'])
def readyplayerone():
    data = request.get_json()
    # print(data)
    # logging.info("data sent for evaluation {}".format(data))
    N_integer = int(data["maxChoosableInteger"])
    T_totaldesired = int(data["desiredTotal"])
    Jar_pre1 = range(1, N_integer+1)
    Jar_1 = list(Jar_pre1)
    Jar_2 = []
    calculated = strategy(N_integer, T_totaldesired, Jar_1, Jar_2)
    output = {"res" : calculated}
    return Response(json.dumps(output), mimetype='application/json')


def strategy(N_integer, T_totaldesired , Jar_1 , Jar_2):

    if N_integer >= T_totaldesired:
        return 1                # Player 1 wins on the first turn

    if T_totaldesired == (N_integer*(N_integer + 1) / 2):        # Case of requiring the perfect AP Sum
        if N_integer % 2 == 0:
            return -1                   # Player 2 will always win (Even number of tries)
        return N_integer                # Player 1 will always win (Odd number of tries)

    if T_totaldesired > (N_integer*(N_integer + 1) / 2):        # Impossible case of having more than possible
        return -1

    while (len(Jar_2) < N_integer and T_totaldesired - sum(Jar_2) > max(Jar_1)):    #Fixing up the empty max arg
        ideal_number = T_totaldesired - sum(Jar_2) - min(Jar_1) - max(Jar_1)
        if ideal_number in Jar_1:
            Jar_1.remove(ideal_number)
            Jar_2.append(ideal_number)
        else:
            number = min(Jar_1)
            Jar_1.remove(number)
            Jar_2.append(number)

    turns = len(Jar_2)+1
    if turns % 2  == 0:
        return -1
    else:
        return turns
import logging
import json

from flask import request, jsonify, Response;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

"""
Main function that will be called by the request
"""

@app.route('/composition', methods=['POST'])
def composition():
    data = request.get_json()
    print(data)
    logging.info("data sent for evaluation {}".format(data))

    banned_list = form_banned(data['patterns'])
    calculated = min_delete(data['composition'], banned_list)
    setId_number = data['setId']
    output = {  "testId" : setId_number, "result" : calculated}
    return Response(json.dumps(output), mimetype='application/json')




"""
Helper function to calculate the minimum number of deletes required.
Input: String to be analysed; banned_list
Output: Int reflecting the number of deletes required
"""
def min_delete(input_str, banned_list):
    str_length = len(input_str)
    print(input_str)
    if str_length == 0 or str_length == 1: #The banned_list will never contain a str with only 0/1 char
        print(0)
        return 0

    # if str_length == 2: #The banned_list will never contain a str with only 1 char
    #    if input_str in banned_list:

    if input_str[-2:] in banned_list:
        #print(input_str + 'hihi') just testing this
        shortened1 = input_str[:-1]
        shortened2 = input_str[:-2] + input_str[-1]
        s1_value = min_delete(shortened1, banned_list) + 1
        s2_value = min_delete(shortened2, banned_list) + 1
        print(min(s1_value, s2_value))
        return min(s1_value, s2_value)

    #Case where the last two characters are not in the banned list
    shortened3 = input_str[:-2]
    print(min_delete(shortened3 , banned_list))
    return min_delete(shortened3 , banned_list)



"""
Helper function to form the banned array.
"""
def form_banned(initial_patterns):
    banned_patterns = []
    for pattern in initial_patterns:
        rev_str = pattern[::-1]   # reversing the pattern
        banned_patterns.append(rev_str)
    banned_patterns.extend(initial_patterns)
    print(banned_patterns)
    return banned_patterns


# def composition():
#     data = request.get_json()
#     logging.info("data sent for evaluation {}".format(data))
#     inputValue = data.get("input")
#     result = inputValue * inputValue
#     logging.info("My result :{}".format(result))
#     return json.dumps(result)

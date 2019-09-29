import logging
import json
import sys

from flask import request, jsonify, Response;

from codeitsuisse import app;

logger = logging.getLogger(__name__)
sys.setrecursionlimit(13000)

"""
Main function that will be called by the request
"""

@app.route('/composition', methods=['POST'])
def composition():
    data = request.get_json()
    # print(data)
    # logging.info("data sent for evaluation {}".format(data))

    banned_list = form_banned(data['patterns'])
    dict_seen = {}                  #using dynamic programming
    calculated = decorated_delete(data['composition'], banned_list, dict_seen, data['compositionLength'])
    setId_number = data['setId']
    output = {"testId" : setId_number, "result" : calculated}
    return Response(json.dumps(output), mimetype='application/json')



"""
Decorator function to implement iteration. 
Builds up dict_seen from the bottom-up to reduce the number of recursive calls required.
"""
def decorated_delete(input_str, banned_list, dict_seen, original_length):
    answer = 0
    for counter in range(original_length):
        answer = min_delete(input_str[0:counter+1], banned_list, dict_seen)     # incrementally lengthening the string
    return answer


"""
Helper function to calculate the minimum number of deletes required.
Input: String to be analysed; banned_list
Output: Int reflecting the number of deletes required
"""
def min_delete(input_str, banned_list, dict_seen):

    if input_str in dict_seen:              #Usage of dynamic programming to speed the code up
        return dict_seen[input_str]

    str_length = len(input_str)

    if str_length == 0 or str_length == 1: #The banned_list will never contain a str with only 0/1 char
        dict_seen[input_str] = 0
        return 0

    if input_str[-2:] in banned_list:
        shortened1 = input_str[:-1]
        shortened2 = input_str[:-2] + input_str[-1]
        s1_value = min_delete(shortened1, banned_list, dict_seen) + 1
        s2_value = min_delete(shortened2, banned_list, dict_seen) + 1
        min_value = min(s1_value, s2_value)
        dict_seen[input_str] = min_value
        return min_value


    #Case where the last two characters are not in the banned list
    shortened3 = input_str[:-1]         # -1 because the 2nd last char may be illegally paired with the 3rd last!
    s3_value = min_delete(shortened3 , banned_list, dict_seen)
    dict_seen[input_str] = s3_value
    return s3_value



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



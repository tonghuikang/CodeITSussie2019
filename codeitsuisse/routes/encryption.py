import logging
import json

from flask import request, jsonify, Response;

from codeitsuisse import app;

logger = logging.getLogger(__name__)
#Impartial game

@app.route('/encryption', methods=['POST'])
def encryption():
    data = request.get_json()
    # print(data)
    # logging.info("data sent for evaluation {}".format(data))

    final_output = []
    for entry in data:
        int_step, clear_text = entry["n"], entry["text"]
        clean_input = sanitise(clear_text)                   #Pre-processing of string
        output_string = encrypt(int_step, clean_input)
        final_output.append(output_string)

    #return jsonify(final_output)
    return Response(json.dumps(final_output), mimetype='application/json')


"""
Preprocessing the input for encryption
"""
def sanitise(cleartext):
    uppertext = cleartext.upper()
    alpha_string = ""
    for char in uppertext:
        if char.isalnum():
            alpha_string = alpha_string + char
    return alpha_string


"""
Main function for encrypting. 
Takes in a step and a clean input, spits out a ciphertext.
"""
def encrypt(int_step, clean_input):
    if int_step >= len(clean_input):    # Encryption fails due to step size being too large
        return clean_input

    encrypt_length = len(clean_input)
    cipher = ["0"]*encrypt_length    # Dealing with an array first for easy indexing, convert to string later
    for index in range(len(clean_input)):
        mod_index = (index * int_step) % len(clean_input)       # Using modulo to wrap around the ciphertext!
        cipher[mod_index] = clean_input[index]

    cipher_string = "".join(cipher)
    return cipher_string






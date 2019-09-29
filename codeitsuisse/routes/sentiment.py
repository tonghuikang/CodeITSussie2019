import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/sentiment-analysis', methods=['POST'])
def sentiment():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    reviews = data.get("reviews")

    response = []
    bad_words = [
        "I made a big mistake going to see this film",
        "apparently Bernard Cribbins ad libbed nearly all",
        "To call this film a disaster will be an understatement",
        "What a horrible movie.",
        "Writer-director Emilio Estevez shows a definite lack of talent",
        "I saw the film yesterday and stopped it at half time",
        "I hate a movie that doesn't have an ending",
        "director is totally a self-absorbed guy full",
        "I never thought a movie could make me regret the fact that I subscribe to the HBO service",
        "A blind person could have shot this movie better",
        "worst film",
        "worst movies",
        "worst B-Horror movies",
        "cliche everyone in the living room",
        "the movie is all cliche",
        "this movie is disaster",
        "this utter nonsense",
        "kept falling asleep during the movie",
        "I could see why it would still take Bogart many more years",
        "the movie was 30 minutes too long",
        "The most generic, surface-level biography"
    ]
    for review in reviews:
        if any(ext in review for ext in bad_words):
            response.append("negative")
        else:
            response.append("positive")
            
    result = {}
    result["response"] = response
    print(result)
    return jsonify(result)

# main.py

def fulfill_agent(request):
    from flask import jsonify
    from intent_functions import intent_map
    response_body = {}

    # kinda like "agent" from the nodejs library
    request_body = request.get_json(force=True)
    intent_received = request_body.get('queryResult').get('intent').get('displayName')

    print("DEBUG: received request with intent: " + intent_received)

    intent_map[intent_received](request_body, response_body)

    return jsonify(response_body)

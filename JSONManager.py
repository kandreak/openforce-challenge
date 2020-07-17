#python component to manage json data

import json

#get a JSON string, return a Python Dictionary of that JSON
def parse (JSONString):
    return json.loads(JSONString)
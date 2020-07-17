#python module to retrieve the json string from the web

import requests

def getJson(url):
    r = requests.get(url, allow_redirects=True)
    return r.content
# python component to manage json data

import json


# get a JSON string, return a list of Python Dictionaries of that JSON
def parse(JSONString):
    return json.loads(JSONString)


# get a JSON string from the list of Python Dictionaries JSONDict
def serialize(JSONDict):
    return json.dumps(JSONDict)


# filter the list of Python Dictionaries to get a list of Python Dictionaries of Regioni and Totale_Casi
def getTotaleRegionale(JSONDict):
    resultDict = []

    # iterate over provincia
    for x in JSONDict:
        # iterate over results
        for y in resultDict:

            # sum up totale_casi, if I have this regione
            # using denominazione because P.A. Bolzano and Trento have the same codice_regione
            if y["denominazione_regione"] == x["denominazione_regione"]:
                y["totale_casi"] += x["totale_casi"]
                break

        # else, add new regione
        else:
            # resultDict.append(dict({"codice_regione": x["codice_regione"], "denominazione_regione": x["denominazione_regione"], "totale_casi": x["totale_casi"]}))
            resultDict.append(dict(
                {"denominazione_regione": x["denominazione_regione"],
                 "totale_casi": x["totale_casi"]}))

    return resultDict


# filter JSONDict leaving only data about the target date
def filterByDate(JSONDict, date):
    dateString = date.strftime("%Y-%m-%d")
    result = list(filter(lambda i: i["data"].startswith(dateString), JSONDict))
    return result

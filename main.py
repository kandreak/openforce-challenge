import datetime

from flask import Flask, request

import JSONManager
import WebRetriever

app = Flask(__name__)


@app.route("/openforcechallenge")
def openForceChallenge():
    date = ""
    filename = ""

    # example date parameter: ?date=2020-03-15
    dateArg = request.args.get("date", default="", type=str)

    if filename == "":
        if dateArg == "":
            filename = "dpc-covid19-ita-province-latest.json"
        else:
            filename = "dpc-covid19-ita-province.json"

            # input sanitizing
            try:
                date = datetime.datetime.strptime(dateArg, "%Y-%m-%d")
            except ValueError:
                return ("Incorrect date format, should be YYYY-MM-DD!")
                exit(1)

            if date < datetime.datetime(2020, 2, 24):
                return ("Date should be after 2020-02-24!")
                exit(1)

            # searching data for at most yesterday allows to avoid errors if today's update is late!
            yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
            if date > yesterday:
                return ("Date should be at most yesterday! (leave it blank to get the latest update)")
                exit(1)

    # repo with raw: in this way I can access the raw file
    repo = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/"

    # building url:
    url = repo + filename

    JSONString = WebRetriever.getJson(url)

    JSONDict = JSONManager.parse(JSONString)

    if dateArg != "":
        JSONDict = JSONManager.filterByDate(JSONDict, date)

    JSONDictRegione = JSONManager.getTotaleRegionale(JSONDict)

    # sorting by totale_casi and denominazione_regione
    # since i need ascending order for denominazione_regione and descending order for totale casi,
    # I do ascending order for both, but I negate each totale casi! :D
    JSONDictSorted = sorted(JSONDictRegione, key=lambda i: ((i["totale_casi"] * -1), i["denominazione_regione"]))

    for x in JSONDictSorted:
        print(x)

    JSONResult = JSONManager.serialize(JSONDictSorted)

    return JSONResult

import datetime
import sys

import JSONManager
import WebRetriever

date = ""
dateArg = ""
filename = ""

argv = sys.argv
if len(argv) > 1:
    dateArg = argv[1]

if filename == "":
    if dateArg == "":
        filename = "dpc-covid19-ita-province-latest.json"
    else:
        filename = "dpc-covid19-ita-province.json"

        #input sanitizing
        try:
            date = datetime.datetime.strptime(dateArg, '%Y-%m-%d')
        except ValueError:
            print("Incorrect data format, should be YYYY-MM-DD!")
            print("it was: " + date + ", from " + dateArg)
            exit(1)

        if date < datetime.datetime(2020, 2, 24):
            print("Date should be after 2020-02-24!")
            exit(1)

        #searching data for at most yesterday allows to avoid errors if today's update is late!
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        if date > yesterday:
            print("Date should be at most yesterday! (leave it blank to get the latest update)")
            exit(1)

#repo with raw: in this way I can access the raw file
repo = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/"

#building url:
url = repo + filename

print("retrieving JSON at url " + url + " ... ")
JSONString = WebRetriever.getJson(url)
print("... done!")
print("")

JSONDict = JSONManager.parse(JSONString)

print("filtering, aggregating and sorting JSON data...")

if dateArg != "":
    print("date = " + dateArg)
    JSONDict = JSONManager.filterByDate(JSONDict, date)
JSONDictRegione = JSONManager.getTotaleRegionale(JSONDict)

#sorting by totale_casi and denominazione_regione
#since i need ascending order for denominazione_regione and descending order for totale casi,
#I do ascending order for both, but I negate each totale casi! :D
JSONDictSorted = sorted(JSONDictRegione, key = lambda i: ((i["totale_casi"]*-1), i["denominazione_regione"]))
print("... done!")
print("")

print("JSON content as a list of dictionaries:")
for x in JSONDictSorted:
    print(x)

JSONResult = JSONManager.serialize(JSONDictSorted)

print("")
print("JSON file content:")
print(JSONResult)

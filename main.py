import datetime
import sys

import pandas

import JSONManager
import WebRetriever

date = ""
dateArg = ""
filename = ""
outputExcelFile = ""

# handmade argument parser. I hate myself for this.
argv = sys.argv
hasDate = False
hasOEF = False

if len(argv) > 1:
    if len(argv) % 2 == 0:
        print("invalid argument list")
        exit(1)
    for arg in argv:
        if hasDate:
            dateArg = arg
            hasDate = False
        if hasOEF:
            outputExcelFile = arg
            hasOEF = False
        if arg == "-d":
            hasDate = True
        if arg == "-f":
            hasOEF = True

if filename == "":
    if dateArg == "":
        filename = "dpc-covid19-ita-province-latest.json"
    else:
        filename = "dpc-covid19-ita-province.json"

        # input sanitizing
        try:
            date = datetime.datetime.strptime(dateArg, "%Y-%m-%d")
        except ValueError:
            print("Incorrect data format, should be YYYY-MM-DD!")
            exit(1)

        if date < datetime.datetime(2020, 2, 24):
            print("Date should be after 2020-02-24!")
            exit(1)

        # searching data for at most yesterday allows to avoid errors if today's update is late!
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        if date > yesterday:
            print("Date should be at most yesterday! (leave it blank to get the latest update)")
            exit(1)

# repo with raw: in this way I can access the raw file
repo = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/"

# building url:
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

# sorting by totale_casi and denominazione_regione
# since i need ascending order for denominazione_regione and descending order for totale casi,
# I do ascending order for both, but I negate each totale casi! :D
JSONDictSorted = sorted(JSONDictRegione, key=lambda i: ((i["totale_casi"] * -1), i["denominazione_regione"]))
print("... done!")
print("")

print("JSON content as a list of dictionaries:")
for x in JSONDictSorted:
    print(x)

JSONResult = JSONManager.serialize(JSONDictSorted)

print("")
print("JSON file content:")
print(JSONResult)

# save it to excel file using Pandas
# notes: needed to pip install xlwt, index=False remove the extra first column
if len(argv) > 2:
    file = argv[2]

if outputExcelFile != "":
    pandas.read_json(JSONResult).to_excel(outputExcelFile + ".xls", index=False)

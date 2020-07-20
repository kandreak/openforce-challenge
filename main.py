import WebRetriever
import JSONManager

#todo get filename and date as arg

# example date format: 2020-07-16T17:00:00
filename = ""
date = "2020-07-16T17:00:00"

if filename == "":
    if date == "":
        filename = "dpc-covid19-ita-province-latest.json"
    else:
        filename = "dpc-covid19-ita-province.json"

#repo with raw: in this way I can access the raw file
repo = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/"

#building url:
url = repo + filename

print("retrieving JSON at url " + url + " ... ")
JSONString = WebRetriever.getJson(url)
print("... done!")
print("")

JSONDict = JSONManager.parse(JSONString)

print("filtering, aggregation and sorting of JSON data...")
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

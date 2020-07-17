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

JSONString = WebRetriever.getJson(url)
JSONDict = JSONManager.parse(JSONString)
JSONDict = JSONManager.filterByDate(JSONDict, date)
JSONDictRegione = JSONManager.getTotaleRegionale(JSONDict)

#sorting by totale_casi and denominazione_regione
#since i need ascending order for denominazione_regione and descending order for totale casi,
#I do ascending order for both, but I negate each totale casi! :D
JSONDictSorted = sorted(JSONDictRegione, key = lambda i: ((i["totale_casi"]*-1), i["denominazione_regione"]))

for x in JSONDictSorted:
    print(x)
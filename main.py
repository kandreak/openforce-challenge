import WebRetriever
import JSONManager

print("hello world")

#todo get filename as arg

filename = "dpc-covid19-ita-province-latest.json"

#repo with raw: in this way I can access the raw file
repo = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/"

#building url:
url = repo + filename

#print(url)

#print(WebRetriever.getJson(url))

JSONString = WebRetriever.getJson(url)

JSONDict = JSONManager.parse(JSONString)

print(JSONDict)
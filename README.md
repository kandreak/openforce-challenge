# openforce-challenge
The software I developed accesses the JSON data from the github repository https://github.com/pcm-dpc/COVID-19. It gets JSON data aggregated by “province” and aggregates it further by “regione”, summing up “totale_casi”. It allows to get the latest update, or to retrieve data from a certain date.
The software is divided in 2 branches:
script: it is meant to be used as a Python3 script, and it also allows to create an Excel file of the retrieved data;
web: it runs a Flask http server which answers to GET request with the retrieved data.
Software has been implemented in Python3.8. Code is available here:
https://github.com/kandreak/openforce-challenge.

-Files
main.py: entry point of the program. This is the only file changing between script and web branches.

JSONManager.py: component dealing with JSON data manipulation.

WebRetriever.py: component which accesses the web to get the files.

README.md: standard github readme file.

.gitignore: a standard python .gitignore provided by github.


--Script branch
The script branch hosts the version of the software which is meant to be called as a script via CLI. 
-Usage
python3 main.py [-d <date>][-f <outputExcelFile>]

date: optional parameter. If present, only data of the target date are shown. date must be in the format “YYYY-MM-DD”, and it must be between 2020-02-24 and yesterday (today is not allowed as a date, in order to avoid accessing the file while today’s data are still not present; leaving the date parameter blank allows to access to the latest available data).

outputExcelFile: optional parameter. If present, data are stored in an .xls file with the target name.

-Notes
First, arguments are parsed. If date has not been provided, the script chooses “dpc-covid19-ita-province-latest.json”, otherwise it accesses “dpc-covid19-ita-province.json”.
Then, a URL is composed from the chosen file and the target github repo: "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/" (note that https://raw.githubusercontent.com/ allows to get raw files from repos).
The WebRetriever gets the JSON string from the file, then the JSONManager parse it to a list of dictionaries.
after that, if we have a target date, the JSONManager filter it by date. In any case, it also aggregates data by “regione”, summing up “totale_casi”.
After that, a lambda function order the JSON data by descending “totale_casi”, and ascending alphabetical order of “denominazione_regione”. Results are printed to standard output.
Then, JSONManager serializes the JSON dictionaries back to a string, the script prints it, and finally Pandas is used to write the result to “outputExcelFile”.xls, if requested.


--Web branch
The web branch hosts a web version of the software providing almost the same functionalities as a Flask http server, answering on GET requests. The business logic is almost the same, except it does not print to standard out. It is now accessible at: http://andreakpiermarteri.pythonanywhere.com/openforcechallenge

-Usage
Accessing the URL directly provides the latest update of the JSON data. Otherwise, a GET parameter can be passed to provide a date:
http://andreakpiermarteri.pythonanywhere.com/openforcechallenge?date=2020-03-15
In this case, it returns the JSON data filtered by that date.

-Notes
First, “/openforcechallenge” is declared as the route of the web application. Then, python request is used to parse the optional argument (date).
After that, it follows the same business logic of the script version, except it does not print on the standard output (since this is a web server); instead, it just returns advices on the usage on the web page itself, if needed.
Finally, the JSON result string is served.

import requests
from threadManager import ThreadManager

countriesUri = "https://api.covid19api.com/countries"
countryUri = "https://api.covid19api.com/total/country/"

def processData(country):
    data = requests.get(countryUri + country["Slug"]).json()
    dataToSend = []
    previousValues = {
        "Confirmed": 0,
        "Deaths": 0,
        "Recovered": 0
    }

    for item in data:
        dataToSend.append({
            "Country": item["Country"], 
            "Confirmed": item["Confirmed"] - previousValues["Confirmed"],
            "Deaths": item["Deaths"] - previousValues["Deaths"],
            "Recovered": item["Recovered"] - previousValues["Recovered"]
            })

        previousValues = item

manager = ThreadManager(5,processData)
countries = requests.get(countriesUri).json()

for country in countries:
    manager.addResource(country)

    
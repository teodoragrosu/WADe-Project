import requests
from threadManager import ThreadManager
from datetime import datetime
from datetime import timedelta
import time
import dateutil.parser

countriesUri = "https://api.covid19api.com/countries"
countryUri = "https://api.covid19api.com/total/country/"
apiMetricsUri = "http://127.0.0.1:5000/api/metrics"

class MetricsConsumer:
    def __init__(self):
        self.threadManager = ThreadManager(5,lambda resource: self.processData(resource))
        self.countries = requests.get(countriesUri).json()
        self.countriesState = {}
        self.sleepTime = 900 #seconds
    
    def start(self):
        while True:
            for country in self.countries:
                lastQuery = None
                if country["Slug"] in self.countriesState:
                    lastQuery = self.countriesState[country["Slug"]]

                self.threadManager.addResource({"country": country, "lastQuery": lastQuery})
            time.sleep(self.sleepTime)
            

    def processData(self, data):
        params = {}
        fromDate = None
        if data["lastQuery"] != None:
            fromDate = data["lastQuery"]
            params["from"] = fromDate.strftime('%Y-%m-%dT00:00:00Z')
            params["to"] = datetime.now().strftime('%Y-%m-%dT00:00:00Z')

        items = requests.get(countryUri + data["country"]["Slug"], params = params).json()
        dataToSend = []
        previousValues = {
            "Confirmed": 0,
            "Deaths": 0,
            "Recovered": 0
        }

        for item in items:
            if fromDate == None or fromDate < dateutil.parser.parse(item["Date"]):
                dataToSend.append({
                    "Country": data["country"]["ISO2"], 
                    "Confirmed": item["Confirmed"] - previousValues["Confirmed"],
                    "Deaths": item["Deaths"] - previousValues["Deaths"],
                    "Recovered": item["Recovered"] - previousValues["Recovered"],
                    "Date": item["Date"]
                    })
                previousValues = item
                
        if len(dataToSend) > 0:
            requests.post(apiMetricsUri, json = {"items": dataToSend})
            self.countriesState[data["country"]["Slug"]] = dateutil.parser.parse(items[-1]["Date"])

consumer = MetricsConsumer()
consumer.start()

    
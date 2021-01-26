import requests
from consumers.threadManager import ThreadManager
from datetime import datetime
import time
import dateutil.parser

countriesUri = "https://api.covid19api.com/countries"
countryUri = "https://api.covid19api.com/total/country/"

apiMetricsUri = "http://127.0.0.1:5000/api/metrics"
apiMetricsInitialValuesUri = "http://127.0.0.1:5000/api/metrics/initialValues"


class MetricsConsumer:
    def __init__(self):
        self.threadManager = ThreadManager(1,lambda resource: self.processData(resource))
        self.countries = requests.get(countriesUri).json()[:20]
        self.countriesState = {}
        self.populateCountriesState()
        self.sleepTime = 3600 #seconds

    def start(self):
        while True:
            for country in self.countries:
                lastQuery = None
                if country["Slug"] in self.countriesState:
                    lastQuery = self.countriesState[country["Slug"]]

                self.threadManager.addResource({"country": country, "lastQuery": lastQuery})
            time.sleep(self.sleepTime)

    def populateCountriesState(self):
        try:
            latestState = requests.get(apiMetricsInitialValuesUri).json()
        except:
            return
        for country in latestState.keys():
            try:
                slug = next(c["Slug"] for c in self.countries if c["ISO2"] == country)
                self.countriesState[slug] = dateutil.parser.parse(latestState[country] + "T00:00:00Z")
            except:
                pass

    def processData(self, data):
        params = {}
        fromDate = None
        if data["lastQuery"] is not None:
            fromDate = data["lastQuery"]
            params["from"] = fromDate.strftime('%Y-%m-%dT00:00:00Z')
            params["to"] = datetime.now().strftime('%Y-%m-%dT00:00:00Z')

        items = requests.get(countryUri + data["country"]["Slug"], params=params).json()
        dataToSend = []
        previousValues = {
            "Confirmed": 0,
            "Deaths": 0,
            "Recovered": 0
        }

        for item in items:
            if fromDate is None or fromDate < dateutil.parser.parse(item["Date"]):
                dataToSend.append({
                    "country": data["country"]["ISO2"],
                    "confirmed": item["Confirmed"] - previousValues["Confirmed"],
                    "deceased": item["Deaths"] - previousValues["Deaths"],
                    "recovered": item["Recovered"] - previousValues["Recovered"],
                    "active": item["Active"],
                    "total_confirmed": item["Confirmed"],
                    "total_deceased": item["Deaths"],
                    "total_recovered": item["Recovered"],
                    "date": item["Date"]
                    })

            previousValues = item
                
        if len(dataToSend) > 0:
            requests.post(apiMetricsUri, params={"apiKey": "metricsConsumerApiKey"}, json={"items": dataToSend})
            self.countriesState[data["country"]["Slug"]] = dateutil.parser.parse(items[-1]["Date"])


consumer = MetricsConsumer()
consumer.start()

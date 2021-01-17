import requests
from threadManager import ThreadManager
from datetime import datetime
from datetime import timedelta
import time
import dateutil.parser
from newsfetch.news import newspaper

apiNewsUri = "http://127.0.0.1:5000/api/news"
apiKey = ""
newsApiUri = 'https://newsapi.org/v2/everything'

class NewsConsumer:
    def __init__(self):
        self.threadManager = ThreadManager(3, lambda resource: self.processData(resource))
        self.sleepTime = 960  # seconds
        self.params = {
            'q': 'covid',
            'pageSize': 100,
            'apiKey': apiKey,
            'sortBy': 'publishedAt',
            'page': 1,
            "apiKey": "newsConsumerApiKey"
        }

    def start(self):
        while True:
            self.params["from"] = (datetime.now() + timedelta(minutes = -300)).strftime('%Y-%m-%dT%H:%M:%SZ')
            self.params["to"] = (datetime.now() + timedelta(minutes = -285)).strftime('%Y-%m-%dT%H:%M:%SZ')
            news = requests.get(newsApiUri, params=self.params).json()["articles"]
            for n in news:
                self.threadManager.addResource((n['url'], n["publishedAt"], n["title"]))
            
            time.sleep(self.sleepTime)

    def processData(self, resource):
        news = newspaper(resource[0])

        if not any(item in news.keywords for item in ['covid', 'coronavirus', 'covid19', 'lockdown', 'virus', 'vaccine', 'illness', 'symptom', 'pandemic']):
            return

        requests.post(apiNewsUri, json={"url": resource[0], "date": resource[1], "title": resource[2], "keywords": news.keywords, "publication": news.publication })


consumer = NewsConsumer()
consumer.start()
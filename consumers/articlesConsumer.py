import requests
from threadManager import ThreadManager
from datetime import datetime
from datetime import timedelta
import time
import dateutil.parser
from newsfetch.news import newspaper
import json

apiArticlesUri = "http://127.0.0.1:5000/api/articles"
apiKey = ""
newsApiUri = 'https://newsapi.org/v2/everything'
sources = []

with open("../consumers/articleSources.json", "r") as sourcesFile:
    sources = json.load(sourcesFile)

class ArticlesConsumer:
    def __init__(self):
        self.threadManager = ThreadManager(3, lambda resource: self.processData(resource))
        self.sleepTime = 960  # seconds
        self.params = {
            'q': 'covid',
            'pageSize': 100,
            'apiKey': apiKey,
            'sortBy': 'publishedAt',
            'page': 1,
            'language': "en",
            'from': "2021-01-01",
            'to': "2021-01-02",
            'domains': ','.join(sources)
        }

    def start(self):
        while True:
            news = requests.get(newsApiUri, params=self.params).json()["articles"]
            for n in news:
                self.threadManager.addResource((n['url'], n["publishedAt"], n["title"], n["description"], n["author"]))

            return
    
    def processData(self, resource):
        article = newspaper(resource[0])

        requests.post(apiArticlesUri, params={"apiKey": "articlesConsumerApiKey"}, json={"url": resource[0], "date": resource[1], "title": resource[2], "authors": [resource[4]], "abstract": resource[3], "categories": [article.category]})

c = ArticlesConsumer()
c.start()
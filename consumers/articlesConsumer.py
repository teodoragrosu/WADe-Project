import requests
from threadManager import ThreadManager
from datetime import datetime
from datetime import timedelta
import time
import dateutil.parser
from newsfetch.news import newspaper
import json

apiArticlesUri = "http://127.0.0.1:5000/api/articles"
apiKey = "f314f8aa6b874a54b58bfa89907c1fd2"
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
            'from': "2021-01-03",
            'to': "2021-01-04",
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
        category = article.category
        categories = []
        if category == 'HEALTH':
            categories.append('health')
            articleType = 'article'
        elif category == 'research-article':
            articleType = 'research'
            category = None
        elif category == 'COMMENT & OPINION':
            articleType = "journal contribution"
            category = None
        else:
            articleType = 'article'

        if 'health' in article.keywords:
            categories.append('health')
        if 'life' in article.keywords:
            categories.append('life')
        if 'physics' in article.keywords:
            categories.append('physics')
        if 'virus' in article.keywords:
            categories.append('virus')
        if 'social' in article.keywords:
            categories.append('social')
        if 'history' in article.keywords:
            categories.append('history')
        if 'science' in article.keywords:
            categories.append('science')
        if 'economic' in article.keywords:
            categories.append('economic')
        if 'politics' in article.keywords:
            categories.append('politics')

        requests.post(apiArticlesUri, params={"apiKey": "articlesConsumerApiKey"}, json={"url": resource[0], "date": resource[1], "title": resource[2], "authors": [resource[4]], "abstract": resource[3], "categories": list(set(categories)), "articleType": articleType})

c = ArticlesConsumer()
c.start()
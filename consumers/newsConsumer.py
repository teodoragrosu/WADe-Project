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
        self.sleepTime = 900  # seconds
        self.params = {
            'q': 'covid',
            'pageSize': 100,
            'apiKey': apiKey,
            'sortBy': 'publishedAt',
            'from': "2021-01-01",
            'language': 'en'
        }

    def start(self):
        while True:
            try:
                latestDate = self.params['from']
                self.params["page"] = 1
                news = requests.get(newsApiUri, params=self.params).json()['articles']
                if len(news) > 0:
                    latestDate = news[0]["publishedAt"]

                while len(news) > 0:
                    try:
                        if self.params["page"] > 7:
                            break
                        for n in news:
                            self.threadManager.addResource((n['url'], n["publishedAt"], n["title"]))
                        self.params["page"] += 1
                        news = requests.get(newsApiUri, params=self.params).json()['articles']
                    except:
                        self.params["page"] += 1
                        news = requests.get(newsApiUri, params=self.params).json()['articles']
                        pass
            except:
                pass

            self.params['from'] = (dateutil.parser.parse(latestDate) + timedelta(minutes = 1)).strftime('%Y-%m-%dT%H:%M:%SZ')
            
            time.sleep(self.sleepTime)

    def processData(self, resource):
        news = newspaper(resource[0])

        if not any(item in news.keywords for item in ['covid', 'coronavirus', 'covid19', 'lockdown', 'virus', 'vaccine', 'illness', 'symptom', 'pandemic']):
            return

        if len(news.authors) > 0:
            author = news.authors[0]
        else:
            author = news.publication

        requests.post(apiNewsUri, json={"url": resource[0], "date": resource[1], "title": resource[2], "keywords": news.keywords, "author": author })


consumer = NewsConsumer()
consumer.start()
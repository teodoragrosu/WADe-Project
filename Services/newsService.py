from coda_graph.graph import CovidGraph
from coda_graph.graph_handler import GraphHandler


class NewsService:
    def __init__(self):
        self.graphHandler = GraphHandler("news")
        self.graph = CovidGraph("news")

    def addNews(self, news):
        self.graph.add_news(news["title"], news["date"], news["url"], news["publication"], news["keywords"])

    def get_news(self, id_=-1, publication="", limit=20, offset=0):
        return self.graphHandler.get_news(id_, publication, limit, offset)

    def serialize(self):
        self.graph.get_serialization("news")

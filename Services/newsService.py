from coda_graph.graph import CovidGraph
from coda_graph.graph_handler import GraphHandler

PATH = "http://localhost:8082/codapi/resources"


class NewsService:
    def __init__(self):
        self.graphHandler = GraphHandler()
        self.graph = CovidGraph()

    def addNews(self, news):
        self.graph.add_news("CO", news["title"], news["date"], news["url"], news["keywords"])

    def serialize(self):
        self.graph.get_serialization()

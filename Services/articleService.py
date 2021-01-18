from coda_graph.graph import CovidGraph
from coda_graph.graph_handler import GraphHandler


class ArticlesService:
    def __init__(self):
        self.graphHandler = GraphHandler("articles")
        self.graph = CovidGraph("articles")

    def addArticles(self, article):
        self.graph.add_article(article["title"], article["authors"], article["abstract"], article["date"], article["url"], art_type=article["articleType"], categories=article["categories"])

    def serialize(self):
        self.graph.get_serialization("articles")


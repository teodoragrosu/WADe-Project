from coda_graph.graph_handler import GraphHandler


class ArticlesService:
    def __init__(self):
        self.graphHandler = GraphHandler()

    def addArticles(self, article):
        self.graphHandler.add_articles(article["title"], article["authors"], article["abstract"], article["date"], article["url"], art_type=article["articleType"], categories=article["categories"])

    def get_articles(self, id_=-1, type_="", limit=20, offset=0):
        return self.graphHandler.get_articles(id_, type_, limit, offset)
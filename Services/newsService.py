from coda_graph.graph_handler import GraphHandler


class NewsService:
    def __init__(self):
        self.graphHandler = GraphHandler()

    def addNews(self, news):
        self.graphHandler.add_news(news["title"], news["date"], news["url"], news["publication"], news["keywords"], news.get("image_url"))

    def get_news(self, id_=-1, publication="", limit=20, offset=0):
        return self.graphHandler.get_news(id_, publication, limit, offset)


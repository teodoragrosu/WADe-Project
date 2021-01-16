from rdflib import Graph


class GraphStore:
    casesInstance = None
    newsInstance = None
    articlesInstance = None

    @staticmethod
    def getInstance(graph_type):
        if graph_type == "cases":
            if GraphStore.casesInstance is None:
                GraphStore.casesInstance = Graph().parse(f"../coda_graph/{graph_type}_graph.rdf", format="turtle")
            return GraphStore.casesInstance
        elif graph_type == "news":
            if GraphStore.newsInstance is None:
                GraphStore.newsInstance = Graph().parse(f"../coda_graph/{graph_type}_graph.rdf", format="turtle")
            return GraphStore.newsInstance
        elif graph_type == "articles":
            if GraphStore.articlesInstance is None:
                GraphStore.articlesInstance = Graph().parse(f"../coda_graph/{graph_type}_graph.rdf", format="turtle")
            return GraphStore.articlesInstance

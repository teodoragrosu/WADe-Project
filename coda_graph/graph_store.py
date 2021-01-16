from rdflib import Graph

class GraphStore:
    graphInstance = None

    @staticmethod
    def getInstance():
        if GraphStore.graphInstance is None:
            GraphStore.graphInstance = Graph().parse("../coda_graph/graph.rdf", format="turtle")
        return GraphStore.graphInstance

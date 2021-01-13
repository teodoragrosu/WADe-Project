import datetime
import json
from codAPI.graph import CovidGraph
from rdflib.namespace import SDO, OWL
from rdflib import Graph

PATH = "http://localhost:8082/codapi/resources"


def _create_graph():
    cg = CovidGraph()

    cg.add_country("RO")
    cg.add_cases("RO", "deceased", "2020-01-01", 1000)
    cg.add_cases("RO", "confirmed", "2020-01-02", 1200)
    cg.add_country("UK")  # hasCases false

    cg.add_news("RO", ["keyword1", "keyword2"], "2020-12-01", "google.com")

    cg.add_article("article1", ["auth1"], "abstract1", "2020-06-01", "google.com", "citation", "dataset", ['keyworddd'])
    cg.add_article("article2", ["auth1", "auth2"], "abstract2", "2020-12-01", "sdcdfvfs.com", "citation",
                   "journal contribution", ["keyword1"])
    cg.get_serialization()


class GraphHandler:
    def __init__(self):
        self.graph = Graph().parse("codApi/graph.rdf", format="turtle")

    def _get_results(self, query):
        results = []
        for row in self.graph.query(query, initNs={'SDO': SDO, 'owl': OWL}):
            article = {}
            for key, values in row.asdict().items():
                v = values.toPython()
                if isinstance(v, (datetime.date, datetime.datetime)):
                    article[key] = v.strftime("%Y-%m-%d")
                else:
                    article[key] = v
            results.append(article)

        return results

    def get_all_available_countries(self):
        query = f"""
            SELECT DISTINCT ?uri ?country_code
            WHERE {{
                    ?uri rdf:type SDO:Country .
                    ?uri <{PATH}/properties/IdentifiedBy> ?country_code .
        }} """
        return json.dumps(self._get_results(query))

    def get_cases_by_country_code(self, country_code):
        # by default, returns the cases for all days available
        query = f"""
            SELECT DISTINCT ?cases ?date ?type ?value ?country
            WHERE {{
                    ?cases rdfs:subClassOf owl:Thing .
                    ?cases <{PATH}/properties/IsReportedOn> ?date .
                    ?cases <{PATH}/properties/IsOfType> ?type .
                    ?cases rdf:value ?value .
                    ?country rdf:type SDO:Country .
                    ?country <{PATH}/properties/IdentifiedBy> ?country_code .
                    ?country rdf:type ?cases
            FILTER (?country_code = '{country_code}')
            }}
        """
        return json.dumps(self._get_results(query))

    def get_article_by_id(self, id_):
        query = f"""
            SELECT ?id ?title ?abstract ?uri ?art_type ?keywords
            WHERE {{
                    ?uri rdf:type SDO:ScholarlyArticle .
                    ?uri <{PATH}/properties/IdentifiedBy> ?id .
                    ?uri SDO:headline ?title .
                    ?uri SDO:abstract ?abstract .
                    ?uri SDO:url ?url .
                    ?uri <{PATH}/properties/hasType> ?art_type .
                    ?uri SDO:keywords ?keywords .
            FILTER (?id = {id_})
        }}"""
        return json.dumps(self._get_results(query))






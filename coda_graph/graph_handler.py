import datetime
import json
from rdflib.namespace import SDO, OWL, RDFS
from rdflib import Graph

PATH = "http://localhost:8082/codapi/resources"


class GraphHandler:
    def __init__(self):
        self.graph = Graph().parse("../coda_graph/graph.rdf", format="turtle")

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

    def _get_country_results(self, query):
        country = {}
        for row in self.graph.query(query, initNs={'SDO': SDO, 'owl': OWL, 'rdfs': RDFS}):
            if row.asdict().get("date"):
                _date = row.asdict()["date"].toPython().strftime("%Y-%m-%d")
                if _date not in country.keys():
                    country[_date] = {row.asdict()["type"].toPython(): row.asdict()["value"].toPython()}
                else:
                    country[_date].update({row.asdict()["type"].toPython(): row.asdict()["value"].toPython()})
            else:
                country[row.asdict()["country_code"].toPython()] = row.asdict()["uri"].toPython()

        return country

    def get_all_available_countries(self):
        query = f"""
            SELECT DISTINCT ?uri ?country_code
            WHERE {{
                    ?uri rdf:type SDO:Country .
                    ?uri <{PATH}/properties/IdentifiedBy> ?country_code .
        }} """
        return json.dumps(self._get_results(query))

    def get_cases_by_country_code(self, country_code, start_date="", end_date=""):
        """
        If start_date and end_date are not provided, the function returns the all time data for the specified country
        If only the start_date is provided, the statistics for that day are returned
        If both start_date and end_date are provided, the statistics for the date range are returned
        """
        if start_date and end_date:
            filter_condition = f"&& ?date >= '{start_date}'^^xsd:date && ?date <='{end_date}'^^xsd:date"
        elif start_date:
            filter_condition = f"&& ?date = '{start_date}'^^xsd:date"
        else:
            filter_condition = ""

        query = f"""
            SELECT DISTINCT ?cases ?date ?type ?value ?country
            WHERE {{
                    ?cases rdfs:subClassOf owl:Thing .
                    ?cases <{PATH}/properties/IsReportedOn> ?date .
                    ?cases <{PATH}/properties/IsOfType> ?type .
                    ?cases rdf:value ?value .
                    ?country rdf:type SDO:Country .
                    ?country <{PATH}/properties/IdentifiedBy> ?country_code .
                    ?country rdf:type ?cases .
            FILTER (?country_code = '{country_code}' {filter_condition})
            }}
        """
        return json.dumps(self._get_country_results(query))

    def _get_article_results(self, query):
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
        return json.dumps(self._get_article_results(query))

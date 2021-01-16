import datetime
import json
from rdflib.namespace import SDO, OWL, RDFS

from coda_graph.graph_store import GraphStore

PATH = "http://localhost:8082/codapi/resources"


class GraphHandler:
    def __init__(self, name):
        self.graph = GraphStore.getInstance(name)

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
        return json.dumps(self._get_country_results(query))

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
                elif key in ["authors", "categories"]:
                    article[key] = v.split(";")
                else:
                    article[key] = v
            results.append(article)

        return results

    def get_articles(self, id_=-1, type_="", limit=20, offset=0):
        """
        By default, if no id or type are specified, the latest 20 articles will be returned

        id_: int
        type_: string (eg. `dataset`, `article`)

        """
        filter_condition = ""
        if id_ >= 0:
            filter_condition = f"FILTER (?id = {id_})"
        elif type_:
            filter_condition = f"FILTER (?art_type = '{type_}')"

        query = f"""
            SELECT DISTINCT ?id ?title 
                            (group_concat(distinct ?a;separator=';') as ?authors) 
                            ?abstract ?date ?url ?citation ?art_type 
                            (group_concat(distinct ?c;separator=';') as ?categories)
            WHERE {{
                ?uri rdf:type SDO:ScholarlyArticle .
                ?uri <{PATH}/properties/IdentifiedBy> ?id .
                ?uri SDO:headline ?title .
                ?uri SDO:author ?a .
                ?uri SDO:abstract ?abstract .
                ?uri SDO:datePublished ?date .
                ?uri SDO:citation ?citation .
                ?uri SDO:url ?url .
                ?uri <{PATH}/properties/hasType> ?art_type .
                ?uri SDO:about ?c .
            {filter_condition}
            }}
            GROUP BY ?id
            ORDER BY DESC(?date) LIMIT {limit} OFFSET {offset}
        """

        return json.dumps(self._get_article_results(query))

    def _get_news_results(self, query):
        results = []
        for row in self.graph.query(query, initNs={'SDO': SDO, 'owl': OWL, 'rdfs': RDFS}):
            news = {}
            for key, values in row.asdict().items():
                v = values.toPython()
                if isinstance(v, datetime.date):
                    news[key] = v.strftime("%Y-%m-%d")
                elif key == "keywords":
                    news[key] = v.split(";")
                else:
                    news[key] = v
            results.append(news)

        return results

    def get_news(self, id_=-1, publication="", limit=20, offset=0):
        filter_condition = ""
        if id_ >= 0:
            filter_condition = f"FILTER (?id = {id_})"
        elif publication:
            filter_condition = f"FILTER (?publication = '{publication}')"

        query = f"""
            SELECT DISTINCT ?id ?publication ?title ?date ?url_source
                            (group_concat(distinct ?k;separator=';') as ?keywords)
            WHERE {{
                ?uri rdf:type SDO:NewsArticle .
                ?uri <{PATH}/properties/IdentifiedBy> ?id .
                ?uri <{PATH}/properties/PublishedIn> ?publication .
                ?uri SDO:headline ?title .
                ?uri SDO:datePublished ?date .
                ?uri SDO:url ?url_source .
                ?uri SDO:keywords ?k .
            {filter_condition}
            }}
            GROUP BY ?id
            ORDER BY DESC(?date) LIMIT {limit} OFFSET {offset}
        """
        return json.dumps(self._get_news_results(query))

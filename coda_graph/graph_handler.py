import json
from SPARQLWrapper import SPARQLWrapper, JSON, POST


# PATH = "http://localhost:7200/repositories/coda"
API_PATH = "http://localhost:5000/api/country/"
PATH = "http://35.190.193.250:7200/repositories/coda"   # cloud path


class GraphHandler:
    def __init__(self):
        self.wrapper = SPARQLWrapper(PATH)
        self.wrapper.user = "admin"
        self.wrapper.passwd = "root"
        self.wrapper.setReturnFormat(JSON)
        self.PREFIXES = """
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX ns1: <http://coda.org/resources/properties/>
            PREFIX ns2: <https://schema.org/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
        """

    @staticmethod
    def _get_country_results(response):
        countries = {}
        for r in response["results"]["bindings"]:
            if r.get("date"):
                _date = r["date"]["value"].split("T")[0]
                if _date not in countries.keys():
                    countries[_date] = {r["type"]["value"]: r["value"]["value"]}
                else:
                    countries[_date][r["type"]["value"]] = r["value"]["value"]
            elif r.get("month"):
                month = r["month"]["value"]
                if month not in countries.keys():
                    countries[month] = {
                        f'avg_{r["type"]["value"]}_per_day': r["avgValue"]["value"]
                    }
                else:
                    countries[month][f'avg_{r["type"]["value"]}_per_day'] = r[
                        "avgValue"
                    ]["value"]
            else:
                countries[
                    r["country_code"]["value"]
                ] = f"{API_PATH}{r['country_code']['value']}"

        return countries

    def ask_country_exists(self, country_code):
        self.wrapper.setQuery(
            f"""
            {self.PREFIXES}
            ASK 
                WHERE {{
                    ?country rdf:type ns2:Country .
                    ?country ns1:IdentifiedBy ?country_code .
                FILTER (?country_code = '{country_code}')
                }}
        """
        )
        response = self.wrapper.query().convert()
        return response["boolean"]

    def get_all_available_countries(self):
        self.wrapper.setQuery(
            f"""
            {self.PREFIXES}
            SELECT DISTINCT ?uri ?country_code
            WHERE {{
                    ?uri rdf:type ns2:Country .
                    ?uri ns1:IdentifiedBy ?country_code .
        }} """
        )

        response = self.wrapper.query().convert()
        return json.dumps(self._get_country_results(response))

    def get_cases_by_country_code(
        self, country_code, start_date="", end_date="", latest=False, download=False
    ):
        """
        If start_date and end_date are not provided, the function returns the all time data for the specified country
        If only the start_date is provided, the statistics for that day are returned
        If both start_date and end_date are provided, the statistics for the date range are returned

        latest = True will return the cases on the latest day in the graph (by default, False -> will return all cases)
        download = True will order the cases asc (for the download file)
        """
        if start_date and end_date:
            filter_condition = f"&& ?date >= '{start_date}'^^xsd:dateTime && ?date <='{end_date}'^^xsd:dateTime"
        elif start_date:
            filter_condition = f"&& ?date = '{start_date}'^^xsd:dateTime"
        else:
            filter_condition = ""

        self.wrapper.setQuery(
            f"""
            {self.PREFIXES}
            SELECT DISTINCT ?cases ?date ?type ?value ?country_code ?country
            WHERE {{
                    ?cases rdfs:subClassOf owl:Thing .
                    ?cases ns1:IsReportedOn ?date .
                    ?cases ns1:IsOfType ?type .
                    ?cases rdf:value ?value .
                    ?country rdf:type ns2:Country .
                    ?country ns1:IdentifiedBy ?country_code .
                    ?country rdf:type ?cases .
            FILTER (?country_code = '{country_code}' {filter_condition})
            }}
            ORDER BY {'ASC' if download else 'DESC'}(?date) {'LIMIT 7' if latest else ''}
        """
        )

        response = self.wrapper.query().convert()
        return json.dumps(self._get_country_results(response))

    def get_monthly_avg(self, country_code):
        self.wrapper.setQuery(
            f"""
            {self.PREFIXES}
            SELECT DISTINCT ?type (AVG(?value) as ?avgValue) (SUM(?value) as ?sumValue) ?month
            WHERE {{
                SELECT DISTINCT ?cases ?date ?type ?value ?country
                WHERE {{
                    ?cases rdfs:subClassOf owl:Thing .
                    ?cases ns1:IsReportedOn ?date .
                    ?cases ns1:IsOfType ?type .
                    ?cases rdf:value ?value .
                    ?country rdf:type ns2:Country .
                    ?country ns1:IdentifiedBy ?country_code .
                    ?country rdf:type ?cases .
                    FILTER (?country_code = '{country_code}'
                        && ?type in ('confirmed', 'active', 'recovered', 'deceased')
                        && YEAR(?date) = 2020)
                }}
                ORDER BY ASC(?date)
            }}
            GROUP BY ?type (MONTH(?date) as ?month)
        """
        )

        response = self.wrapper.query().convert()
        return json.dumps(self._get_country_results(response))

    def add_country(self, country_code):
        self.wrapper = SPARQLWrapper(f"{PATH}/statements")
        self.wrapper.user = "admin"
        self.wrapper.passwd = "root"
        self.wrapper.setMethod(POST)

        self.wrapper.setQuery(
            f"""
            {self.PREFIXES}
            INSERT DATA {{
                GRAPH <http://coda.org/countries> {{
                    <http://coda.org/resources/countries/{country_code}> rdf:type ns2:Country .
                    <http://coda.org/resources/countries/{country_code}> ns1:IdentifiedBy '{country_code}' .
                }}
            }}
        """
        )

        self.wrapper.queryType = "INSERT"
        self.wrapper.query()

    def add_cases(self, country_code, type_, date_, number):
        self.wrapper = SPARQLWrapper(f"{PATH}/statements")
        self.wrapper.user = "admin"
        self.wrapper.passwd = "root"
        self.wrapper.setMethod(POST)

        self.wrapper.setQuery(
            f"""
            {self.PREFIXES}
            INSERT DATA {{
                GRAPH <http://coda.org/countries> {{
                    _:a rdf:type owl:Class .
                    _:a rdfs:subClassOf owl:Thing .
                    _:a ns1:IsReportedOn '{date_}'^^xsd:dateTime .
                    _:a ns1:IsOfType '{type_}' .
                    _:a rdf:value '{number}'^^xsd:integer .
                    <http://coda.org/resources/countries/{country_code}> rdf:type _:a .
                }}
            }}
        """
        )

        self.wrapper.queryType = "INSERT"
        self.wrapper.query()

    def _get_latest_id(self, _type):
        # type -> NewsArticle or ScholarlyArticle
        self.wrapper.setQuery(
            f"""
            {self.PREFIXES}
            SELECT DISTINCT (MAX(?id) as ?max)
            WHERE {{
                ?uri rdf:type ns2:{_type} .
                ?uri ns1:IdentifiedBy ?id .
            }}
        """
        )
        response = self.wrapper.query().convert()
        return int(response["results"]["bindings"][0]["max"]["value"])

    @staticmethod
    def _get_article_results(response):
        results = {}
        for r in response["results"]["bindings"]:
            results[r["id"]["value"]] = {
                "date": r["date"]["value"],
                "title": r["title"]["value"],
                "authors": r["authors"]["value"].split(";"),
                "categories": r["categories"]["value"].split(";"),
                "type": r["art_type"]["value"],
                "abstract": r["abstract"]["value"],
                "url": r["url"]["value"],
            }
        return results

    def get_articles(self, id_=-1, type_="", limit=20, offset=0):
        """
        By default, if no id or type are specified, the latest 20 articles will be returned

        id_: int
        type_: string (eg. `dataset`, `article`)

        """
        filter_condition = ""
        if id_ >= 0:
            filter_condition = f"FILTER (?id = '{id_}')"
        elif type_:
            filter_condition = f"FILTER (?art_type = '{type_}')"

        self.wrapper.setQuery(
            f"""
            {self.PREFIXES}
            SELECT DISTINCT ?id ?title 
                            (group_concat(distinct ?a;separator=';') as ?authors) 
                            ?abstract ?date ?url ?art_type 
                            (group_concat(distinct ?c;separator=';') as ?categories)
            WHERE {{
                ?uri rdf:type ns2:ScholarlyArticle .
                ?uri ns1:IdentifiedBy ?id .
                ?uri ns2:headline ?title .
                ?uri ns2:author ?a .
                ?uri ns2:abstract ?abstract .
                ?uri ns2:datePublished ?date .
                ?uri ns2:url ?url .
                ?uri ns1:hasType ?art_type .
                ?uri ns2:about ?c .
            {filter_condition}
            }}
            GROUP BY ?id ?title ?abstract ?date ?url ?art_type 
            ORDER BY DESC(?date) LIMIT {limit} OFFSET {offset}
        """
        )

        response = self.wrapper.query().convert()
        return json.dumps(self._get_article_results(response))

    def add_articles(self, title, authors, abstract, date, url, art_type, categories):
        self.wrapper = SPARQLWrapper(f"{PATH}/statements")
        self.wrapper.user = "admin"
        self.wrapper.passwd = "root"
        self.wrapper.setMethod(POST)

        id_ = self._get_latest_id("ScholarlyArticle") + 1
        self.wrapper.setQuery(
            f"""
            {self.PREFIXES}
            INSERT DATA {{
                GRAPH <http://coda.org/articles> {{
                    <http://coda.org/resources/articles/{id_}> rdf:type ns2:ScholarlyArticle .
                    <http://coda.org/resources/articles/{id_}> ns2:headline '{title}' .
                    <http://coda.org/resources/articles/{id_}> ns2:authors '{authors}' .
                    <http://coda.org/resources/articles/{id_}> ns2:abstract '{abstract}' .
                    <http://coda.org/resources/articles/{id_}> ns2:datePublished '{date}'^^xsd:date .
                    <http://coda.org/resources/articles/{id_}> ns2:url '{url}'^^xsd:url .
                    <http://coda.org/resources/articles/{id_}> ns2:about {categories} .
                    <http://coda.org/resources/articles/{id_}> ns1:IdentifiedBy '{id_}'^^xsd:integer .
                    <http://coda.org/resources/articles/{id_}> ns1:hasType '{id_}' .
                }}
            }}
        """
        )

        self.wrapper.queryType = "INSERT"
        self.wrapper.query()

    @staticmethod
    def _get_news_results(response):
        results = {}
        for r in response["results"]["bindings"]:
            results[r["id"]["value"]] = {
                "date": r["date"]["value"],
                "title": r["title"]["value"],
                "publication": r["publication"]["value"],
                "keywords": r["keywords"]["value"].split(";"),
                "source": r["url_source"]["value"],
                "img_url": r["img_url"]["value"] if r.get("img_url") else "",
            }
        return results

    def get_news(self, id_=-1, publication="", limit=20, offset=0):
        filter_condition = ""
        if id_ >= 0:
            filter_condition = f"FILTER (?id = {id_})"
        elif publication:
            filter_condition = f"FILTER (?publication = '{publication}')"

        self.wrapper.setQuery(
            f"""
            {self.PREFIXES}
            SELECT DISTINCT ?id ?publication ?title ?date ?url_source ?img_url
                            (group_concat(distinct ?k;separator=';') as ?keywords)
            WHERE {{
                ?uri rdf:type ns2:NewsArticle .
                ?uri ns1:IdentifiedBy ?id .
                ?uri ns1:PublishedIn ?publication .
                ?uri ns2:url ?url_source .
                ?uri ns2:headline ?title .
                ?uri ns2:datePublished ?date .
                OPTIONAL {{?uri ns1:hasImage ?img_url}}
                ?uri ns2:keywords ?k .
            {filter_condition}
            }}
            GROUP BY ?id ?publication ?title ?date ?url_source ?img_url
            ORDER BY DESC(?date) LIMIT {limit} OFFSET {offset}
        """
        )
        response = self.wrapper.query().convert()
        return json.dumps(self._get_news_results(response))

    def add_news(self, title, date, url_source, publication, keywords, img_url):
        self.wrapper = SPARQLWrapper(f"{PATH}/statements")
        self.wrapper.user = "admin"
        self.wrapper.passwd = "root"
        self.wrapper.setMethod(POST)

        id_ = self._get_latest_id("NewsArticle") + 1
        self.wrapper.setQuery(
            f"""
            {self.PREFIXES}
            INSERT DATA {{
                GRAPH <http://coda.org/news> {{
                    <http://coda.org/resources/news/{id_}> rdf:type ns2:NewsArticle .
                    <http://coda.org/resources/news/{id_}> ns2:headline '{title}' .
                    <http://coda.org/resources/news/{id_}> ns2:datePublished '{date}'^^xsd:date .
                    <http://coda.org/resources/news/{id_}> ns2:url '{url_source}'^^xsd:url .
                    <http://coda.org/resources/news/{id_}> ns2:keywords {keywords} .
                    <http://coda.org/resources/news/{id_}> ns1:IdentifiedBy '{id_}'^^xsd:integer .
                    <http://coda.org/resources/news/{id_}> ns2:PublishedIn '{publication}' .
                    <http://coda.org/resources/news/{id_}> ns2:hasImage '{img_url}' .
                }}
            }}
        """
        )

        self.wrapper.queryType = "INSERT"
        self.wrapper.query()

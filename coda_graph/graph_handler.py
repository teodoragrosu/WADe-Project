import json
from SPARQLWrapper import SPARQLWrapper, JSON, POST
import shortuuid

PATH = "http://localhost:7200/repositories/coda"
API_PATH = "http://localhost:5000/api/country/"
#API_PATH = "https://coda-apiv1.herokuapp.com/api/country"
#PATH = "http://35.205.159.186:7200/repositories/coda"   # cloud path


class GraphHandler:
    def __init__(self):
        self.wrapper = SPARQLWrapper(PATH)
        self.wrapper.user = "admin"
        self.wrapper.passwd = "root"
        self.wrapper.setReturnFormat(JSON)
        self.PREFIXES = """
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX ns1: <http://coda.org/resources/properties/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX schema: <https://schema.org/>
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
                    ?country rdf:type schema:Country .
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
                    ?uri rdf:type schema:Country .
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
                    ?country rdf:type schema:Country .
                    ?country ns1:IdentifiedBy ?country_code .
                    ?country ns1:hasCases ?cases .
            FILTER (?country_code = '{country_code}' {filter_condition})
            }}
            ORDER BY {'ASC' if download else 'DESC'}(?date) {'LIMIT 7' if latest else ''}
        """
        )

        response = self.wrapper.query().convert()
        return json.dumps(self._get_country_results(response))

    def get_country_totals(self):
        self.wrapper.setQuery(
            f"""
                    {self.PREFIXES}
            SELECT ?cases ?date ?type ?value ?country_code ?country
            WHERE {{
                    ?cases rdfs:subClassOf owl:Thing .
                    ?cases ns1:IsReportedOn ?date .
                    ?cases ns1:IsOfType ?type .
                    ?cases rdf:value ?value .
                    ?country rdf:type schema:Country .
                    ?country ns1:IdentifiedBy ?country_code .
                    ?country ns1:hasCases ?cases .
            FILTER (?type = 'total_confirmed' && ?date = '2021-01-20'^^xsd:dateTime)
            }}
            ORDER BY DESC (?value) LIMIT 22
            """
        )
        response = self.wrapper.query().convert()
        return json.dumps(self._get_country_totals(response))

    @staticmethod
    def _get_country_totals(response):
        results = {}
        for r in response["results"]["bindings"]:
            results[r["country_code"]["value"]] = r["value"]["value"]
        return results

    def get_active_totals(self, start_date='', end_date=''):

        if start_date and end_date:
            filter_condition = f"&& ?date >= '{start_date}'^^xsd:dateTime && ?date <='{end_date}'^^xsd:dateTime"
        else:
            filter_condition = ''

        self.wrapper.setQuery(
            f"""
                    {self.PREFIXES}
            SELECT DISTINCT ?date (SUM(?value) as ?sumValue) WHERE {{
                SELECT ?date ?value
                WHERE {{
                        ?cases rdfs:subClassOf owl:Thing .
                        ?cases ns1:IsReportedOn ?date .
                        ?cases ns1:IsOfType ?type .
                        ?cases rdf:value ?value .
                        ?country ns1:hasCases ?cases .
                FILTER (?type = 'active' && ?value > 0 {filter_condition})
                }}
            ORDER BY ASC (?date)}}
            GROUP BY ?date
            """
        )
        response = self.wrapper.query().convert()
        return json.dumps(self._get_active_totals(response))

    @staticmethod
    def _get_active_totals(response):
        results = {}
        for r in response["results"]["bindings"]:
            results[r["date"]["value"][:10]] = r["sumValue"]["value"]
        return results

    def get_evol_totals(self):
        self.wrapper.setQuery(
            f"""
                    {self.PREFIXES}
            SELECT DISTINCT ?type (Sum(?value) as ?sumValue) ?date
            WHERE {{
                SELECT DISTINCT ?cases ?date ?type ?value
                WHERE {{
                    ?cases rdfs:subClassOf owl:Thing .
                    ?cases ns1:IsReportedOn ?date .
                    ?cases ns1:IsOfType ?type .
                    ?cases rdf:value ?value .
                    FILTER (?type in ('recovered', 'deceased') && ?value > 0)
                }}
                ORDER BY ASC(?date)
            }}
            GROUP BY ?type ?date
            """
        )
        response = self.wrapper.query().convert()
        return json.dumps(self._get_evol_totals(response))

    @staticmethod
    def _get_evol_totals(response):
        results = { 'date': [],
                    'recovered': [],
                    'deceased': []}
        for r in response["results"]["bindings"]:
            results["date"].append(r["date"]["value"][:10])
            results[r["type"]["value"]].append(r["sumValue"]["value"])

        results['date'] = list(set(results['date']))
        results['date'].sort()

        return results

    def get_pie_totals(self, pie_date=""):
        if pie_date:
            filter_condition = f"&& ?date <= '{pie_date}T00:00:00Z'^^xsd:dateTime"
        else:
            filter_condition = f"&& ?date = '2021-01-23T00:00:00Z'^^xsd:dateTime"

        self.wrapper.setQuery(
            f"""
            {self.PREFIXES}
            SELECT DISTINCT ?type (SUM(?value) as ?sumValue) WHERE {{
            SELECT ?type ?value ?date
            WHERE {{
                    ?cases rdfs:subClassOf owl:Thing .
                    ?cases ns1:IsReportedOn ?date .
                    ?cases ns1:IsOfType ?type .
                    ?cases rdf:value ?value .
                    ?country ns1:hasCases ?cases .
            FILTER (?type in ('total_confirmed', 'total_recovered', 'total_deceased') {filter_condition})
            }}
            }}
            GROUP BY ?type
            """
        )
        response = self.wrapper.query().convert()
        return json.dumps(self._get_pie_totals(response))

    @staticmethod
    def _get_pie_totals(response):
        results = {}
        for r in response["results"]["bindings"]:
            results[r["type"]["value"]] = r["sumValue"]["value"]
        return results

    def get_average_totals(self):
        self.wrapper.setQuery(
            f"""
            {self.PREFIXES}
            SELECT DISTINCT ?type (AVG(?value) as ?avgValue) ?month
            WHERE {{
                SELECT DISTINCT ?cases ?date ?type ?value
                WHERE {{
                    ?cases rdfs:subClassOf owl:Thing .
                    ?cases ns1:IsReportedOn ?date .
                    ?cases ns1:IsOfType ?type .
                    ?cases rdf:value ?value .
                    FILTER (?type in ('confirmed', 'recovered', 'deceased')
                        && YEAR(?date) = 2020 && ?value > 0)
                }}
                ORDER BY ASC(?date)
            }}
            GROUP BY ?type (MONTH(?date) as ?month)
            """
        )
        response = self.wrapper.query().convert()
        return json.dumps(self._get_average_totals(response))

    @staticmethod
    def _get_average_totals(response):
        results = {}
        for r in response["results"]["bindings"]:
            results[r["month"]["value"]] = {}
        for r in response["results"]["bindings"]:
            updt = {'avg_'+r["type"]["value"]+'_per_day': r["avgValue"]["value"]}
            results[r["month"]["value"]].update(updt)
        return results

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
                    ?country rdf:type schema:Country .
                    ?country ns1:IdentifiedBy ?country_code .
                    ?country ns1:hasCases ?cases .
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
                    <http://coda.org/resources/countries/{country_code}> rdf:type schema:Country .
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
                    <http://coda.org/resources/countries/{country_code}> ns1:hasCases _:a .
                }}
            }}
        """
        )

        self.wrapper.queryType = "INSERT"
        self.wrapper.query()

    def _get_latest_id(self, _type):
        # type -> NewsArticle or ScholarlyArticle
        self.wrapper.setQuery(f"""
            {self.PREFIXES}
            SELECT DISTINCT (MAX(?id) as ?max)
            WHERE {{
                ?uri rdf:type schema:{_type} .
                ?uri ns1:IdentifiedBy ?id .
            }}
        """
        )
        response = self.wrapper.query().convert()
        return int(response["results"]["bindings"][0]["max"]["value"])

    @staticmethod
    def _get_article_results(response):
        results = []
        for r in response["results"]["bindings"]:
            results.append({
                "date": r["date"]["value"],
                "title": r["title"]["value"],
                "authors": r["authors"]["value"].split(", "),
                "categories": r["categories"]["value"].split(";"),
                "type": r["art_type"]["value"],
                "abstract": r["abstract"]["value"],
                "url": r["url"]["value"],
            })
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
            SELECT DISTINCT ?id ?title ?authors ?abstract ?date ?url ?art_type ?categories
            WHERE {{
                ?uri rdf:type schema:ScholarlyArticle .
                ?uri ns1:IdentifiedBy ?id .
                ?uri schema:headline ?title .
                ?uri schema:author ?authors .
                ?uri schema:abstract ?abstract .
                ?uri schema:datePublished ?date .
                ?uri schema:url ?url .
                ?uri ns1:hasType ?art_type .
                ?uri schema:about ?categories .
            {filter_condition}
            }}
            ORDER BY DESC(?date) LIMIT {limit} OFFSET {offset}
        """
        )

        response = self.wrapper.query().convert()
        return json.dumps(self._get_article_results(response))

    def get_articles_filtered(self, type_="", limit=20, offset=0, search_term="", categories=[]):
        filter_condition = ""
        if type_:
            filter_condition += f"?art_type = '{type_}' &&"
        if search_term:
            filter_condition += f"contains(?title, \"{search_term}\" ) &&"
        if len(categories) > 0:
            category_condition = ""
            for category in categories:
                category_condition += f"contains(?categories, \"{category}\" ) ||"
            filter_condition += "( " + category_condition[:-3] + " ) &&"

        if filter_condition:
            filter_condition = f"FILTER ({filter_condition[:-3]})"

        self.wrapper.setQuery(f"""
            {self.PREFIXES}
            SELECT DISTINCT ?id ?title ?authors
                            ?abstract ?date ?url ?art_type 
                            ?categories
            WHERE {{
                ?uri rdf:type schema:ScholarlyArticle .
                ?uri ns1:IdentifiedBy ?id .
                ?uri schema:headline ?title .
                ?uri schema:author ?authors .
                ?uri schema:abstract ?abstract .
                ?uri schema:datePublished ?date .
                ?uri schema:url ?url .
                ?uri ns1:hasType ?art_type .
                ?uri schema:about ?categories .
            {filter_condition}
            }}
            ORDER BY DESC(?date) LIMIT {limit} OFFSET {offset}
            """)

        response = self.wrapper.query().convert()
        return json.dumps(self._get_article_results(response))

    def add_articles(self, title, authors, abstract, date, url, art_type, categories):
        id_ = shortuuid.uuid()

        self.wrapper = SPARQLWrapper(f"{PATH}/statements")
        self.wrapper.user = "admin"
        self.wrapper.passwd = "root"
        self.wrapper.setMethod(POST)

        self.wrapper.setQuery(
            f"""
            {self.PREFIXES}
            INSERT DATA {{
                GRAPH <http://coda.org/articles> {{
                    <http://coda.org/resources/articles/{id_}> rdf:type schema:ScholarlyArticle .
                    <http://coda.org/resources/articles/{id_}> schema:headline "{title}" .
                    <http://coda.org/resources/articles/{id_}> schema:author "{authors}" .
                    <http://coda.org/resources/articles/{id_}> schema:abstract "{abstract}" .
                    <http://coda.org/resources/articles/{id_}> ns1:hasType '{art_type}' .
                    <http://coda.org/resources/articles/{id_}> schema:datePublished '{date}'^^xsd:date .
                    <http://coda.org/resources/articles/{id_}> schema:url '{url}'^^xsd:url .
                    <http://coda.org/resources/articles/{id_}> schema:about "{';'.join(categories)}" .
                    <http://coda.org/resources/articles/{id_}> ns1:IdentifiedBy '{id_}' .
                }}
            }}
        """
        )

        self.wrapper.queryType = "INSERT"
        self.wrapper.query()

    @staticmethod
    def _get_news_results(response):
        results = []
        for r in response["results"]["bindings"]:
            results.append({
                "date": r["date"]["value"],
                "title": r["title"]["value"],
                "publication": r["publication"]["value"],
                "keywords": r["keywords"]["value"].split(";"),
                "source": r["url_source"]["value"],
                "img_url": r["img_url"]["value"] if r.get("img_url") else "",
            })
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
            SELECT DISTINCT ?id ?publication ?title ?date ?url_source ?img_url ?keywords
            WHERE {{
                ?uri rdf:type schema:NewsArticle .
                ?uri ns1:IdentifiedBy ?id .
                ?uri ns1:PublishedIn ?publication .
                ?uri schema:url ?url_source .
                ?uri schema:headline ?title .
                ?uri schema:datePublished ?date .
                OPTIONAL {{?uri ns1:hasImage ?img_url}}
                ?uri schema:keywords ?keywords .
            {filter_condition}
            }}
            ORDER BY DESC(?date) LIMIT {limit} OFFSET {offset}
        """
        )
        response = self.wrapper.query().convert()
        return json.dumps(self._get_news_results(response))

    def get_news_filtered(self, publication="", limit=20, offset=0, search_term=""):
        filter_condition = ""
        if publication:
            filter_condition += f"?publication = '{publication}' &&"
        if search_term:
            filter_condition += f"contains(?title, \"{search_term}\" ) &&"

        if filter_condition:
            filter_condition = f"FILTER ({filter_condition[:-3]})"

        self.wrapper.setQuery(
            f"""
            {self.PREFIXES}
            SELECT DISTINCT ?id ?publication ?title ?date ?url_source ?img_url
                            (group_concat(distinct ?k;separator=';') as ?keywords)
            WHERE {{
                ?uri rdf:type schema:NewsArticle .
                ?uri ns1:IdentifiedBy ?id .
                ?uri ns1:PublishedIn ?publication .
                ?uri schema:url ?url_source .
                ?uri schema:headline ?title .
                ?uri schema:datePublished ?date .
                OPTIONAL {{?uri ns1:hasImage ?img_url}}
                ?uri schema:keywords ?k .
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

        id_ = shortuuid.uuid()
        self.wrapper.setQuery(
            f"""
            {self.PREFIXES}
            INSERT DATA {{
                GRAPH <http://coda.org/news> {{
                    <http://coda.org/resources/news/{id_}> rdf:type schema:NewsArticle .
                    <http://coda.org/resources/news/{id_}> schema:headline "{title}" .
                    <http://coda.org/resources/news/{id_}> schema:datePublished '{date}'^^xsd:date .
                    <http://coda.org/resources/news/{id_}> schema:url '{url_source}'^^xsd:url .
                    <http://coda.org/resources/news/{id_}> schema:keywords "{';'.join(keywords)}" .
                    <http://coda.org/resources/news/{id_}> ns1:IdentifiedBy '{id_}' .
                    <http://coda.org/resources/news/{id_}> ns1:PublishedIn "{publication}" .
                    <http://coda.org/resources/news/{id_}> ns1:hasImage '{img_url}' .
                }}
            }}
        """
        )

        self.wrapper.queryType = "INSERT"
        self.wrapper.query()

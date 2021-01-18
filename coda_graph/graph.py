from rdflib import URIRef, BNode, Literal, Graph
from rdflib.namespace import RDF, SDO, OWL, RDFS, XSD
from coda_graph.graph_store import GraphStore

PATH = "http://localhost:8082/codapi/resources"
PROPERTIES = [
    "IsOfType",         # CASES -> one of confirmed, deceased, recovered, tested;
    "IsReportedOn",     # CASES -> reported on DATE
    "IdentifiedBy",     # COUNTRY -> COUNTRY CODE, ARTICLE -> ID, NEWS -> ID
    "PublishedIn",      # NEWS -> PUBLICATION
    "hasCases",         # COUNTRY -> CASES
]


class CovidGraph:
    def __init__(self, name):
        self.graph = GraphStore.getInstance(name)
        self.add_properties()
        self.news_id = 0
        self.article_id = 0

    def add_properties(self):
        for property_name in PROPERTIES:
            uri = URIRef(f"{PATH}/properties/{property_name}")
            self.graph.add((uri, RDF.type, RDF.Property))

    def update_property(self, resource_uri, property_name, new_value):
        self.graph.set((resource_uri, URIRef(f"{PATH}/properties/{property_name}"), new_value))

    def remove_property(self):
        pass  # TODO

    def add_country(self, country_code):
        """
        The country. For example, USA. You can also provide the two-letter ISO 3166-1 alpha-2 country code.
        https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Officially_assigned_code_elements
        """
        uri = URIRef(f"{PATH}/countries/{country_code}")
        self.graph.add((uri, RDF.type, SDO.Country))
        # set IdentifiedBy country code property
        self.graph.add((uri, URIRef(f"{PATH}/properties/IdentifiedBy"), Literal(country_code)))
        # after creation, the country entry has no cases yet
        self.graph.add((uri, URIRef(f"{PATH}/properties/hasCases"), SDO.false))

    def make_cases(self, case_type, date):
        assert case_type in ["confirmed", "deceased", "recovered", "active", "total_confirmed", "total_deceased",
                             "total_recovered"]

        cases = BNode()  # resource node where the exact URI is not known, a GUID is generated
        self.graph.add((cases, RDF.type, OWL.Class))
        self.graph.add((cases, RDFS.subClassOf, OWL.Thing))

        # set IsReportedOn property
        self.graph.add((cases, URIRef(f"{PATH}/properties/IsReportedOn"), Literal(date, datatype=XSD.dateTime)))
        # set IsOneOf property
        self.graph.add((cases, URIRef(f"{PATH}/properties/IsOfType"), Literal(case_type)))

        return cases

    def add_cases(self, country_code, case_type, date, number):
        country_uri = URIRef(f"{PATH}/countries/{country_code}")
        case_node = self.make_cases(case_type, date)
        self.graph.add((case_node, RDF.value, Literal(number, datatype=XSD.integer)))

        self.graph.add((country_uri, RDF.type, case_node))

        # update hasCases property for country
        self.update_property(country_uri, "hasCases", SDO.true)

    def add_news(self, title, date, url_source, publication, keywords=None):
        news_uri = URIRef(f"{PATH}/news/{self.news_id}")
        self.graph.add((news_uri, RDF.type, SDO.NewsArticle))  # https://schema.org/NewsArticle

        # schema.org properties:
        self.graph.add((news_uri, SDO.headline, Literal(title)))
        self.graph.add((news_uri, SDO.datePublished, Literal(date, datatype=XSD.dateTime)))
        self.graph.add((news_uri, SDO.url, Literal(url_source, datatype=XSD.url)))
        if keywords:
            for k in keywords:
                self.graph.add((news_uri, SDO.keywords, Literal(k)))
        else:
            self.graph.add((news_uri, SDO.keywords, Literal("")))

        # custom properties:
        self.graph.add((news_uri, URIRef(f"{PATH}/properties/IdentifiedBy"), Literal(self.news_id)))
        self.graph.add((news_uri, URIRef(f"{PATH}/properties/PublishedIn"), Literal(publication)))

        self.news_id += 1

    def add_article(self, title, authors, abstract, date, url_source, citation="", art_type="", categories=None):
        # MANDATORY FIELDS: title, authors, abstract, date, url_source
        article_uri = URIRef(f"{PATH}/articles/{self.article_id}")

        # schema.org properties:
        self.graph.add((article_uri, RDF.type, SDO.ScholarlyArticle))  # https://schema.org/ScholarlyArticle
        self.graph.add((article_uri, SDO.headline, Literal(title)))
        for a in authors:
            self.graph.add((article_uri, SDO.author, Literal(a)))
        self.graph.add((article_uri, SDO.abstract, Literal(abstract)))
        self.graph.add((article_uri, SDO.datePublished, Literal(date, datatype=XSD.dateTime)))
        self.graph.add((article_uri, SDO.url, Literal(url_source, datatype=XSD.url)))
        self.graph.add((article_uri, SDO.citation, Literal(citation)))

        if categories:
            for c in categories:
                self.graph.add((article_uri, SDO.about, Literal(c)))
        else:
            self.graph.add((article_uri, SDO.about, Literal("")))

        # custom properties:
        if art_type:
            assert art_type in ["article", "research", "journal contribution", "dataset"]
            self.graph.add((article_uri, URIRef(f"{PATH}/properties/hasType"), Literal(art_type)))
        else:
            self.graph.add((article_uri, URIRef(f"{PATH}/properties/hasType"), Literal("")))
        self.graph.add((article_uri, URIRef(f"{PATH}/properties/IdentifiedBy"), Literal(self.article_id)))

        self.article_id += 1

    def get_serialization(self, name):
        return self.graph.serialize(destination=f"../coda_graph/{name}_graph.rdf", format="turtle")


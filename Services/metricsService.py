from coda_graph.graph import CovidGraph
from coda_graph.graph_handler import GraphHandler
import json

PATH = "http://localhost:8082/codapi/resources"


class MetricsService:
    def __init__(self):
        self.graphHandler = GraphHandler()
        self.graph = CovidGraph()

    def addMetrics(self, metrics):
        country = metrics[0]["country"]
        availableCountries = json.loads(self.graphHandler.get_all_available_countries())
        if not any(c["country_code"] == country for c in availableCountries):
            self.graph.add_country(country)

        for metric in metrics:
            print(metric)
            self.graph.add_cases(country, "confirmed", metric["date"], metric["confirmed"])
            self.graph.add_cases(country, "deceased", metric["date"], metric["deceased"])
            self.graph.add_cases(country, "recovered", metric["date"], metric["recovered"])
            self.graph.add_cases(country, "active", metric["date"], metric["active"])
            self.graph.add_cases(country, "total_confirmed", metric["date"], metric["total_confirmed"])
            self.graph.add_cases(country, "total_deceased", metric["date"], metric["total_deceased"])
            self.graph.add_cases(country, "total_recovered", metric["date"], metric["total_recovered"])

    def get_metrics(self, country_code, start_date="", end_date=""):
        return self.graphHandler.get_cases_by_country_code(country_code, start_date, end_date)

    def serialize(self):
        self.graph.get_serialization()

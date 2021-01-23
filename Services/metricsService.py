from coda_graph.graph_handler import GraphHandler
import json


class MetricsService:
    def __init__(self):
        self.graphHandler = GraphHandler()

    def addMetrics(self, metrics):
        country = metrics[0]["country"]
        if not self.graphHandler.ask_country_exists(country):
            self.graphHandler.add_country(country)

        for metric in metrics:
            self.graphHandler.add_cases(country, "confirmed", metric["date"], metric["confirmed"])
            self.graphHandler.add_cases(country, "deceased", metric["date"], metric["deceased"])
            self.graphHandler.add_cases(country, "recovered", metric["date"], metric["recovered"])
            self.graphHandler.add_cases(country, "active", metric["date"], metric["active"])
            self.graphHandler.add_cases(country, "total_confirmed", metric["date"], metric["total_confirmed"])
            self.graphHandler.add_cases(country, "total_deceased", metric["date"], metric["total_deceased"])
            self.graphHandler.add_cases(country, "total_recovered", metric["date"], metric["total_recovered"])

    def get_metrics_initial_values(self):
        result = {}
        countries = json.loads(self.graphHandler.get_all_available_countries())
        for country in countries:
            metrics = list(json.loads(self.get_country_metrics(country, "", "", latest=True, download=False)).keys())
            if metrics:
                result[country] = metrics[0]

        return result

    def get_all_metrics(self):
        all_data = {}
        all_countries = json.loads(self.graphHandler.get_all_available_countries())
        for country_code in all_countries.keys():
            all_data[country_code] = json.loads(self.graphHandler.get_cases_by_country_code(country_code))
        return all_data

    def get_country_metrics(self, country_code, start_date="", end_date="", latest=False, download=False):
        return self.graphHandler.get_cases_by_country_code(country_code, start_date, end_date, latest, download)

    def get_country_monthly_avg(self, country_code):
        return self.graphHandler.get_monthly_avg(country_code)

    def get_country_totals(self):
        return self.graphHandler.get_country_totals()

    def get_pie_totals(self, pie_date=""):
        return self.graphHandler.get_pie_totals(pie_date)

    def get_average_totals(self):
        return self.graphHandler.get_average_totals()

    def get_active_totals(self, start_date="", end_date=""):
        return self.graphHandler.get_active_totals(start_date, end_date)

    def get_evol_totals(self):
        return self.graphHandler.get_evol_totals()

    def serialize(self):
        self.graph.get_serialization("cases")
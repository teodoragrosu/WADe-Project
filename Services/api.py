import csv
import json
from datetime import datetime
from flask import Flask, jsonify, request, abort, send_file
from flask_cors import CORS

from Services.articleService import ArticlesService
from Services.decorators.apiKeyDecorator import require_app_key
from Services.metricsService import MetricsService
from Services.newsService import NewsService
from coda_graph.graph_handler import GraphHandler


app = Flask(__name__, static_url_path="")
CORS(app)
metricsService = MetricsService()
newsService = NewsService()
articlesService = ArticlesService()


# ====================================== ERROR CODES ==============================================
@app.errorhandler(400)
def bad_request(error_message="Error: Bad Request"):
    return jsonify(error=str(error_message)), 400


@app.errorhandler(404)
def not_found(error_message="Error: Resource not found"):
    return jsonify(error=str(error_message)), 404


@app.errorhandler(500)
def server_error(error_message='Error: Internal server error'):
    return jsonify(error=str(error_message)), 500


# ==================================== METRICS ENDPOINTS ==================================================
@app.route('/api/metrics/initialValues', methods=['GET'])
@require_app_key
def getMetricsInitialValues():
    result = metricsService.get_metrics_initial_values()
    return jsonify(result)


@app.route('/api/metrics', methods=['POST'])
@require_app_key
def addMetrics():
    metricsService.addMetrics(request.json["items"])
    return jsonify({'status': 1})


@app.route('/api/metrics', methods=['GET', 'POST'])
def metrics():
    if request.method == 'GET':
        data = metricsService.get_all_metrics()
        return jsonify(data)
    else:
        return abort(405, "Method not allowed!")


@app.route('/api/countries', methods=['GET'])
def get_all_available_countries():
    if request.method != "GET":
        return abort(405, "Method not allowed!")

    return metricsService.graphHandler.get_all_available_countries()


@app.route('/api/country/<string:country_code>', methods=['GET'])
@app.route('/api/country/<string:country_code>/latest', methods=['GET'])
def get_country_metrics(country_code):
    if request.method == "GET":
        if "latest" in request.url_rule.rule:
            data = metricsService.get_country_metrics(country_code, request.args[datetime.now().strftime("%Y-%m-%d")])
        elif request.args.get("date"):
            data = metricsService.get_country_metrics(country_code, request.args["date"])
        else:
            data = metricsService.get_country_metrics(country_code, request.args.get("from", ""), request.args.get("to", ""))
        if data != "{}":
            return data
        else:
            return jsonify("No data found for the country you selected. Please choose another date or checkout the list"
                           " of country codes available at http://127.0.0.1:5000/api/countries")
    else:
        return abort(405, "Method not allowed!")


@app.route('/api/country/monthly/<string:country_code>', methods=['GET'])
def get_country_monthly_avg(country_code):
    if request.method == "GET":
        if not country_code:
            return abort(400, "Please provide a country code!")
        return metricsService.get_country_monthly_avg(country_code)
    else:
        return abort(405, "Method not allowed!")


@app.route('/api/country/<string:country_code>/download', methods=['GET'])
def download_country_metrics(country_code):
    if request.method != "GET":
        return abort(405, "Method not allowed!")

    download_format = request.args.get("format")
    if not download_format or download_format.lower() not in ["json", "csv"]:
        return abort(400, description="Download format incorrect or not specified! Available formats: CSV, JSON")

    data = metricsService.get_country_metrics(country_code,
                                              request.args.get("from", ""),
                                              request.args.get("to", ""),
                                              download=True)
    file_path = f"{country_code}_data.{request.args['format']}"
    with open(file_path, "w") as metrics_file:
        if download_format.lower() == "json":
            json.dump(json.loads(data), metrics_file)
            mimetype = "application/json"
        elif download_format.lower() == "csv":
            _data = json.loads(data)
            writer = csv.DictWriter(metrics_file,
                                    fieldnames=["Date",
                                                "Confirmed",
                                                "Recovered",
                                                "Deceased",
                                                "Active",
                                                "Total Confirmed",
                                                "Total Recovered",
                                                "Total Deceased"])
            writer.writeheader()
            for date, values in _data.items():
                writer.writerow({
                    "Date": date,
                    "Confirmed": values["confirmed"],
                    "Recovered": values["recovered"],
                    "Deceased": values["deceased"],
                    "Active": values["active"],
                    "Total Confirmed": values["total_confirmed"],
                    "Total Recovered": values["total_recovered"],
                    "Total Deceased": values["total_deceased"],
                })
            mimetype = "text/csv"

    return send_file(file_path, mimetype=mimetype, attachment_filename=file_path, as_attachment=True)


# =========================================== NEWS ENDPOINTS ==============================================

@app.route('/api/news', methods=['POST'])
@require_app_key
def add_news():
    newsService.addNews(request.json)
    return jsonify({'status': 1})


@app.route('/api/news/latest', methods=['GET'])
@app.route('/api/news/filter/<string:publication>', methods=['GET'])
def get_news(publication=""):
    if request.method == 'GET':
        if "latest" in request.url_rule.rule:
            data = newsService.get_news(limit=request.args.get("limit", 20),
                                        offset=request.args.get("offset", 0))
        elif "filter" in request.url_rule.rule:
            data = newsService.get_news(publication=publication,
                                        limit=request.args.get("limit", 20),
                                        offset=request.args.get("offset", 0))
        return data
    else:
        return abort(405, "Method not allowed!")


# =========================================== ARTICLE ENDPOINTS ==============================================

@app.route('/api/articles', methods=['POST'])
@require_app_key
def add_articles():
    articlesService.addArticles(request.json)
    return jsonify({'status': 1})

@app.route('/api/articles/latest', methods=['GET'])
@app.route('/api/articles/filter/<int:id_>', methods=['GET'])
@app.route('/api/articles/filter/<string:type_>', methods=['GET'])
def get_articles(id_=-1, type_=""):
    if request.method == 'GET':
        # TODO: remove this after ArticleService is added
        handler = GraphHandler("articles")
        if "latest" in request.url_rule.rule:
            data = handler.get_articles(limit=request.args.get("limit", 20),
                                        offset=request.args.get("offset", 0))
        elif "filter" in request.url_rule.rule:
            data = handler.get_articles(id_=id_,
                                        type_=type_,
                                        limit=request.args.get("limit", 20),
                                        offset=request.args.get("offset", 0))
        return data
    else:
        return abort(405, "Method not allowed!")

# =========================================== GRAPH ENDPOINTS ==============================================


@app.route('/api/graph/serialize/<string:type_>', methods=['GET'])
def serialize(type_):
    # type -> what graph to serialize (cases, news, articles)
    if request.method == "GET":
        if type_ == "cases":
            metricsService.serialize()
        elif type_ == "news":
            newsService.serialize()
        elif type_ == "articles":
            articlesService.serialize()
        else:
            return abort(400, "Bad Request")
        return jsonify({'status': 1})
    else:
        return abort(405, "Method not allowed!")


if __name__ == '__main__':
    app.run(debug=True)
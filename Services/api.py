import csv
import json
import os
import pathlib
from os.path import dirname, abspath

from flask import Flask, jsonify, request, abort, send_file, send_from_directory
from flask_cors import CORS

from Services.articleService import ArticlesService
from Services.decorators.apiKeyDecorator import require_app_key
from Services.metricsService import MetricsService
from Services.newsService import NewsService


app = Flask(__name__, static_url_path="")
CORS(app)
metricsService = MetricsService()
newsService = NewsService()
articlesService = ArticlesService()


# ====================================== INDEX ====================================================
@app.route('/', methods=['GET'])
def index():
    return jsonify({"Welcome to the CODA API! Check out the documentation at": "https://coda-documentation.herokuapp.com/v1/ui/"})


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
# @require_app_key
def addMetrics():
    metricsService.addMetrics(request.json["items"])
    return jsonify({'status': 1})


@app.route('/api/metrics', methods=['GET'])
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
            data = metricsService.get_country_metrics(country_code, latest=True)
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

@app.route('/api/metrics/totals', methods=['GET'])
def get_country_totals():
    if request.method == "GET":
        data = metricsService.get_country_totals()
        return data
    else:
        return abort(405, "Method not allowed!")

@app.route('/api/metrics/active', methods=['GET'])
def get_active_totals():
    if request.method == "GET":
        data = metricsService.get_active_totals(request.args.get("from", ""), request.args.get("to", ""))
        return data
    else:
        return abort(405, "Method not allowed!")

@app.route('/api/metrics/pie', methods=['GET'])
def get_pie_totals():
    if request.method == "GET":
        data = metricsService.get_pie_totals(request.args.get("date", ""))
        return data
    else:
        return abort(405, "Method not allowed!")

@app.route('/api/metrics/averages', methods=['GET'])
def get_average_totals():
    if request.method == "GET":
        data = metricsService.get_average_totals()
        return data
    else:
        return abort(405, "Method not allowed!")

@app.route('/api/metrics/evols', methods=['GET'])
def get_evol_totals():
    if request.method == "GET":
        data = metricsService.get_evol_totals()
        return data
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
                                              latest=False,
                                              download=True)
    file_name = f"{country_code}_data.{request.args['format']}"
    parent_directory = dirname(dirname(abspath(__file__)))
    file_path = os.path.join(parent_directory, 'FrontEnd', file_name)

    print(file_path)

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
                    "Confirmed": values.get("confirmed", 0),
                    "Recovered": values.get("recovered", 0),
                    "Deceased": values.get("deceased", 0),
                    "Active": values.get("active", 0),
                    "Total Confirmed": values.get("total_confirmed", 0),
                    "Total Recovered": values.get("total_recovered", 0),
                    "Total Deceased": values.get("total_deceased", 0),
                })
            mimetype = "text/csv"

    #return send_file(file_path, mimetype=mimetype, attachment_filename=file_path, as_attachment=True)
    #return send_from_directory(directory=pathlib.Path().absolute(), filename=file_path, as_attachment=True)
    return 'Download finished'


# =========================================== NEWS ENDPOINTS ==============================================

@app.route('/api/news', methods=['POST'])
# @require_app_key
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


@app.route('/api/news/page/<int:page>', methods=['GET'])
def get_news_filtered(page):
    search_term = request.args.get('search_term')
    publication = request.args.get('publication')
    data = newsService.get_news_filtered(publication, 10, (page - 1) * 10, search_term)
    return data


# =========================================== ARTICLE ENDPOINTS ==============================================

@app.route('/api/articles', methods=['POST'])
@require_app_key
def add_articles():
    articlesService.addArticles(request.json)
    return jsonify({'status': 1})


@app.route('/api/articles/latest', methods=['GET'])
@app.route('/api/articles/filter/<string:type_>', methods=['GET'])
def get_articles(id_=-1, type_=""):
    if request.method == 'GET':
        if "latest" in request.url_rule.rule:
            data = articlesService.get_articles(
                        id_=-1, type_="",
                        limit=request.args.get("limit", 20),
                        offset=request.args.get("offset", 0))
        elif "filter" in request.url_rule.rule:
            data = articlesService.get_articles(id_=id_,
                                                type_=type_,
                                                limit=request.args.get("limit", 20),
                                                offset=request.args.get("offset", 0))
        return data
    else:
        return abort(405, "Method not allowed!")


@app.route('/api/articles/page/<int:page>', methods=['GET'])
def get_articles_filtered(page):
    search_term = request.args.get('search_term')
    categories = request.args.getlist('categories')
    data = articlesService.get_articles_filtered('', 10, (page - 1) * 10, search_term, categories)
    return data


if __name__ == '__main__':
    app.run(debug=True)
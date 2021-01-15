import csv
import json
import os
from datetime import datetime
from flask import Flask, jsonify, request, make_response, abort, send_file
from Services.metricsService import MetricsService

app = Flask(__name__, static_url_path="")
metricsService = MetricsService()


# ====================================== ERROR CODES ==============================================
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'Error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'Error': 'Resource not found'}), 404)


@app.errorhandler(500)
def not_found(error):
    return make_response(jsonify({'Error': 'Internal server error'}), 500)


# ==================================== METRICS ENDPOINTS ==================================================

@app.route('/api/metrics', methods=['GET'])
def get_all_metrics():
    data = metricsService.get_all_metrics()
    return jsonify(data)


@app.route('/api/metrics', methods=['POST'])
def createMetric():
    metricsService.addMetrics(request.json["items"])
    return jsonify({'status': 1})


@app.route('/api/country/<string:country_code>', methods=['GET'])
@app.route('/api/country/<string:country_code>/latest', methods=['GET'])
def get_country_metrics(country_code):
    if "latest" in request.url_rule.rule:
        data = metricsService.get_country_metrics(country_code, request.args[datetime.now().strftime("%Y-%m-%d")])
    elif request.args.get("date"):
        data = metricsService.get_country_metrics(country_code, request.args["date"])
    else:
        data = metricsService.get_country_metrics(country_code, request.args.get("from", ""), request.args.get("to", ""))
    return data


@app.route('/api/country/<string:country_code>/download', methods=['GET'])
def download_country_metrics(country_code):
    download_format = request.args.get("format")
    if not download_format or download_format.lower() not in ["json", "csv"]:
        abort(400, description="Download format incorrect or not specified! Available formats: CSV, JSON")

    data = metricsService.get_country_metrics(country_code, request.args.get("from", ""), request.args.get("to", ""))
    file_path = f"{country_code}_data.{request.args['format']}"
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
                print(values)
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

    @app.after_request
    def remove_file(response):
        try:
            os.remove(file_path)
        except Exception as error:
            app.logger.error("Error removing or closing downloaded file", error)
        return response
    return send_file(file_path, mimetype=mimetype, attachment_filename=file_path, as_attachment=True)


@app.route('/api/metrics/<int:id>', methods=['PUT'])
def updateMetric(id):
    print("PUT", id, request.json)
    return jsonify({'status': 1})


@app.route('/api/metrics/<int:id>', methods=['DELETE'])
def deleteMetric(id):
    print("DELETE", id)
    return jsonify({'status': 1})


# =========================================== NEWS ENDPOINTS ==============================================

# TODO

# =========================================== GRAPH ENDPOINTS ==============================================


@app.route('/api/graph/serialize', methods=['GET'])
def serialize():
    metricsService.serialize()
    return jsonify({'status': 1})


if __name__ == '__main__':
    app.run(debug=True)

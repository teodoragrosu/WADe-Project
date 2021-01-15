from datetime import datetime

from flask import Flask, jsonify, request, make_response
from Services.metricsService import MetricsService

app = Flask(__name__, static_url_path="")
metricsService = MetricsService()


@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/api/metrics', methods=['GET'])
def getAll():
    print("GET")
    return jsonify({'status': 1})


@app.route('/api/graph/serialize', methods=['GET'])
def serialize():
    metricsService.serialize()
    return jsonify({'status': 1})


@app.route('/api/metrics/<int:id>', methods=['GET'])
def getById(id):
    print("GET ID", id)
    return jsonify({'status': 1})


@app.route('/api/metrics', methods=['POST'])
def createMetric():
    metricsService.addMetrics(request.json["items"])
    return jsonify({'status': 1})

@app.route('/api/metrics/initialValues', methods=['GET'])
def getMetricsInitialValues():
    result = metricsService.get_metrics_initial_values()
    return jsonify(result)

@app.route('/api/country/<string:country_code>', methods=['GET'])
@app.route('/api/country/<string:country_code>/latest', methods=['GET'])
def get_metric(country_code):
    if "latest" in request.url_rule.rule:
        data = metricsService.get_metrics(country_code, request.args[datetime.now().strftime("%Y-%m-%d")])
    elif request.args.get("date"):
        data = metricsService.get_metrics(country_code, request.args["date"])
    else:
        data = metricsService.get_metrics(country_code, request.args.get("from", ""), request.args.get("to", ""))
    return data


@app.route('/api/metrics/<int:id>', methods=['PUT'])
def updateMetric(id):
    print("PUT", id, request.json)
    return jsonify({'status': 1})


@app.route('/api/metrics/<int:id>', methods=['DELETE'])
def deleteMetric(id):
    print("DELETE", id)
    return jsonify({'status': 1})


if __name__ == '__main__':
    app.run(debug=True)

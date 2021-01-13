from flask import Flask, jsonify, abort, request, make_response, url_for
from API.metricsService import MetricsService

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

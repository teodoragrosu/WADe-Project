from flask import Flask, render_template, request, jsonify, redirect
import json
from datetime import datetime
import requests
from flask_cors import CORS

import FrontEnd.statisticsData as sd

localApiPath = 'http://127.0.0.1:5000/api/'
app = Flask(__name__)
CORS(app)

@app.route("/")
@app.route("/news")
def news_list_page():
    return render_template("news_list_page.html")

@app.route("/articles")
def article_list_page():
    return render_template("article_list_page.html")

@app.route("/about")
def about_page():
    return render_template("about_page.html")

@app.route("/statistics")
def statistics_page():
    open('templates/chart_data/line_data.json', 'w').close()
    open('templates/chart_data/pie_data.json', 'w').close()
    today_date = datetime.today().strftime('%Y-%m-%d')

    response = requests.get('http://127.0.0.1:5000/api/countries')
    countries = response.json().keys()
    return render_template("statistics_page.html", today_date=today_date, countries=countries)

@app.route('/statistics', methods=['POST'])
def receive_dates():
    if request.method == "POST":
        with open('templates/chart_data/country_data.json') as json_file:
            json_data = json.load(json_file)

            with open("templates/chart_data/evol_data.json", "w") as data:
                evol_labels, evol_recovered, evol_deceased = sd.evol_chart_data(json_data)
                evol_json = {'date': evol_labels, 'recovered': evol_recovered, 'deceased': evol_deceased}
                json.dump(evol_json, data)

            if len(request.form) == 2:
                print(request.form['start_date'], request.form['end_date'])
                line_dict = sd.line_chart_data(json_data, request.form['start_date'], request.form['end_date'])

                with open("templates/chart_data/line_data.json", "w") as data:
                    json.dump(line_dict, data)

            if len(request.form) == 1:
                pie_dict = sd.pie_chart_data(json_data, request.form['pie_date'])

                with open("templates/chart_data/pie_data.json", "w") as data:
                    json.dump(pie_dict, data)

    return 'Data uploaded'


@app.route('/country_data', methods=['POST', 'GET'])
def country_data():
    if request.method == "POST":
        with open("templates/chart_data/country_data.json", "w") as data:
            data.write(request.form['country_data'])
        sd.save_chart_data()
    if request.method == "GET":
        return render_template("chart_data/country_data.json")

    return "Data uploaded"


@app.route('/line_data')
def line_data():
    return render_template("chart_data/line_data.json")

@app.route('/pie_data')
def pie_data():
    return render_template("chart_data/pie_data.json")

@app.route('/bar_data')
def bar_data():
    return render_template("chart_data/bar_data.json")

@app.route('/evol_data')
def evol_data():
    return render_template("chart_data/evol_data.json")

if __name__ == '__main__':
    app.run(debug=True, port=8000)

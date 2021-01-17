from flask import Flask, render_template, request, jsonify, redirect
import json
from datetime import datetime
import requests
import FrontEnd.statisticsData as sd

app = Flask(__name__)

@app.route("/articles")
def article_list_page():
    return render_template("article_list_page.html")

@app.route("/about")
def about_page():
    return render_template("about_page.html")

@app.route("/statistics")
def statistics_page():
    open('templates/line_data.json', 'w').close()
    open('templates/pie_data.json', 'w').close()
    today_date = datetime.today().strftime('%m/%d/%Y')
    # response = requests.get('http://localhost:5000/api/country/CI')
    # data = response.json()
    # dates = list(data.keys())
    # cases = []
    # for case in data.values():
    #     cases.append(case['active'])
    #
    # return render_template("statistics_page.html",
    #                        today_date=today_date,
    #                        labels=dates,
    #                        values=cases)
    with open('CI_data.json') as json_file:
        json_data = json.load(json_file)

        line_labels, line_values = sd.line_chart_data(json_data)
        pie_labels, pie_values = sd.pie_chart_data(json_data)

        with open("templates/line_data.json", "w") as data:
            line_json = {'line_labels': line_labels, 'line_values': line_values}
            json.dump(line_json, data)

        with open("templates/pie_data.json", "w") as data:
            pie_json = {'pie_labels': pie_labels, 'pie_values': pie_values}
            json.dump(pie_json, data)

    return render_template("statistics_page.html",
                           line_labels=line_labels,
                           line_values=line_values,
                           today_date=today_date,
                           pie_labels=pie_labels,
                           pie_values=pie_values)


@app.route('/statistics', methods=['POST'])
def receive_dates():
    if request.method == "POST":
        with open('CI_data.json') as json_file:
            json_data = json.load(json_file)

            if len(request.form) == 2:
                start_date1, end_date1 = sd.format_date(request.form['start_date1']), sd.format_date(request.form['end_date1'])
                print(start_date1, end_date1)
                line_labels, line_values = sd.line_chart_data(json_data, start_date1, end_date1)

                with open("templates/line_data.json", "w") as data:
                    line_json = {'line_labels': line_labels, 'line_values': line_values}
                    json.dump(line_json, data)

            if len(request.form) == 1:
                stats_date = sd.format_date(request.form['stats_date'])
                pie_labels, pie_values = sd.pie_chart_data(json_data, stats_date)

                with open("templates/pie_data.json", "w") as data:
                    pie_json = {'pie_labels': pie_labels, 'pie_values': pie_values}
                    json.dump(pie_json, data)

    return 'Data uploaded'


@app.route('/line_data')
def line_data():
    return render_template("line_data.json")


@app.route('/pie_data')
def pie_data():
    return render_template("pie_data.json")

if __name__ == '__main__':
    app.run(debug=True, port=8000)

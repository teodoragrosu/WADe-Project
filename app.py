import pathlib
import csv
import pycountry
from flask import (
    Flask,
    render_template,
    request,
    send_from_directory,
    send_file
)
import json
from datetime import datetime
import requests
from flask_cors import CORS

import statisticsData as sd

# localApiPath = "http://127.0.0.1:5000/api/"
PATH = "https://coda-apiv1.herokuapp.com/api"
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
    open("templates/chart_data/line_data.json", "w").close()
    open("templates/chart_data/pie_data.json", "w").close()
    today_date = datetime.today().strftime("%Y-%m-%d")

    response = requests.get(f"https://coda-apiv1.herokuapp.com/api/countries")
    codes = list(response.json().keys())
    names = []
    for code in codes:
        convert = pycountry.countries.get(alpha_2=code)
        if convert != None:
            names.append(convert.name)
        else:
            names.append("")

    countries = dict(zip(codes, names))

    return render_template(
        "statistics_page.html", today_date=today_date, countries=countries
    )


@app.route("/statistics", methods=["POST"])
def receive_dates():
    if request.method == "POST":
        with open("templates/chart_data/country_data.json") as json_file:
            json_data = json.load(json_file)

            with open("templates/chart_data/evol_data.json", "w") as data:
                evol_labels, evol_recovered, evol_deceased = sd.evol_chart_data(
                    json_data
                )
                evol_json = {
                    "date": evol_labels,
                    "recovered": evol_recovered,
                    "deceased": evol_deceased,
                }
                json.dump(evol_json, data)

            if len(request.form) == 2:
                print(request.form["start_date"], request.form["end_date"])
                line_dict = sd.line_chart_data(
                    json_data, request.form["start_date"], request.form["end_date"]
                )

                with open("templates/chart_data/line_data.json", "w") as data:
                    json.dump(dict(sorted(line_dict.items())), data)

            if len(request.form) == 1:
                pie_dict = sd.pie_chart_data(json_data, request.form["pie_date"])

                with open("templates/chart_data/pie_data.json", "w") as data:
                    json.dump(pie_dict, data)

    return "Data uploaded"


@app.route("/country_data", methods=["POST", "GET"])
def country_data():
    if request.method == "POST":
        with open("templates/chart_data/country_data.json", "w") as data:
            data.write(request.form["country_data"])
        sd.save_chart_data()
    if request.method == "GET":
        return render_template("chart_data/country_data.json")

    return "Data uploaded"


@app.route("/download_csv", methods=["GET"])
def download_csv():
    if request.method == "GET":
        code = request.args.get("code")
        file_path = f"{code}_data.csv"

        with open(file_path, "w") as metrics_file:
            data = requests.get(f"https://coda-apiv1.herokuapp.com/api/country/{code}").json()
            writer = csv.DictWriter(metrics_file,
                                    fieldnames=["Date",
                                                "Confirmed",
                                                "Recovered",
                                                "Deceased",
                                                "Active",
                                                "Total_Confirmed",
                                                "Total_Recovered",
                                                "Total_Deceased"])
            writer.writeheader()
            for date, values in data.items():
                writer.writerow({
                    "Date": date,
                    "Confirmed": values.get("confirmed", 0),
                    "Recovered": values.get("recovered", 0),
                    "Deceased": values.get("deceased", 0),
                    "Active": values.get("active", 0),
                    "Total_Confirmed": values.get("total_confirmed", 0),
                    "Total_Recovered": values.get("total_recovered", 0),
                    "Total_Deceased": values.get("total_deceased", 0),
                })
            mimetype = "text/csv"

        return send_file(file_path, mimetype=mimetype, attachment_filename=file_path, as_attachment=True)


@app.route("/download_json", methods=["GET"])
def download_json():
    if request.method == "GET":
        code = request.args.get("code")
        file_path = f"{code}_data.json"

        with open(file_path, "w") as metrics_file:
            data = requests.get(f"https://coda-apiv1.herokuapp.com/api/country/{code}")
            json.dump(json.loads(data.content), metrics_file)
            mimetype = "application/json"

        return send_file(file_path, mimetype=mimetype, attachment_filename=file_path, as_attachment=True)


@app.route("/line_data")
def line_data():
    return render_template("chart_data/line_data.json")


@app.route("/pie_data")
def pie_data():
    return render_template("chart_data/pie_data.json")


@app.route("/bar_data")
def bar_data():
    return render_template("chart_data/bar_data.json")


@app.route("/evol_data")
def evol_data():
    return render_template("chart_data/evol_data.json")


if __name__ == "__main__":
    app.run(debug=True)

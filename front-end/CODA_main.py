from flask import Flask, render_template
import json
from datetime import datetime
import requests
app = Flask(__name__)

@app.route("/articles")
def article_list_page():
    return render_template("article_list_page.html")

@app.route("/about")
def about_page():
    return render_template("about_page.html")

@app.route("/statistics")
def statistics_page():
    today_date = datetime.today().strftime('%d-%m-%Y')
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

        #line chart
        data = json.load(json_file)
        dates = list(data.keys())
        cases = []
        for case in data.values():
            cases.append(case['active'])

        #pie chart
        pie_labels = ['Total recovered', 'Total confirmed', 'Total deceased']
        pie_values = []
        pie_values.append(data[dates[-1]]['total_recovered'])
        pie_values.append(data[dates[-1]]['total_confirmed'])
        pie_values.append(data[dates[-1]]['total_deceased'])

        print (pie_labels,pie_values)

    return render_template("statistics_page.html",
                           line_labels=dates,
                           line_values=cases,
                           today_date=today_date,
                           pie_labels=pie_labels,
                           pie_values=pie_values
                           )

@app.route("/test_article")
def test_article_page():
    return render_template("full_article_page.html")

if __name__ == '__main__':
    app.run(debug=True, port=8000)

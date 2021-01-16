from flask import Flask, render_template
import json
import requests
app = Flask(__name__)

@app.route("/articles")
def article_page():
    return render_template("article_page.html")

@app.route("/about")
def about_page():
    return render_template("about_page.html")

@app.route("/statistics")
def statistics_page():
    with open('templates/data.json') as json_file:
        data = json.load(json_file)
        dates = list(data['BN'].keys())
        cases = []
        for case in data['BN'].values():
            cases.append(case['active'])

    return render_template("statistics_page.html", labels=dates, values=cases)

if __name__ == '__main__':
    app.run(debug=True)

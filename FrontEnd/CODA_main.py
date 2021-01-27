import pathlib

import pycountry
from flask import Flask, render_template, request, jsonify, redirect, send_from_directory
import json
from datetime import datetime
import requests
from flask_cors import CORS

import FrontEnd.statisticsData as sd

apiPath ='https://coda-apiv1.herokuapp.com/api/'
#apiPath = 'http://127.0.0.1:5000/api/'
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
    today_date = datetime.today().strftime('%Y-%m-%d')

    response = requests.get(apiPath + 'countries')
    codes = list(response.json().keys())
    names = []
    for code in codes:
        convert = pycountry.countries.get(alpha_2=code)
        if convert != None:
            names.append(convert.name)
        else:
            names.append('Kosovo')

    countries = dict(zip(codes, names))

    return render_template("statistics_page.html", today_date=today_date, countries=countries)


if __name__ == '__main__':
    app.run(debug=True, port=8000)

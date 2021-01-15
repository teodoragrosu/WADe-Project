from flask import Flask, render_template
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
    return render_template("statistics_page.html")

if __name__ == '__main__':
    app.run(debug=True)
    response = requests.get("http://api.open-notify.org/this-api-doesnt-exist")
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/articles")
def article_page():
    return render_template("article_page.html")

@app.route("/about")
def about_page():
    return render_template("about_page.html")

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask
from scrapers import main

app = Flask(__name__)
data = ""


@app.route("/")
def home():
    return "<p>Hello World!</p>"


@app.route("/get_contests")
def get_contests():
    return main.get_contests()


if __name__ == "__main__":
    app.run(debug=True)

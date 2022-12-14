from flask import Flask
import scraper

app = Flask(__name__)

@app.route("/")
def home():
  return "<p>My first flask app</p>"

@app.route("/get_contests")
def get_contests():
  return scraper.get_contests()

if __name__ == "__main__":
  app.run(debug = True)
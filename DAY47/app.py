from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

NEWS_API_KEY = os.getenv("NEWSKEY")

def fetch_news():
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "country": "us",
        "apiKey": NEWS_API_KEY,
        "pageSize": 10
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("articles", [])
    return []

@app.route("/")
def index():
    articles = fetch_news()
    return render_template("index.html", articles=articles)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

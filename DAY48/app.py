from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def fetch_headlines():
    url = "https://news.ycombinator.com/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        headlines = soup.select(".titleline > a")
        news = []
        for headline in headlines[:10]:
            news.append({
                "title": headline.get_text(),
                "link": headline.get("href")
            })
        return news
    return []

@app.route("/")
def index():
    news = fetch_headlines()
    return render_template("index.html", news=news)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

"""
Headlines - news feeds from several sources
usage: python headlines.py
virtualenv headlines
"""
import feedparser
from flask import Flask
from flask import render_template
from flask import request
import json
import urllib2
import urllib

# create an instance of the Flask object using our module's name as a parameter
app = Flask(__name__)

RSS_FEEDS = {
	'bbc': 'http://feeds.bbci.co.uk/news/rss.xml?edition=us',
	'cnn': 'http://rss.cnn.com/rss/edition.rss%20',
	'abc': 'http://feeds.abcnews.com/abcnews/topstories',
	'nyt': 'http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml'
}

@app.route("/")
def get_news():
	query = request.args.get("publication")
	if not query or query.lower() not in RSS_FEEDS:
		publication = "bbc"
	else:
		publication = query.lower()
	feed = feedparser.parse(RSS_FEEDS[publication])
	weather = get_weather("London,UK")
	return render_template("home.html", articles=feed['entries'], weather=weather)
	#	title=first_article.get("title"),
	#	published=first_article.get("published"),
	#	summary=first_article.get("summary"))

def get_weather(query):
	api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=6e236304b03456fd46d29fa7688aacc2"
	query = urllib.quote(query)
	url = api_url.format(query)
	data = urllib2.urlopen(url).read()
	parsed = json.loads(data)
	weather = None
	if parsed.get("weather"):
		weather = {"description": parsed["weather"][0]["description"],
		"temperature":parsed["main"]["temp"],
		"city":parsed["name"]}
	return weather


if __name__ == '__main__':
	app.run(port=5000, debug=True)
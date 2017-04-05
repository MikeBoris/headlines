import feedparser
from flask import Flask
from flask import render_template
from flask import request

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
	return render_template("home.html", articles=feed['entries'])
	#	title=first_article.get("title"),
	#	published=first_article.get("published"),
	#	summary=first_article.get("summary"))

if __name__ == '__main__':
	app.run(port=5000, debug=True)
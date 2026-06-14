import feedparser

def get_vogue_news():

    feed = feedparser.parse(
        "https://www.vogue.com/feed/rss"
    )

    articles = []

    for item in feed.entries[:8]:

        articles.append({

            "title": item.title,

            "link": item.link

        })

    return articles
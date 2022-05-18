import sqlalchemy.exc
from bayes import NaiveBayesClassifier, label_news
from bottle import redirect, request, route, run, template
from db import News, session
from scraputils import get_news


@route("/news")
def news_list():
    sn = session()
    rows = sn.query(News).filter(News.label == None).all()
    return template("news_template", rows=rows)


@route("/add_label/", method="GET")
def add_label():
    sn = session()
    label = request.GET.get("label", "")
    id = int(request.GET.get("id", ""))
    row = sn.query(News).filter(News.id == id).one()
    row.label = label
    sn.add(row)
    sn.commit()
    redirect("/news")


@route("/update")
def update_news():
    sn = session()
    url = "https://news.ycombinator.com/"
    list = get_news(url)
    for dic in list:
        try:
            row = sn.query(News).filter(News.title == dic["title"]).one()
        except sqlalchemy.exc.NoResultFound:
            new = News(
                title=dic["title"],
                author=dic["author"],
                url=dic["url"],
                comments=dic["comments"],
                points=dic["points"],
            )
            sn.add(new)
            sn.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    label_news()
    redirect("/news")


if __name__ == "__main__":
    run(host="localhost", port=8080)

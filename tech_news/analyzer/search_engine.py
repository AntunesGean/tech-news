import datetime
from tech_news.database import search_news


# Requisito 7
def search_by_title(title):

    search_news_list = []

    for news_one in search_news({"title": {"$regex": title, "$options": "i"}}):
        search_news_list.append((news_one["title"], news_one["url"]))

    return search_news_list


# Requisito 8
def search_by_date(date):

    try:
        date = datetime.date.fromisoformat(date).strftime("%d/%m/%Y")
        search_news_list = []

        for news_one in search_news({"timestamp": date}):
            search_news_list.append((news_one["title"], news_one["url"]))
        return search_news_list

    except ValueError:
        raise ValueError("Data inválida")


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""

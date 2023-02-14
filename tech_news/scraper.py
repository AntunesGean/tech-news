import requests
import time
from parsel import Selector
from tech_news.database import create_news


# Requisito 1
def fetch(url):

    time.sleep(1)
    try:
        response = requests.get(
            url, headers={"user-agent": "Fake user-agent"},
            timeout=3
        )
        if response.status_code != 200:
            return None
        return response.text

    except requests.ReadTimeout:
        return None


# Requisito 2
def scrape_updates(html_content):

    selector = Selector(html_content)
    news = selector.css('h2.entry-title a::attr(href)').getall()
    return news


# Requisito 3
def scrape_next_page_link(html_content):

    selector = Selector(html_content)
    next_url = selector.css("a.next::attr(href)").get()

    if next_url:
        return next_url
    return None


# Requisito 4
def scrape_news(html_content):

    selector = Selector(html_content)
    url = selector.css('link[rel="canonical"]::attr(href)').get()
    title = selector.css("h1.entry-title::text").get().strip()
    timestamp = selector.css("li.meta-date::text").get()
    writer = selector.css(".meta-author .author a::text").get()
    read_time = selector.css(".meta-reading-time::text").re_first(r"\d+")
    summary = selector.xpath("string(//p)").get().strip()
    category = selector.css(".category-style .label::text").get()

    return {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "reading_time": int(read_time),
        "summary": summary,
        "category": category,
    }


# Requisito 5
def get_tech_news(amount):

    URL_BASE = "https://blog.betrybe.com/"
    news = []
    count = 0

    while count < amount:
        response_fetch = fetch(URL_BASE)
        news_list = scrape_updates(response_fetch)

        for news_one in news_list:
            return_fetch = fetch(news_one)
            data = scrape_news(return_fetch)
            news.append(data)
            count += 1

            if count == amount:
                break

        URL_BASE = scrape_next_page_link(response_fetch)

    create_news(news)
    return news

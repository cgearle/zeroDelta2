import requests
from bs4 import BeautifulSoup as parse


# seems that nasdaq and yahoo try to interfere with requests as much as possible, my request were perfectly fine elsewhere
# seems scraping is more trouble than it is worth
# instead start developing with polygon.io as it is free, then move to something better like https://eodhistoricaldata.com when I feel like the app is good enough
# changing apis should not be a problem as I should not work with the raw JSON file, but map to an object instead so there are less points of failure for data stream changes

# TODO: recieve a function for more intricate finds
def scrape(url, tag, html_class, fun):
    try:
        page = requests.get(url)
        parsed = parse(page.content, "html.parser")
        result = parsed.find(tag, class_=html_class)
        return result
    except Exception as e:
        print(e)


def gimmie_contents_as_text(html, tag):
    try:
        return [span.get_text() for span in html.find_all(tag)]
    except Exception as e:
        print(e)

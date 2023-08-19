import requests
from bs4 import BeautifulSoup
from datetime import datetime

link = 'https://news.un.org/en/tags/sdgs'
quote_link = "https://api.quotable.io/quotes/random?limit=3"
date_frmt = "%d %B %Y"
output_frmt = "%d %b"

quotes = {}


def get_blogs():
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'html.parser')
    s = soup.find('div', class_="view-content")
    h = s.find_all('h2', class_="node__title")
    div = s.find_all('div', class_="node__content")
    span = s.find_all('time', class_="datetime")

    a_links = []
    headers = []
    descrip = []
    dates = []
    dt = []

    for h2 in h:
        a_tag = h2.find('a')  # Find the <a> tag within each <h3> element
        if a_tag:
            a_links.append(f"https://news.un.org{a_tag['href']}")
            headers.append(a_tag.text)
    for tag in div:
        p = tag.find('p')
        if p:
            descrip.append(p.text)
    for tag in span:
        if tag:
            txt = tag.text
            frmt_date = datetime.strptime(txt, date_frmt)
            formatted_date = frmt_date.strftime(output_frmt)
            dates.append(formatted_date)

    for i in range(len(a_links)):
        dt.append([headers[i], descrip[i], a_links[i], dates[i]])

    return dt


def get_quote():
    q = requests.get(quote_link)
    q = q.json()
    for i in q:
        quotes[i['content']] = i['author']
    return quotes

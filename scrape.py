import requests
from bs4 import BeautifulSoup
from datetime import datetime

link = 'https://blogs.worldbank.org/search%3Ff%5B0%5D%3Dlanguage%3Aen%26f%5B1%5D%3Dtopic%3A303'
quote_link = "https://api.quotable.io/random"
date_frmt = "%B %d, %Y"
output_frmt = "%d %b"


def get_blogs():
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'html.parser')
    s = soup.find('div', class_="view-content")
    h = s.find_all('h3', class_="field-content")
    div = s.find_all('div', class_="field-content")
    span = s.find_all('span', class_="field-content")

    a_links = []
    headers = []
    descrip = []
    dates = []
    dt = []

    for h3 in h:
        a_tag = h3.find('a')  # Find the <a> tag within each <h3> element
        if a_tag:
            a_links.append(f"https://blogs.worldbank.org{a_tag['href']}")
            headers.append(a_tag.text)
    for tag in div:
        p = tag.find('p')
        if p:
            descrip.append(p.text)
    for tag in span:
        date = tag.find('time')
        if date:
            txt = date.text
            frmt_date = datetime.strptime(txt, date_frmt)
            formatted_date = frmt_date.strftime(output_frmt)
            dates.append(formatted_date)

    for i in range(len(a_links)):
        dt.append([headers[i], descrip[i], a_links[i], dates[i]])

    return dt


def get_quote():
    q = requests.get(quote_link).json()
    return q["content"], q["author"]

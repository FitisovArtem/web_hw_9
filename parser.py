import json

import requests
from bs4 import BeautifulSoup

BASE_URL = 'http://quotes.toscrape.com'
authors_url_list = []
all_pages_list = [BASE_URL]


def get_all_pages(url_site):
    html_doc = requests.get(url_site)
    soup = BeautifulSoup(html_doc.content, 'html.parser')
    try:
        pages = soup.find('li', attrs={'class': 'next'}).find('a')['href']
        next_url = BASE_URL+pages
        all_pages_list.append(next_url)
        get_all_pages(next_url)

    except Exception:
        return True


def parse_data_qoutes(url_page):
    qoutes_list = []
    html_doc = requests.get(url_page)

    if html_doc.status_code == 200:
        soup = BeautifulSoup(html_doc.content, 'html.parser')
        qoutes_div = soup.select('div', attrs={'class': 'col-md-8'})[0].find_all('div', attrs={'class': 'quote'})
        for qoutes in qoutes_div:
            tags = []
            author_ = qoutes.find('small', attrs={'class': 'author'})
            author = author_.text
            a_url = f"{BASE_URL}{author_.find_next_sibling('a')['href']}"
            if a_url not in authors_url_list:
                authors_url_list.append(a_url)

            tags_ = qoutes.find('div', attrs={'class': 'tags'}).find_all('a', attrs={'class': 'tag'})
            for tag in tags_:
                tags.append(tag.text)
            quote = qoutes.find('span', attrs={'class': 'text'}).text[1:-1]
            qoutes_list.append({
                'author': author,
                'tags': tags,
                'quote': quote
            })

    return qoutes_list


def parse_data_authors(url_page):
    authors_list = []
    html_doc = requests.get(url_page)

    if html_doc.status_code == 200:
        soup = BeautifulSoup(html_doc.content, 'html.parser')
        fullname = soup.find('h3', attrs={'class': 'author-title'}).text.replace("-", " ")
        born_date = soup.find('span', attrs={'class': 'author-born-date'}).text
        born_location = soup.find('span', attrs={'class': 'author-born-location'}).text
        description = (soup.find('div', attrs={'class': 'author-description'}).text
                       .replace('\n', "").strip())
        authors_list.append({
            'fullname': fullname,
            'born_date': born_date,
            'born_location': born_location,
            'description': description
        })

    return authors_list


def main():
    get_all_pages(BASE_URL)
    for page in all_pages_list:
        print(page)
        result = parse_data_qoutes(page)
        with open('data/qoutes.json', 'w', encoding='utf-8') as file:
            json.dump(result, file, ensure_ascii=False, indent=2)

        with open('data/authors.json', 'w', encoding='utf-8') as file:
            result = []
            for el in authors_url_list:
                result.append(parse_data_authors(el)[0])
            json.dump(result, file, ensure_ascii=False, indent=2)

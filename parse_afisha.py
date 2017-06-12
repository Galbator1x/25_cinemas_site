import json

import requests
from bs4 import BeautifulSoup


def fetch_movies_urls(movies_count=10):
    afisha_url = 'https://www.afisha.ru/msk/schedule_cinema/'
    afisha_html = requests.get(afisha_url).text
    soup = BeautifulSoup(afisha_html, 'html.parser')
    titles = soup.find_all('h3', class_='usetags')
    return [title.find('a')['href'] for title in titles][:movies_count]


def fetch_movie_info(movie_url):
    movie_html = requests.get(movie_url).text
    soup = BeautifulSoup(movie_html, 'html.parser')
    data_from_script = soup.select('script[type="application/ld+json"]')[0].text
    data_json = json.loads(data_from_script)
    rating = float(data_json.get('aggregateRating', {}).get('ratingValue', 0))
    votes = data_json.get('aggregateRating', {}).get('ratingCount', 0)
    return {'title': data_json['name'], 'description': data_json['description'],
            'genre': data_json['genre'], 'votes': votes, 'url': movie_url,
            'image': data_json['image'], 'rating': rating, 'content': data_json['text']}


def fetch_movies_info():
    return [fetch_movie_info(url) for url in fetch_movies_urls()]

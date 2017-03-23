import json

import requests
from bs4 import BeautifulSoup


def get_movies_urls(movies_count=10):
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
    title = data_json['name']
    description = data_json['description']
    content = data_json['text']
    genre = data_json['genre']
    image = data_json['image']
    rating = float(data_json.get('aggregateRating', {}).get('ratingValue', 0))
    votes = data_json.get('aggregateRating', {}).get('ratingCount', 0)
    return {'title': title, 'description': description,
            'content': content, 'genre': genre, 'image': image,
            'rating': rating, 'votes': votes, 'url': movie_url}


def get_movies_info():
    return [fetch_movie_info(url) for url in get_movies_urls()]

import json
from queue import Queue
from threading import Thread

import requests
from bs4 import BeautifulSoup

import config


def fetch_movies_urls(movies_count=10):
    afisha_url = 'https://www.afisha.ru/msk/schedule_cinema/'
    afisha_html = requests.get(afisha_url).text
    soup = BeautifulSoup(afisha_html, 'html.parser')
    titles = soup.find_all('h3', class_='usetags')
    return [title.find('a')['href'] for title in titles][:movies_count]


def fetch_movie_info_worker(q, movies):
    while not q.empty():
        url = q.get()
        movie_html = requests.get(url).text
        soup = BeautifulSoup(movie_html, 'html.parser')
        data_from_script = soup.select('script[type="application/ld+json"]')[0].text
        data_json = json.loads(data_from_script)
        rating = float(data_json.get('aggregateRating', {}).get('ratingValue', 0))
        votes = data_json.get('aggregateRating', {}).get('ratingCount', 0)
        movies.append({'title': data_json['name'], 'content': data_json['text'],
                       'genre': data_json['genre'], 'votes': votes,
                       'image': data_json['image'], 'rating': rating,
                       'url': url, 'description': data_json['description']})
        q.task_done()


def fetch_movies_info():
    movies = []
    q = Queue()
    [q.put(url) for url in fetch_movies_urls()]
    for _ in range(int(config.THREADS_COUNT)):
        t = Thread(target=fetch_movie_info_worker, args=(q, movies))
        t.start()
    q.join()
    return movies

import json

from flask import Flask, render_template
from parse_afisha import fetch_movies_info
from werkzeug.contrib.cache import SimpleCache

app = Flask(__name__)
app.config.from_object('config')
cache = SimpleCache()


def make_movies_list():
    movies = cache.get('movies')
    if movies is None:
        movies = fetch_movies_info()
        cache.set('movies', movies, timeout=app.config['CACHE_MOVIES_TIMEOUT'])
    return movies


@app.route('/')
def films_list():
    return render_template('films_list.html', movies=make_movies_list())


@app.route('/api/docs')
def api_docs():
    return render_template('api_docs.html')


@app.route('/api/movies')
def get_movies():
    return json.dumps(make_movies_list(), ensure_ascii=False)


if __name__ == '__main__':
    app.run()

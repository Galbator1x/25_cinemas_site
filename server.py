from parse_afisha import get_movies_info

import json

from flask import Flask, render_template
from werkzeug.contrib.cache import SimpleCache

app = Flask(__name__)
app.config.from_object('config')
cache = SimpleCache()


@app.route('/')
def films_list():
    movies = cache.get('movies')
    if movies is None:
        movies = get_movies_info()
        cache.set('movies', movies, timeout=12 * 60 * 60)
    return render_template('films_list.html', movies=movies)


@app.route('/api/docs')
def api_docs():
    return render_template('api_docs.html')


@app.route('/api/movies')
def get_movies():
    movies = cache.get('movies')
    if movies is None:
        movies = get_movies_info()
        cache.set('movies', movies, timeout=12 * 60 * 60)
    return json.dumps(movies, ensure_ascii=False)


if __name__ == "__main__":
    app.run()

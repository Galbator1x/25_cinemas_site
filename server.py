from parse_afisha import get_movies_info

import json
import os

from flask import Flask, render_template
from werkzeug.contrib.cache import SimpleCache

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
cache = SimpleCache()


def get_movies_from_cache():
    movies = cache.get('movies')
    if movies is None:
        movies = get_movies_info()
        cache.set('movies', movies, timeout=12 * 60 * 60)
    return movies


@app.route('/')
def films_list():
    return render_template('films_list.html', movies=get_movies_from_cache())


@app.route('/api/docs')
def api_docs():
    return render_template('api_docs.html')


@app.route('/api/movies')
def get_movies():
    return json.dumps(get_movies_from_cache(), ensure_ascii=False)


if __name__ == "__main__":
    app.run()

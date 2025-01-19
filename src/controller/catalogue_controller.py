import requests
from flask import render_template

OMDB_API_KEY = '773f7b1a'

def search_movies(query):
    url = f"http://www.omdbapi.com/?s={query}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    data = response.json()
    if data.get('Response') == 'True':
        return data['Search']
    else:
        return []

def catalogue_view(request):
    if request.method == 'POST':
        search_query = request.form['search']
        movies = search_movies(search_query)
        return render_template('catalogue.html', movies=movies)
    return render_template('catalogue.html', movies=[])


from models.movie import Movie 
from flask import render_template, request, current_app
import requests

class MovieService:
    @staticmethod
    def search_movies_api(query):
        """Service method to call OMDb API"""
        api_key = current_app.config['OMDB_API_KEY']
        url = f"http://www.omdbapi.com/?s={query}&apikey={api_key}"
        
        try:
            response = requests.get(url)
            data = response.json()
            
            if data.get('Response') == 'True':
                return data.get('Search', [])
            else:
                return []
        except:
            return []
        
    @staticmethod
    def search():
        """Controller method for search route"""
        query = request.args.get('query')
        movies = []
        
        if query:
            movies = MovieService.search_movies_api(query)
            
            for movie in movies:
                existing_movie = Movie.query.filter_by(imdb_id=movie['imdbID']).first()
                movie['already_added'] = existing_movie is not None
            
        return render_template('search.html', movies=movies, query=query)
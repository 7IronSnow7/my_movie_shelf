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
            
            # Debug
            print("API Response:", data)
            
            if data.get('Response') == 'True':
                # return{
                #     'title': data.get('Title', ''),
                #     'year': int(data.get('Year', 0)) if data.get('Year', '').isdigit() else None,
                #     'plot': data.get('Plot', 'No plot available'),
                #     'imdb_rating': float(data.get('imdbRating', 0)) if data.get('imdbRating', 'N/A') != 'N/A' else None,
                #     'poster_url': data.get('Poster', '') if data.get('Poster') != 'N/A' else None
                # }
                # movies = data.get('Search', [])
                # print("Movies found:", len(movies))
                # if movies:
                #     print("First movie:", movies[0])
                #     return movies
                return data.get('Search', [])
            else:
                # print("API Error:", data.get('Error', 'Unknown error'))
                return []
        except:
            # print("Exception:", str(e))
            return []
    
    @staticmethod
    def get_movie_details(imdb_id):
        """Get detailed information about the movie plot"""
        api_key = current_app.config['OMDB_API_KEY']
        url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={api_key}"
        
        try:
            print(f"Making request to: {url}")
            response = requests.get(url)
            print(f"Response status: {response.status_code}")
            
            data = response.json()
            print(f"Detailed API Response for {imdb_id}:", data)
            
            if data.get('Response') == 'True':
                return {
                    'title': data.get('Title', ''),
                    'year': int(data.get('Year', 0)) if data.get('Year', '').isdigit() else None,
                    'plot': data.get('Plot', 'No plot available'),
                    'imdb_rating': float(data.get('imdbRating', 0)) if data.get('imdbRating', 'N/A') != 'N/A' else None,
                    'poster_url': data.get('Poster', '') if data.get('Poster') != 'N/A' else None,
                    'genre': data.get('Genre', ''),
                    'director': data.get('Director', ''),
                    'actors': data.get('Actors', ''),
                    'runtime': data.get('Runtime', '')
                }
            else:
                print(f"API Error for {imdb_id}:", data.get('Error', 'Unknown error'))
                return None
        except Exception as e:
            print(f"Exception getting details for {imdb_id}:", str(e))
            return None
        
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
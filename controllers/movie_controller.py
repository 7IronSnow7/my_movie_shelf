from flask import Blueprint, render_template, request, redirect, url_for, jsonify, current_app
from models.movie import Movie
from models import db
from services.movie_services import MovieService
import requests

movie_bp = Blueprint('movie', __name__)

# Search for a movie
@movie_bp.route('/search')
def search():
    return MovieService.search()

# Add movie to the watch list
@movie_bp.route('/add_movie', methods=['POST'])
def add_movie():
    # Get the form data
    title = request.form.get('title')
    year = request.form.get('year')
    imdb_id = request.form.get('imdb_id')
    
    # Get detailed movie information
    movie_details = MovieService.get_movie_details(imdb_id)
    
    if movie_details:
        movie = Movie(
            title=movie_details['title'],
            year=movie_details['year'],
            imdb_id=imdb_id,
            plot=movie_details['plot'],
            imdb_rating=movie_details['imdb_rating'],
            poster_url=movie_details['poster_url'],
            watched=False
        )
    else:
        # In case API call fails
        movie = Movie(
            title=title,
            year=year,
            imdb_id=imdb_id,
            watched=False
        )
    
    db.session.add(movie)
    db.session.commit()
    return redirect(url_for('movie.search'))

# Checking which movies are on the watchlist
@movie_bp.route('/watchlist')
def watchlist():
    movies = Movie.query.all()
    return render_template('watchlist.html', movies=movies)

# Mark movies as watched
@movie_bp.route('/mark_watched', methods=['POST'])
def mark_watched():
    movie_id = request.form.get('movie_id')
    
    watched_movie = Movie.query.get(movie_id)
    watched_movie.watched = True
    
    db.session.commit()
    return redirect(url_for('movie.watchlist'))

# Remove a movie
@movie_bp.route('/remove_movie', methods=['POST'])
def remove_movie():
    movie_id = request.form.get('movie_id')
    movie = Movie.query.get(movie_id)
    
    db.session.delete(movie)
    db.session.commit()
    
    return redirect(url_for('movie.watchlist'))

@movie_bp.route('/rate_movie_ajax', methods=['POST'])
def rate_movie_ajax():
    movie_id = request.form.get('movie_id')
    rating = request.form.get('rating')
    
    movie = Movie.query.get(movie_id)
    movie.user_rating = int(rating)
    movie.watched = True
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'new_rating': int(rating),
        'movie_id': movie_id
    })

# Keeping old route incase jsonify doesn't work
@movie_bp.route('/rate_movie', methods=['POST'])
def rate_movie():
    movie_id = request.form.get('movie_id')
    rating = request.form.get('rating')
    
    movie = Movie.query.get(movie_id)
    movie.user_rating = int(rating)
    
    db.session.commit()
    return redirect(url_for('movie.watchlist'))
    
@movie_bp.route('/test_api')
def test_api():
    api_key = current_app.config['OMDB_API_KEY']
    
    # Test the exact same movie that works in the example
    test_url = f"http://www.omdbapi.com/?i=tt3896198&apikey={api_key}"
    
    try:
        response = requests.get(test_url)
        data = response.json()
        return f"<pre>{data}</pre>"
    except Exception as e:
        return f"Error: {str(e)}"
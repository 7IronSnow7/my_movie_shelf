from flask import Blueprint, render_template, request, redirect, url_for, jsonify, current_app, flash
from flask_login import login_required, current_user
from models.movie import Movie
from models import db
from services.movie_services import MovieService
import requests

movie_bp = Blueprint('movie', __name__)

# Search for a movie
@movie_bp.route('/search')
@login_required
def search():
    return MovieService.search()

# Add movie to the watch list
@movie_bp.route('/add_movie', methods=['POST'])
def add_movie():
    # Get the form data
    title = request.form.get('title')
    year = request.form.get('year')
    imdb_id = request.form.get('imdb_id')
    imdb_rating = request.form.get('imdb_rating')
    plot = request.form.get('plot')
    user_rating = request.form.get('user_rating')
    poster_url = request.form.get('poster_url')
    
    
    # Get detailed movie information
    movie_details = MovieService.get_movie_details(imdb_id)
    
    if movie_details:
        movie = Movie(
            user_id=current_user.id,
            title=movie_details['title'],
            year=movie_details['year'],
            imdb_id=imdb_id,
            imdb_rating=movie_details['imdb_rating'],
            plot=movie_details['plot'],
            watched=False,
            user_rating=user_rating,
            poster_url=movie_details['poster_url'],
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
    flash(f'Added "{title}" to your watchlist!', 'success')
    return redirect(url_for('movie.search'))

# Checking which movies are on the watchlist
@movie_bp.route('/watchlist')
@login_required
def watchlist():
    movies = Movie.query.all()
    return render_template('watchlist.html', movies=movies)

# Mark movies as watched
@movie_bp.route('/mark_watched', methods=['POST'])
@login_required
def mark_watched():
    movie_id = request.form.get('movie_id')
    
    # Make sure the move belongs to the current user
    movie = Movie.query.filter_by(
        id=movie_id,
        user_id=current_user.id
    ).first()
    
    if movie:
        db.session.delete(movie)
        db.session.commit()
        flash('Movie marked as watched!', 'success')
    else:
        flash('Movie not found!', 'error')
    return redirect(url_for('movie.watchlist'))

# Remove a movie
@movie_bp.route('/remove_movie', methods=['POST'])
@login_required
def remove_movie():
    movie_id = request.form.get('movie_id')
    
    # Make sure the movie belongs to the current user
    movie = Movie.query.filter_by(
        id=movie_id,
        user_id=current_user.id
    ).first()
    
    if movie:
        db.session.delete(movie)
        db.session.commit()
        flash('Movie removed from watchlist!', 'success')
    else:
        flash('Movie not found!', 'error')
    return redirect(url_for('movie.watchlist'))

@movie_bp.route('/rate_movie_ajax', methods=['POST'])
@login_required
def rate_movie_ajax():
    movie_id = request.form.get('movie_id')
    rating = request.form.get('rating')
    
    movie = Movie.query.filter_by(
        id=movie_id,
        user_id=current_user.id
    ).first()
    
    if movie:
        movie.user_rating = int(rating)
        movie.watched = True
        db.session.commit()
    
        return jsonify({
            'success': True,
            'new_rating': int(rating),
            'movie_id': movie_id
        })
    return jsonify({'success': False, 'error': 'Movie not found'})

# Keeping old route incase jsonify doesn't work
@movie_bp.route('/rate_movie', methods=['POST'])
def rate_movie():
    movie_id = request.form.get('movie_id')
    rating = request.form.get('rating')
    
    movie = Movie.query.filter_by(
        id=movie_id,
        user_id=current_user.id
    ).first()
    
    if movie:
        movie.user_rating = int(rating)
        db.session.commit()
        flash('Movie rated successfully!', 'success')
    else:
        flash('Movie not found!', 'error')
        
    return redirect(url_for('movie.watchlist'))
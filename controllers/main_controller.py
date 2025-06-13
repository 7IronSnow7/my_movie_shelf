from flask import Blueprint, render_template
from models.movie import Movie

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    
    total_movies = Movie.query.count()
    watched_movies = Movie.query.filter_by(watched=True).count()
    unwatched_movies = Movie.query.filter_by(watched=False).count()
    
    return render_template('index.html',
                           total_movies=total_movies,
                           watched_movies=watched_movies,
                           unwatched_movies=unwatched_movies)
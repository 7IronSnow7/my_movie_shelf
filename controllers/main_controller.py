from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from models.movie import Movie

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # If user is logged in, show their dashboard
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    else:
        # If not logged in, redirect to login
        return redirect(url_for('auth.login'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    
    total_movies = Movie.query.count()
    watched_movies = Movie.query.filter_by(watched=True).count()
    unwatched_movies = Movie.query.filter_by(watched=False).count()
    
    return render_template('index.html',
                           total_movies=total_movies,
                           watched_movies=watched_movies,
                           unwatched_movies=unwatched_movies,
                           username=current_user.username)
    


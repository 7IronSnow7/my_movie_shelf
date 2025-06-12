from config import Config
from flask import Flask, render_template, request, redirect, url_for
from models import db
from models.movie import Movie
from services.movie_services import MovieService

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize database
    db.init_app(app)

    # create database tables
    with app.app_context():
        db.create_all()
        
    # basic home route
    @app.route('/')
    def home():
        return render_template('index.html')
    
    @app.route('/search')
    def search():
        return MovieService.search()
    
    @app.route('/add_movie', methods=['POST'])
    def add_movie():
        # Get the form data
        title = request.form.get('title')
        year = request.form.get('year')
        imdb_id = request.form.get('imdb_id')
        
        movie = Movie(
            title=title,
            year=year,
            imdb_id=imdb_id,
            watched=False
        )
        
        db.session.add(movie)
        db.session.commit()
        return redirect(url_for('search'))
    
    
    return app

app = create_app()
if __name__ == '__main__':
    app.run(debug=True)
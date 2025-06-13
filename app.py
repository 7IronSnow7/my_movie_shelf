from config import Config
from controllers.main_controller import main_bp
from controllers.movie_controller import movie_bp
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
        
    # Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(movie_bp)
    
    return app

app = create_app()
if __name__ == '__main__':
    app.run(debug=True)
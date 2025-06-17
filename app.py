from config import Config
from controllers.admin_controller import admin_bp
from controllers.auth_controller import auth_bp
from controllers.main_controller import main_bp
from controllers.movie_controller import movie_bp
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager
from models import db
from models.movie import Movie
from services.movie_services import MovieService

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize database
    db.init_app(app)
    
    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        from models.user import User
        return User.query.get(int(user_id))

    # create database tables
    with app.app_context():
        db.create_all()
        
        # Create default users
        from models.user import User
        User.create_default_users()
        
    # Blueprints
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(movie_bp)
    
    print("OMDB API KEY:", app.config.get('OMDB_API_KEY'))
    
    return app

app = create_app()
if __name__ == '__main__':
    app.run(debug=True)
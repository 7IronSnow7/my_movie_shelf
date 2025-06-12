from config import Config
from flask import Flask, render_template
from models import db
from models.movie import Movie

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
        
    return app

app = create_app()
if __name__ == '__main__':
    app.run(debug=True)
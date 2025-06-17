
from models import db
from datetime import datetime, timezone

class Movie(db.Model):
    __tablename__ = 'movies'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer, nullable=True)
    imdb_id = db.Column(db.String(20), nullable=True)
    imdb_rating = db.Column(db.Integer, nullable=True)
    plot = db.Column(db.Text)
    watched = db.Column(db.Boolean, default=False, nullable=False)
    user_rating = db.Column(db.Integer, nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    poster_url = db.Column(db.String(500))
    
    # Foreign key to link movie to user
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __repr__(self):
        return f'<Movie {self.title} ({self.year})>'

from datetime import datetime, timezone
from models import db

class Movie(db.Model):
    __tablename__ = 'movies'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Columns
    title = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=True) 
    watched = db.Column(db.Boolean, default=False, nullable=False)
    imdb_rating = db.Column(db.Float, nullable=True) # 7.8, 8.2 etc
    poster_url = db.Column(db.String(200), nullable=True)
    plot = db.Column(db.String(1000), nullable=True)
    imdb_id = db.Column(db.String(20), nullable=True)
    user_rating = db.Column(db.Integer, nullable=True) # Scale 1 to 5
    notes = db.Column(db.String(500), nullable=True) 
    date_added = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    
    def __repr__(self):
        return f'<Movie {self.title} ({self.year})>'
        

import os
from pathlib import Path

basedir = Path(__file__).parent
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{basedir / "movieshelf.db"}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # OMDB API config
    OMDB_API_KEY = os.environ.get('OMDB_API_KEY') or 'ebfed76c'
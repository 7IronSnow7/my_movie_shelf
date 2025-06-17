from datetime import datetime, timezone
from flask_login import UserMixin
from models import db
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from werkzeug.security import generate_password_hash, check_password_hash
import os

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    
    # Relationship to movies (each user has their own watchlist)
    movies = db.relationship('Movie', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set the user's password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches the hash"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    @classmethod
    def create_default_users(cls):
        """Create default users for demo/development if they don't exist"""
        default_users = [
            {
                "username": "admin",
                "email": "admin@movieshelf.com",
                "password": os.getenv("DEFAULT_ADMIN_PASSWORD", "admin123"),
                "is_admin": True
            },
            {
                "username": "demo",
                "email": "demo@movieshelf.com", 
                "password": os.getenv("DEFAULT_DEMO_PASSWORD", "demo123"),
                "is_admin": False
            }
        ]
        
        created_users = []
        
        for user_data in default_users:
            # Check if user already exists
            existing_user = User.query.filter_by(username=user_data["username"]).first()
            
            if not existing_user:
                # Create new user
                new_user = User(
                    username=user_data["username"],
                    email=user_data["email"],
                    is_admin=user_data["is_admin"]
                )
                new_user.set_password(user_data["password"])
                
                db.session.add(new_user)
                created_users.append(user_data["username"])
        
        if created_users:
            db.session.commit()
            print(f"✅ Created default users: {', '.join(created_users)}")
            print("📋 Default Credentials:")
            for user_data in default_users:
                role = "ADMIN" if user_data["is_admin"] else "USER"
                print(f"   🔑 {user_data['username']} / {user_data['password']} ({role})")
        else:
            print("ℹ️  Default users already exist")
        
        return created_users
# MyMovieShelf

A Flask-based web application for managing your personal movie collection, tracking watched movies, and rating them.

## **Setup Instructions**

### **Prerequisites**
- Python 3.8 or higher
- pip (Python package manager)
- 
### **API Setup**
To fetch movie data (title, plot, poster, etc.), you’ll need a free API key from [OMDb API](https://www.omdbapi.com/apikey.aspx). Add it to your `config.py` as `OMDB_API_KEY`.  
*(Don't worry it's free!)*  

### **Installation**
1. **Fork and download this repository.**
Next, locate the "Fork" button in the top-right corner of this page. Clicking it will create your own copy of the repository. Then, download the files to your development machine by clicking the green "Code" button at the top of the repository page.

<br>**After downloading, unzip the file and extract all contents.**

<br>*I used VSCode as my IDE, but you can use any IDE of your choice.*  


3. **Create a virtual environment:**
    ```bash
   python -m venv venv

4. **Activate the virtual environment:**

Windows:
```bash
  venv\Scripts\activate
```

macOS/Linux:
```bash
bashsource venv/bin/activate
```
-----------------------------------------------------
**Please Note**
If you are having trouble with activating your virtual environment.
Run the command below and then activate your virtual environment again.
```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```
----------------------------------------------------------

5. **Install dependencies:**
```bash
pip install -r requirements.txt
```

6. Run the application and initialize the database:
```bash
python app.py
```
______________________________________________________________________________
The app will automatically create the SQLite database and tables on first run.
Access the application:
Open your browser and navigate to: http://127.0.0.1:5000
______________________________________________________________________________
**Please note** I used SQLite [https://sqlitebrowser.org/dl/] to view my database.

**Default Login Credentials**
**Admin Account:**
<br>Username: admin
<br>Password: admin123

**Demo Account:**
<br>Username: demo
<br>Password: demo123
______________________________________________________________________________
**You can find the passwords in the models/user.py (Line 40 and 46) or .env file.**
______________________________________________________________________________

## App Structure & Functionality
**Core Features**

## Project Structure

```bash
movieshelf/                  # Project root directory
├── controllers/             # Flask blueprints/route handlers
│   └── __pycache__/
├── models/                  # Database models (SQLAlchemy)
│   └── __pycache__/
├── services/                # Business logic layer
│   └── __pycache__/
├── templates/               # Jinja2 templates
│   ├── admin/               # Admin interface templates
│   └── auth/                # Authentication templates
├── venv/                    # Python virtual environment
├── __pycache__/             # Python bytecode cache
├── app.py                   # Main Flask application
├── config.py                # Configuration settings
└── requirements.txt         # Python dependencies
```

### User Features
🎬 **Movie Management**
- Add movies to your personal watchlist
- Remove movies from your collection
- Rate movies (1-5 star rating system)
- View movie details including plot and poster

📊 **Personal Dashboard**
- View your watched movies
- See your ratings history
- Track movies you plan to watch

### Admin Features
👨‍💼 **Administration Panel**
- Manage all users
- Add/remove movies from global database
- Moderate user content
- View system statistics

### Technical Features
🔒 **Authentication System**
- User registration and login
- Password hashing
- Session management

🖼️ **Media Handling**
- Movie poster images
- Responsive design for all devices

## Libraries & Technologies Used**
**Backend**

- Flask - Python web framework
- Flask-SQLAlchemy - Database ORM
- Flask-Login - User session management
- Werkzeug - Password hashing and security
- SQLite - Lightweight database

**Frontend**

- Tailwind CSS - Utility-first CSS framework
- Jinja2 - Template engine (built into Flask)

**Development**

- Python 3.8+ - Programming language

**Development Notes**
MovieShelf is a production-ready Flask application for managing personal movie collections, featuring user authentication, admin controls, and rating systems. 
Built with SQLAlchemy and Jinja2 templates, it's designed for easy deployment while maintaining scalability. 
The clean architecture separates concerns with controllers, services, and models for maintainability.

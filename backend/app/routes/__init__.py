import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from flask import Flask
from flask_cors import CORS
from app.extensions import db, jwt, migrate

def create_app():
    app = Flask(__name__)
    
    # Load config from environment
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-dev-secret')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 86400))
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///airline.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    
    # CORS
    frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:5173')
    CORS(app, origins=[frontend_url], supports_credentials=True)
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.flights import flights_bp
    from app.routes.bookings import bookings_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(flights_bp, url_prefix='/api/flights')
    app.register_blueprint(bookings_bp, url_prefix='/api/bookings')
    
    return app
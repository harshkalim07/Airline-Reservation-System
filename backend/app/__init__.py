from flask import Flask
from flask_cors import CORS
from app.extensions import db, jwt, bcrypt, migrate
from app.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    CORS(app, origins=["http://localhost:5173"])  # Your React app URL
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.flights import flights_bp
    from app.routes.bookings import bookings_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(flights_bp, url_prefix='/api/flights')
    app.register_blueprint(bookings_bp, url_prefix='/api/bookings')
    
    return app
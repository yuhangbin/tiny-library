from flask import Flask
from .database import db
from .routes import book_bp

def create_app(config_object=None):
    app = Flask(__name__)
    
    if config_object:
        app.config.from_object(config_object)
    
    db.init_app(app)
    
    app.register_blueprint(book_bp, url_prefix='/api')
    
    return app 
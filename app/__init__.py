from flask import Flask
from .database import db
from .routes import init_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)

    with app.app_context():
        db.create_all()

    init_routes(app)

    return app 
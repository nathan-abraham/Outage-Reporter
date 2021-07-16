from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Leaflet JS API key
MAPS_API_KEY = ""
DB_NAME = "database.db"
db = SQLAlchemy()
reports = None
find_form_submitted = False
closest_report = None


def create_app():
    global MAPS_API_KEY

    # Initalize Flask Object
    app = Flask(__name__)
    with open("key.txt") as key:
        app.config["SECRET_KEY"] = key.readline()
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
        # Read key
        MAPS_API_KEY = key.readline()

    db.init_app(app)

    from .views import views

    # Register views.py
    app.register_blueprint(views, url_prefix="/")

    create_database(app)

    return app


def create_database(app):
    # If database doesn't already exist, then create it
    if not os.path.exists("website/" + DB_NAME):
        db.create_all(app=app)
        print("Created database")

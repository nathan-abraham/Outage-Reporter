from flask import Flask
import os

# Google maps API key
MAPS_API_KEY = ""

def create_app():
	global MAPS_API_KEY

	# Initalize Flask Object
	app = Flask(__name__)
	with open("key.txt") as key:
		app.config["SECRET_KEY"] = key.readline()
		# Read key
		MAPS_API_KEY = key.readline()

	from .views import views
	
	# Register views.py
	app.register_blueprint(views, url_prefix="/")

	return app
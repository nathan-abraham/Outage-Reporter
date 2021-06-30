from flask import Blueprint, render_template, request
from . import MAPS_API_KEY

# Initialize blueprint
views = Blueprint("views", __name__)

@views.route("/", methods=["GET", "POST"])
def report():
	# Handle post requests
	if request.method == "POST":
		return "testing post request"

	# Render HTML template
	return render_template("report.html")

@views.route("/find", methods=["GET", "POST"])
def find():
	# Render HTML template
	return render_template("find.html", key=MAPS_API_KEY)
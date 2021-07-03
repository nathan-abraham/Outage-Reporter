import json
from flask import Blueprint, render_template, request, redirect, flash, jsonify
from .models import Report
from . import MAPS_API_KEY, db, reports

# Initialize blueprint
views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
def report():
    # Handle post requests
    if request.method == "POST":
        # Get form data
        street_num = request.form.get("streetNum")
        street_name = request.form.get("streetName")
        unit_num = request.form.get("unitNum")
        city = request.form.get("city")
        state = request.form.get("state")
        zip_code = request.form.get("zipCode")
        details = request.form.get("details")

        # Construct report object and add it to database
        try:
            new_report = Report(street_num, street_name, city, state, zip_code, unit_num=unit_num, details=details)
            db.session.add(new_report) 
            db.session.commit()
            flash("Form submitted succesfully.", category="success")
        except:
            flash("There was a problem in submitting the form.", category="error")

        return redirect("/")

    # Render HTML template
    return render_template("report.html")


@views.route("/find", methods=["GET", "POST"])
def find():
    global reports
    # Render HTML template
    return render_template("find.html", key=json.dumps(MAPS_API_KEY), reports=reports)


@views.route("/find-submit", methods=["GET", "POST"])
def find_submit():
    global reports

    # Handle post requests
    if request.method == "POST":
        try:
            # Get data
            city = request.form.get("city")
            zip_code = request.form.get("zipCode")

            # Show success message
            flash("Form submitted succesfully", category="success")
        except:
            # Show error message
            flash("There was a problem in submitting the form.", category="error")
            return redirect("/find")

        # Get matching zip codes
        reports = Report.query.filter_by(zip_code=zip_code).all()
        # reports = Report.query.all()
        print(f"Previous reports: {reports}")

    return redirect("/find") 
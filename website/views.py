import json
from flask import Blueprint, render_template, request, redirect, flash, jsonify
from .models import Report, InvalidAddressError
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
        except InvalidAddressError:
            flash("Invalid Address. Please try again.", category="error") 
        except:
            flash("There was a problem in submitting the form.", category="error")

        return redirect("/")

    # Render HTML template
    return render_template("report.html")


@views.route("/find", methods=["GET", "POST"])
def find():
    global reports
    # Check if reports is emtpy and render HTML template
    not_empty = reports != None and len(reports) > 0
    return render_template("find.html", key=json.dumps(MAPS_API_KEY), reports=reports, not_empty=not_empty)


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
        reports = Report.query.filter_by(city=city).all()
        if not reports:
            flash("No outages found at this location.", category="error")
        # reports = Report.query.all()
        print(f"Previous reports: {reports}")

    return redirect("/find") 
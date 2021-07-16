import json
from flask import Blueprint, render_template, request, redirect, flash, jsonify
from .models import Report, InvalidAddressError, BareReport
from . import MAPS_API_KEY, db, reports, find_form_submitted, closest_report
from geopy import Nominatim
from geopy.distance import geodesic

# Initialize blueprint
views = Blueprint("views", __name__)

def title_case(st):
    return ' '.join(''.join([w[0].upper(), w[1:].lower()]) for w in st.split())

@views.route("/", methods=["GET", "POST"])
def report():
    # Handle post requests
    global find_form_submitted

    find_form_submitted = False

    if request.method == "POST":
        # Get form data
        street_num = request.form.get("streetNum")
        street_name = request.form.get("streetName")
        unit_num = request.form.get("unitNum")
        city = title_case(request.form.get("city")).strip()

        if city == "New York":
            city = "New York City"

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
    return render_template("find.html", key=json.dumps(MAPS_API_KEY), reports=reports, not_empty=not_empty, form_submitted=find_form_submitted, closest_report=closest_report)


@views.route("/find-submit", methods=["GET", "POST"])
def find_submit():
    global reports, find_form_submitted, closest_report

    # Handle post requests
    if request.method == "POST":
        city = ""
        try:
            # Get data
            city = request.form.get("city")
            zip_code = request.form.get("zipCode")

            if city == "New York":
                city = "New York City"

            # Show success message
            flash("Form submitted succesfully", category="success")
            find_form_submitted = True
        except:
            # Show error message
            flash("There was a problem in submitting the form.", category="error")
            return redirect("/find")

        # Get matchingcity names
        reports = Report.query.filter_by(city=city).all()
        if not reports:
            reports = Report.query.filter_by(zip_code=zip_code).all()
            if not reports:
                flash("No outages found at this location.", category="error")

        form_coor = 0, 0
        try:
            form_city = Nominatim(user_agent="myGeocoder").geocode(city)
            form_coor = form_city.latitude, form_city.longitude
        except:
            closest_report = None
            return redirect("/find")

        temp_distance = float("inf")
        for report in reports:
            if report.latitude is None or report.longitude is None:
                continue
            curr_loc = report.latitude, report.longitude
            if geodesic(form_coor, curr_loc).miles < temp_distance:
                closest_report = BareReport(city, report.latitude, report.longitude)



        # reports = Report.query.all()
        print(f"Previous reports: {reports}")

    return redirect("/find") 
import geopy
from geopy import Nominatim
from . import db
from datetime import datetime

class InvalidAddressError(Exception):
	pass

class Report(db.Model):
	# Define fields
	id = db.Column(db.Integer, primary_key=True)
	zip_code = db.Column(db.Integer)
	city = db.Column(db.String(20))
	address = db.Column(db.String(150), nullable=False)
	details = db.Column(db.String(500), nullable=True)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
	latitude = db.Column(db.Float)
	longitude = db.Column(db.Float)

	def __init__(self, street_num, street_name, city, state, zip_code, unit_num="", details=""):
		# Build addres
		self.address = self.build_address(street_num, street_name, city, state, zip_code, unit_num)
		self.zip_code = zip_code
		self.city = city

		# Get coordinates based on address
		self.get_coordinates()
	
	# Build address from separate components
	def build_address(self, street_num, street_name, city, state, zip_code, unit_num):
		return f"{street_num} {street_name}, {city}, {state} {zip_code}"

	def get_coordinates(self):
		locator = Nominatim(user_agent="myGeocoder")
		location = locator.geocode(self.address)

		if location:
			self.latitude = location.latitude
			self.longitude = location.longitude
		else:
			raise InvalidAddressError() 

	# String representation of object for debugging purposes
	def __repr__(self):
		return f"City: {self.city}, Zip Code: {self.zip_code}, Date: {self.date_created}, Details: {self.details}"

class BareReport(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	city = db.Column(db.String(20))
	latitude = db.Column(db.Float)
	longitude = db.Column(db.Float)

	def __init__(self, city, lat, lon):
		self.city = city
		self.latitude = lat
		self.longitude = lon
	

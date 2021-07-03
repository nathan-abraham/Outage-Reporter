from . import db
from datetime import datetime


class Report(db.Model):
	# Define fields
	id = db.Column(db.Integer, primary_key=True)
	zip_code = db.Column(db.Integer)
	city = db.Column(db.String(20))
	address = db.Column(db.String(150), nullable=False)
	details = db.Column(db.String(500), nullable=True)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)

	def __init__(self, street_num, street_name, city, state, zip_code, unit_num="", details=""):
		self.address = self.build_address(street_num, street_name, city, state, zip_code, unit_num)
		self.zip_code = zip_code
		self.city = city
	
	# Build address from separate components
	def build_address(self, street_num, street_name, city, state, zip_code, unit_num):
		return f"{street_num} {street_name}, {city}, {state} {zip_code}"

	# Protect address (which is sensitive information)
	@property
	def get_address(self):
		raise AttributeError("Address is not a readable property")

	# String representation of object for debugging purposed
	def __repr__(self):
		return f"City: {self.city}, Zip Code: {self.zip_code}, Date: {self.date_created}, Details: {self.details}"

from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField, SubmitField, BooleanField, IntegerField, TextField
from wtforms.validators import DataRequired,Email,EqualTo,Length


class Register(FlaskForm):
	name = StringField('Name',[DataRequired(), Length(min=2,max=20)])
	email = StringField('Email',[DataRequired()])
	phone = IntegerField('Phone',[DataRequired()])
	packageID = StringField('Package ID',[DataRequired()])
	seat_num = IntegerField('Number of seats',[DataRequired()])
	password = PasswordField('Password',[DataRequired()])
	confirm_pass = PasswordField('Confirm password',[DataRequired(), EqualTo('password')])
	submit = SubmitField('Book')

class Enquiry(FlaskForm):
	email = StringField('Email',[DataRequired(),Email()])
	password = PasswordField('Password',[DataRequired()])
	login =SubmitField('Login')
	remember = BooleanField('Remember me')

class Feedback(FlaskForm):
	booking_id = StringField('Enter your booking ID',[DataRequired()])
	rating = StringField('Rate your stars here',[DataRequired()])
	review = TextField('Write a brief feeback here')
	done = SubmitField('Done!')

class Admin_login(FlaskForm):
	name = StringField('Name',[DataRequired(), Length(min=2,max=20)])
	email = StringField('Email',[DataRequired()])
	password = PasswordField('Password',[DataRequired()])
	login = SubmitField('Login')

class Add_pack(FlaskForm):
	comp_name = StringField('Company Name',[DataRequired(), Length(min=2,max=20)])
	comp_email = StringField('Company Email',[DataRequired()])
	phone = IntegerField('Phone',[DataRequired()])
	start_loc = StringField('From',[DataRequired()])
	dest_loc = StringField('To',[DataRequired()])
	start_date = StringField('Start date in YYYY/MM/DD',[DataRequired()])
	end_date = StringField('End date in YYYY/MM/DD',[DataRequired()])
	mode = StringField('Mode',[DataRequired()])
	seat_num = IntegerField('Number of seats',[DataRequired()])
	price = IntegerField('Price',[DataRequired()])
	submit = SubmitField('Add package')









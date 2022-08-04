from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from employee_manager.models import User

# add team functionality later
class RegistrationForm(FlaskForm):
	username = StringField('Username', 
		validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email',
		validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	title = StringField('Job title',
		validators=[DataRequired(), Length(min=2, max=50)])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign up')

# function name has to be in this form, and it will be run when validate_on_submit is called from routes.py
	def validate_username(self, username): 
		if User.query.filter_by(username=username.data).first():
			raise ValidationError('username already exists')

	def validate_email(self, email):
		if User.query.filter_by(email=email.data).first():
			raise ValidationError('email already exists')


class LoginForm(FlaskForm):
	email = StringField('Email',
		validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')

	def validate_email(self, email):
		if not User.query.filter_by(email=email.data).first():
			raise ValidationError('email does not exist')
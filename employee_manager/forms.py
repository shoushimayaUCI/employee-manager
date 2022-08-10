from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user

from employee_manager.models import *

# add team functionality later
class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	title = StringField('Job title', validators=[DataRequired(), Length(min=2, max=50)])
	team_id = StringField('Team Id')
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign up')

# function name has to be in this form, and it will be run when validate_on_submit is called from routes.py
	def validate_username(self, username): 
		if User.query.filter_by(username=username.data).first():
			raise ValidationError('username already exists')

	def validate_email(self, email):
		if User.query.filter_by(email=email.data).first():
			raise ValidationError('email already exists')

	def validate_team_id(self, team_id):
		if team_id.data and not Team.query.filter_by(team_id=team_id.data).first():
			raise ValidationError('the team does not exist')


class LoginForm(FlaskForm):
	email = StringField('Email',
		validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')

	def validate_email(self, email):
		if not User.query.filter_by(email=email.data).first():
			raise ValidationError('email does not exist')


class UpdateAccountForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	title = StringField('Job title', validators=[DataRequired(), Length(min=2, max=50)])
	team_id = StringField('Team Id', validators=[DataRequired()])
	picture = FileField('Update Profile Picture', 
		validators=[FileAllowed(['jpg', 'png'])])
	submit = SubmitField('Update')

	def validate_username(self, username):
		if (username.data != current_user.username and 
				User.query.filter_by(username=username.data).first()):
			raise ValidationError('username taken')
	
	def validate_email(self, email):
		if (email.data != current_user.email and 
				User.query.filter_by(email=email.data).first()):
			raise ValidationError('email taken')

	def validate_team_id(self, team_id):
		if not Team.query.filter_by(team_id=team_id.data).first():
			raise ValidationError('the team does not exist')


class NewTaskForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired(), Length(max=50)])
	description = TextAreaField('Description')
	person = StringField('Email of Person You are Assigning to')
	submit = SubmitField('Create')

	def validate_person(self, person):
		if person.data and not User.query.filter_by(email=person.data).first():
			raise ValidationError('there is no user with this email address')


class AnnouncementForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired(), Length(max=50)])
	description = TextAreaField('Description')
	team = StringField('Team to announce it to')
	submit = SubmitField('Create')

	def validate_team(self, team):
		if team.data and not Team.query.filter_by(team_name=team.data).first():
			raise ValidationError('team not found')
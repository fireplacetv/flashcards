from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class SignupForm(FlaskForm):
	first_name = StringField('First name', validators=[DataRequired("Please enter your first name.")])
	last_name = StringField('Last name', validators=[DataRequired("Please enter your last name.")])
	email = StringField('Email', validators=[DataRequired("Please enter your email address."), Email("Please enter your email address.")])
	password = PasswordField('Password', validators=[DataRequired("Please enter a password."), Length(min=6, message="Passwords must be 6 characters or more.")])
	submit = SubmitField('Sign up')

class LoginForm(FlaskForm):
	email=StringField('Email',validators=[DataRequired("Please enter your email address."), Email("Please enter your email address.")])
	password = PasswordField('Password', validators=[DataRequired("Please enter a password.")])
	submit = SubmitField('Sign in')

class AddCardForm(FlaskForm):
	english = StringField('English', validators=[DataRequired("Please enter the english translation.")])
	chinese = StringField('Chinese', validators=[DataRequired("Please enter the chinese translation.")])
	submit = SubmitField("Add")

class EditCardForm(FlaskForm):
	wid = IntegerField('Word ID', validators=[DataRequired("Please enter the word id")])
	oldEnglish = StringField('English', validators=[DataRequired("Please confirm the existing English translation.")])
	oldChinese = StringField('Chinese', validators=[DataRequired("Please confirm the existing Chinese translation.")])
	newEnglish = StringField('English', validators=[DataRequired("Please enter the new English translation.")])
	newChinese = StringField('Chinese', validators=[DataRequired("Please enter the new Chinese translation.")])
	submit = SubmitField("Save")

class DeleteCardForm(FlaskForm):
	wid = IntegerField('Word ID', validators=[DataRequired("Please enter the word id")])
	english = StringField('English', validators=[DataRequired("Please confirm the english translation.")])
	chinese = StringField('Chinese', validators=[DataRequired("Please confirm the chinese translation.")])
	confirm = SubmitField("Delete")
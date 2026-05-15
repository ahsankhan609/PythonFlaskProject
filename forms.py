from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username: StringField = StringField('Username', validators=[
        DataRequired(), Length(min=2, max=20)])

    email: StringField = StringField(
        'Email', validators=[DataRequired(), Email()])

    password: PasswordField = PasswordField('Password', validators=[
        DataRequired(), Length(min=12)])
    confirm_password: PasswordField = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password'), Length(min=12)])

    submit: SubmitField = SubmitField('Sign up!')


class LoginForm(FlaskForm):
    email: StringField = StringField(
        'Email', validators=[DataRequired(), Email()])
    password: PasswordField = PasswordField('Password', validators=[
        DataRequired(), Length(min=12)])
    remember: BooleanField = BooleanField('Remember Me')
    submit: SubmitField = SubmitField('Login')


class FormPostFilesLoginForm(FlaskForm):
    """Demo login form for form_post_files lesson (see form_post_files.py)."""

    email: StringField = StringField(
        'Email', validators=[DataRequired(), Email()])
    password: PasswordField = PasswordField('Password', validators=[
        DataRequired(), Length(min=6, max=128)])
    submit: SubmitField = SubmitField('Login')

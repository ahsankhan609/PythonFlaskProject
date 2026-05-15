# project imports
from flask_wtf import FlaskForm

# third party imports
from wtforms.fields.simple import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    """
    Demo registration form for user sign-up, as used in wtforms_learn.py.

    Fields:
        username: User's display name (2–20 chars).
        email: User's email address (valid format).
        password: User password (min 12 chars).
        confirm_password: Should match 'password' field (min 12 chars).
        submit: Submit button for form submission.

    Example usage in Flask view:
        form = RegistrationForm()
        if form.validate_on_submit():
            # handle successfully registered user, e.g.,
            username = form.username.data
            email = form.email.data
            # ...

    This form validates the presence and correctness of all fields,
    requiring strong passwords and matching confirmation.
    """

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
    """
    Login form for demonstration purposes, as used in wtforms_learn.py.

    Fields:
        email: User's email address (must be valid format).
        password: User password (minimum 12 characters required).
        remember: Checkbox to enable "Remember Me" functionality.
        submit: Submit button to log in.

    Example usage in Flask view:
        form = LoginForm()
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            # handle login logic...

    All fields are required and validated for correct input, enforcing strong passwords.
    """

    email: StringField = StringField(
        'Email', validators=[DataRequired(), Email()])
    password: PasswordField = PasswordField('Password', validators=[
        DataRequired(), Length(min=12)])
    remember: BooleanField = BooleanField('Remember Me')
    submit: SubmitField = SubmitField('Login')


class FormPostFilesLoginForm(FlaskForm):
    """
    Login form used in form_post_files.py for upload authentication demo.

    Fields:
        email: User's email address (must be valid format).
        password: User password (6-128 characters).
        submit: Submit button to log in.

    Example usage in Flask view:
        form = FormPostFilesLoginForm()
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            # handle login logic or file upload authentication
    """

    email: StringField = StringField(
        'Email', validators=[DataRequired(), Email()])
    password: PasswordField = PasswordField('Password', validators=[
        DataRequired(), Length(min=6, max=128)])
    submit: SubmitField = SubmitField('Login')

from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp

USERNAME_PATTERN = r"^[\w\s\-'.]+$"


class RegistrationForm(FlaskForm):
    """Registration form for wtforms_learn (CSRF provided by FlaskForm)."""

    username: StringField = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(min=2, max=20),
            Regexp(
                USERNAME_PATTERN,
                message='Username contains invalid characters.',
            ),
        ],
    )
    email: StringField = StringField(
        'Email',
        validators=[DataRequired(), Email(), Length(max=254)],
    )
    password: PasswordField = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=12, max=128)],
    )
    confirm_password: PasswordField = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.'),
            Length(min=12, max=128),
        ],
    )
    submit: SubmitField = SubmitField('Sign up!')


class LoginForm(FlaskForm):
    """Login form for wtforms_learn (CSRF provided by FlaskForm)."""

    email: StringField = StringField(
        'Email',
        validators=[DataRequired(), Email(), Length(max=254)],
    )
    password: PasswordField = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=12, max=128)],
    )
    remember: BooleanField = BooleanField('Remember Me')
    submit: SubmitField = SubmitField('Login')


class LogoutForm(FlaskForm):
    """CSRF-protected logout (POST only)."""

    submit: SubmitField = SubmitField('Logout')


class FormPostFilesLoginForm(FlaskForm):
    """Demo login form for form_post_files lesson."""

    email: StringField = StringField(
        'Email',
        validators=[DataRequired(), Email(), Length(max=254)],
    )
    password: PasswordField = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=6, max=128)],
    )
    submit: SubmitField = SubmitField('Login')

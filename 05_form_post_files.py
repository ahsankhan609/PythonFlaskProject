from __future__ import annotations

from email_validator.types import ValidatedEmail
import os
import re
import secrets
from typing import Final, TypedDict

from email_validator import EmailNotValidError, validate_email
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

from config import configure_app
from forms import FormPostFilesLoginForm

app = Flask(__name__, template_folder='templates', static_folder='static')
configure_app(app)

MAX_EMAIL_LENGTH: Final = 254
DEMO_EMAIL: Final = 'abc@gmail.com'
DEMO_PASSWORD: Final = 'abc123456789'

_CONTROL_CHARS = re.compile(r'[\x00-\x1f\x7f]')


class IndexFormContext(TypedDict, total=False):
    email: str
    success: bool
    errors: list[str]


def _clean_text(value: str, *, max_length: int) -> str:
    cleaned: str = _CONTROL_CHARS.sub('', value).strip()
    cleaned: str = ' '.join(cleaned.split())
    return cleaned[:max_length]


def _parse_email(raw: str) -> str | None:
    email: str = _clean_text(raw, max_length=MAX_EMAIL_LENGTH)
    if not email:
        return None
    try:
        validated: ValidatedEmail = validate_email(
            email, check_deliverability=False)
    except EmailNotValidError:
        return None
    return validated.normalized


def _credentials_match(email: str, password: str) -> bool:
    """Constant-time check; compare_digest requires ASCII str or use bytes."""
    try:
        email_ok: bool = secrets.compare_digest(
            email.encode('utf-8'),
            DEMO_EMAIL.encode('utf-8'),
        )
        password_ok: bool = secrets.compare_digest(
            password.encode('utf-8'),
            DEMO_PASSWORD.encode('utf-8'),
        )
    except (TypeError, UnicodeEncodeError):
        return False
    return email_ok and password_ok


@app.route('/', methods=['GET', 'POST'])
def index() -> str:
    form: FormPostFilesLoginForm = FormPostFilesLoginForm()
    form_context: IndexFormContext = {}

    if form.validate_on_submit():
        email: str | None = _parse_email(form.email.data or '')
        password: str = form.password.data or ''

        if email is None:
            form_context['errors'] = ['Please enter a valid email address.']
        elif _credentials_match(email, password):
            form_context['email'] = email
            form_context['success'] = True
        else:
            form_context['errors'] = ['Invalid email or password.']
            form_context['email'] = email
    elif request.method == 'POST':
        form_context['errors'] = ['Please correct the errors below.']
        if form.email.data:
            form_context['email'] = _clean_text(
                str(form.email.data), max_length=MAX_EMAIL_LENGTH)

    return render_template(
        '05_form_post_files.html', form=form, form_context=form_context)


# Define the allowed file extensions for images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Folder to store the uploaded files
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Make sure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Helper function to check if the file is an allowed image


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/file_upload', methods=['GET', 'POST'])
def file_upload():
    file_url = None
    file_is_image = False

    if request.method == 'POST':
        # Check if a file is part of the request
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        # If no file is selected
        if file.filename == '':
            return redirect(request.url)

        # If file is selected and it's allowed
        if file and allowed_file(file.filename):
            # Secure the filename and save the file
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Set the URL for the uploaded file
            file_url = url_for('static', filename='uploads/' + filename)
            file_is_image = True
        else:
            # For non-image files, just save the file and show a link
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            file_url = url_for('static', filename='uploads/' + filename)
    return render_template('file_upload.html', file_url=file_url, file_is_image=file_is_image)


# Configure Endpoint
if __name__ == '__main__':
    port = 5555
    url: str = f'http://127.0.0.1:{port}/'
    print(f'\n -> Open: {url}\n')
    # when run on Production make debug = False
    app.run(host='127.0.0.1', port=port, debug=True)

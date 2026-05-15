from __future__ import annotations

import re
from typing import Final, TypedDict

from email_validator import EmailNotValidError, validate_email
from flask import Flask, render_template, request

app = Flask(__name__, template_folder='templates', static_folder='static')

FIELD_FIRST_NAME: Final = 'first_name'
FIELD_EMAIL: Final = 'email'
MAX_NAME_LENGTH: Final = 100
MAX_EMAIL_LENGTH: Final = 254

_CONTROL_CHARS = re.compile(r'[\x00-\x1f\x7f]')


class UserFormData(TypedDict):
    name: str
    email: str


class FormContext(TypedDict, total=False):
    name: str
    email: str
    errors: list[str]


def _clean_text(value: str, *, max_length: int) -> str:
    cleaned = _CONTROL_CHARS.sub('', value).strip()
    cleaned = ' '.join(cleaned.split())
    return cleaned[:max_length]


def _parse_name(raw: str) -> str | None:
    name = _clean_text(raw, max_length=MAX_NAME_LENGTH)
    if not name:
        return None
    if not re.fullmatch(r"[\w\s\-'.]+", name, flags=re.UNICODE):
        return None
    return name


def _parse_email(raw: str) -> str | None:
    email = _clean_text(raw, max_length=MAX_EMAIL_LENGTH)
    if not email:
        return None
    try:
        validated = validate_email(email, check_deliverability=False)
    except EmailNotValidError:
        return None
    return validated.normalized


@app.route('/form', methods=['GET', 'POST'])
def form() -> str:
    form_context: FormContext = {}

    if request.method == 'POST':
        raw_name = request.form.get(FIELD_FIRST_NAME, '')
        raw_email = request.form.get(FIELD_EMAIL, '')

        name = _parse_name(str(raw_name))
        email = _parse_email(str(raw_email))

        errors: list[str] = []
        if name is None:
            errors.append('Please enter a valid first name.')
        if email is None:
            errors.append('Please enter a valid email address.')

        if errors:
            form_context['errors'] = errors
            form_context['name'] = _clean_text(
                str(raw_name), max_length=MAX_NAME_LENGTH)
            form_context['email'] = _clean_text(
                str(raw_email), max_length=MAX_EMAIL_LENGTH)
        else:
            assert name is not None and email is not None
            form_context['name'] = name
            form_context['email'] = email

    return render_template(
        '04_basic_form_data_capture.html', form_context=form_context)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

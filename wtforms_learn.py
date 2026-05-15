from __future__ import annotations

from werkzeug.wrappers.response import Response
import os
from functools import wraps
from typing import Any, Callable, Final, Literal, TypeVar, TypedDict, cast

from flask import Flask, flash, redirect, render_template, session, url_for
from flask_bcrypt import Bcrypt  # type: ignore[import-untyped]
from markupsafe import escape
from werkzeug.wrappers import Response as WerkzeugResponse

from config import configure_app, configure_db
from forms import LoginForm, LogoutForm, RegistrationForm
from models import User, db

app: Flask = Flask(__name__, template_folder='templates',
                   static_folder='static')
configure_app(app)
configure_db(app)

bcrypt: Bcrypt = Bcrypt(app)
db.init_app(app)

with app.app_context():
    db.create_all()

DEFAULT_PORT: Final[Literal[5000]] = 5000
SESSION_EMAIL_KEY: Final[Literal['user_email']] = 'user_email'
SESSION_USERNAME_KEY: Final[Literal['user_username']] = 'user_username'

F = TypeVar('F', bound=Callable[..., Any])


class Post(TypedDict):
    author: str
    title: str
    content: str
    date_posted: str


posts: list[Post] = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018',
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018',
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 3',
        'content': 'Third post content',
        'date_posted': 'April 22, 2018',
    },
]


def is_logged_in() -> bool:
    return SESSION_EMAIL_KEY in session


def login_user(*, email: str, username: str | None, remember: bool) -> None:
    session.clear()
    session[SESSION_EMAIL_KEY] = email
    if username:
        session[SESSION_USERNAME_KEY] = username
    session.permanent = remember


def logout_user() -> WerkzeugResponse:
    session.clear()
    response: Response = redirect(url_for('index'))
    cookie_name: str = str(app.config.get('SESSION_COOKIE_NAME', 'session'))
    cookie_path: str = str(app.config.get('SESSION_COOKIE_PATH', '/'))
    cookie_domain: str | None = app.config.get('SESSION_COOKIE_DOMAIN')
    cookie_samesite: str | None = app.config.get('SESSION_COOKIE_SAMESITE')
    response.delete_cookie(
        cookie_name,
        path=cookie_path,
        domain=str(cookie_domain) if cookie_domain else None,
        samesite=str(cookie_samesite) if cookie_samesite else None,
    )
    return response


def login_required(view: F) -> F:
    @wraps(view)
    def wrapped(*args: Any, **kwargs: Any) -> Any:
        if not is_logged_in():
            flash('Please log in to access that page.', 'warning')
            return redirect(url_for('login'))
        return view(*args, **kwargs)

    return cast(F, wrapped)


def guest_only(view: F) -> F:
    @wraps(view)
    def wrapped(*args: Any, **kwargs: Any) -> Any:
        if is_logged_in():
            return redirect(url_for('dashboard'))
        return view(*args, **kwargs)

    return cast(F, wrapped)


@app.context_processor
def inject_auth_nav() -> dict[str, Any]:
    return {
        'show_auth_nav': True,
        'is_logged_in': is_logged_in(),
        'current_user_email': session.get(SESSION_EMAIL_KEY),
        'current_username': session.get(SESSION_USERNAME_KEY),
        'logout_form': LogoutForm(),
    }


@app.route('/', methods=['GET'])
def index() -> str:
    return render_template(
        'wtforms_learn.html',
        title='WTForms Learning',
        posts=posts,
    )


@app.route('/hello/<username>', methods=['GET'])
def hello(username: str) -> str:
    return f'Greetings: {escape(username)}'


@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard() -> str:
    return render_template(
        'dashboard.html',
        title='Dashboard',
        posts=posts,
        user_email=session.get(SESSION_EMAIL_KEY, ''),
        username=session.get(SESSION_USERNAME_KEY),
    )


@app.route('/register', methods=['GET', 'POST'])
@guest_only
def register() -> WerkzeugResponse | str:
    form: RegistrationForm = RegistrationForm()
    if form.validate_on_submit():
        email: str = (form.email.data or '').strip().lower()
        username: str = (form.username.data or '').strip()

        if User.query.filter_by(email=email).first():
            flash('That email is already registered. Please log in.', 'danger')
            return render_template('register.html', title='WTForms Registration', form=form)

        if User.query.filter_by(username=username).first():
            flash('That username is taken. Please choose another.', 'danger')
            return render_template('register.html', title='WTForms Registration', form=form)

        password_hash: str = bcrypt.generate_password_hash(
            form.password.data or '',
            rounds=int(os.environ.get('BCRYPT_LOG_ROUNDS', '12'))
        ).decode('utf-8')  # type: ignore[assignment]
        user: User = User(username=username, email=email,
                          password_hash=password_hash)
        db.session.add(user)
        db.session.commit()

        login_user(email=email, username=username, remember=False)
        flash(f'Account created for {escape(username)}!', 'success')
        return redirect(url_for('dashboard'))
    return render_template(
        'register.html',
        title='WTForms Registration',
        form=form,
    )


@app.route('/login', methods=['GET', 'POST'])
@guest_only
def login() -> WerkzeugResponse | str:
    form: LoginForm = LoginForm()
    if form.validate_on_submit():
        email: str = (form.email.data or '').strip().lower()
        user: User | None = User.query.filter_by(email=email).first()
        if not user or not bcrypt.check_password_hash(  # type: ignore[no-untyped-call]
            cast(str, user.password_hash), form.password.data or ''
        ):
            flash('Invalid email or password.', 'danger')
            return render_template('login.html', title='WTForms Login', form=form)

        login_user(
            email=email,
            username=user.username,
            remember=bool(form.remember.data),
        )
        flash(f'Logged in as {escape(email)}!', 'success')
        return redirect(url_for('dashboard'))
    return render_template(
        'login.html',
        title='WTForms Login',
        form=form,
    )


@app.route('/logout', methods=['POST'])
def logout() -> WerkzeugResponse:
    form: LogoutForm = LogoutForm()
    if not form.validate_on_submit():
        flash('Invalid logout request.', 'danger')
        return redirect(url_for('index'))
    response: Response = logout_user()
    flash('You have been logged out successfully.', 'info')
    return response


if __name__ == '__main__':
    port: int = int(os.environ.get('FLASK_PORT', str(DEFAULT_PORT)))
    debug: bool = os.environ.get(
        'FLASK_ENV', 'development').lower() != 'production'
    url: str = f'http://127.0.0.1:{port}/'
    print(f'\n  → Open: {url}\n')
    app.run(host='127.0.0.1', port=port, debug=debug)

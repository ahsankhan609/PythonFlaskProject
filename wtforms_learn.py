from werkzeug.wrappers.response import Response
from markupsafe import escape
from flask import Flask, render_template, flash, redirect, url_for

from forms import RegistrationForm, LoginForm

app: Flask = Flask(__name__, template_folder='templates',
                   static_folder='static')

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

posts: list[dict[str, str]] = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'

    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'

    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'

    }
]


@app.route('/', methods=['GET'])
def index() -> str:
    return render_template('wtforms_learn.html', title='WTForms Learning', posts=posts)


@app.route('/hello/<username>', methods=['GET'])
def hello(username: str) -> str:
    return f'Greetings: {escape(username)}'


@app.route('/register', methods=['GET', 'POST'])
def register() -> Response | str:
    form: RegistrationForm = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', title='WTForms Registration', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login() -> Response | str:
    form: LoginForm = LoginForm()
    if form.validate_on_submit():
        flash(f'Logged in as {form.email.data}!', 'success')
    return render_template('login.html', title='WTForms Login', form=form)


if __name__ == '__main__':
    port = 5000
    url: str = f'http://127.0.0.1:{port}/'
    print(f'\n -> Open: {url}\n')
    # when run on Production make debug = False
    app.run(host='127.0.0.1', port=port, debug=True)

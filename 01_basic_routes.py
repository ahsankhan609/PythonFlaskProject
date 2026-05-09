from typing import Literal

from flask import Flask

app = Flask(__name__)


@app.route('/')
def index() -> Literal['<h1>Hello World!</h1>']:
    return '<h1>Hello World!</h1>'


@app.route('/about')
def about() -> Literal['<h1>Hello World!</h1><p>Its about me.</p>']:
    return '<h1>Hello World!</h1><p>Its about me.</p>'


@app.route('/contact')
def contact() -> Literal['<h1>Hello World!</h1><p>Its Contact me.</p>']:
    return '<h1>Hello World!</h1><p>Its Contact me.</p>'


# Configure Endpoint
if __name__ == '__main__':
    # when run on Production make it False
    app.run(host='0.0.0.0', port=5555, debug=True)

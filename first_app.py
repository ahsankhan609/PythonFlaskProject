from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hello World!</h1>'


@app.route('/about')
def about():
    return '<h1>Hello World!</h1><p>Its about me.</p>'


@app.route('/contact')
def contact():
    return '<h1>Hello World!</h1><p>Its Contact me.</p>'


# Configure Endpoint
if __name__ == '__main__':
    # when run on Production make it False
    app.run(host='0.0.0.0', port=5555, debug=True)

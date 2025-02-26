from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hello World!</h1>'


@app.route('/greet/<name>')  # asking for argument in the url
def greet(name):
    return f"hello {name}"


# @app.route('/add/<int:n1>/<int:n2>')  # asking for argument in the url
# def add(n1, n2):
#     return f"{n1} + {n2} = {n1+n2}"

@app.route('/add/<path:numbers>')  # Accepting a path string
def add(numbers: str) -> str:
    """Sums all the numbers passed as arguments in the URL."""
    # Split the input string into a list of numbers and convert them to integers
    try:
        numbers_list = [int(num) for num in numbers.split('/')]
        result = sum(numbers_list)
        return f"Sum of {', '.join(map(str, numbers_list))} = {result}"
    except ValueError:
        return "Please provide valid integer values.Dont use '/' in the end."


# Configure Endpoint
if __name__ == '__main__':
    # when run on Production make it False
    app.run(host='0.0.0.0', port=5555, debug=True)

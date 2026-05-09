from typing import Literal

from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def index() -> Literal['<h1>Hello World!</h1>']:
    return '<h1>Hello World!</h1>'


@app.route('/greet/<name>')  # asking for argument in the url
def greet(name: str) -> str:
    """
    Description: 
    greet user when name is provided

    Args: name(str) - user name is required

    Example:
    >>> http://localhost:5555/greet/<user_name>   
    """
    return f"hello {name}"


# asking for argument in the url
@app.route('/add_2_numbers/<int:n1>/<int:n2>')
def add_2_numbers(n1: int, n2: int) -> str:
    return f"{n1} + {n2} = {n1+n2}"


@app.route('/add_numbers/<path:numbers>')  # Accepting a path string
def add_numbers(numbers: str) -> str:
    """Sums all the numbers passed as arguments in the URL."""
    # Split the input string into a list of numbers and convert them to integers
    try:
        numbers_list: list[int] = [int(num) for num in numbers.split('/')]
        result: int = sum(numbers_list)
        return f"Sum of {', '.join(map(str, numbers_list))} = {result}"
    except ValueError:
        return "Please provide valid integer values.Dont use '/' in the end."


@app.route('/my_route', methods=['GET', 'POST'])
def my_route() -> str:
    # Get query parameters (e.g., ?name=John&age=30)

    # Get 'name' parameter from query string
    name: str | None = request.args.get('name')

    # Get 'age' parameter from query string
    age: str | None = request.args.get('age')

    # Get form data
    if request.method == 'POST':
        # Handle POST request
        return f"This is a POST Request . Name: {name}, Age: {age}"
    else:
        # Return the values in the response when provided in the URL
        return f"This is a Get Request . Name: {name}, Age: {age}"
    # use this URL for example
    # http://localhost:5555/my_route?name=ali&age=42


# Configure Endpoint
if __name__ == '__main__':
    # when run on Production make it False
    app.run(host='0.0.0.0', port=5555, debug=True)

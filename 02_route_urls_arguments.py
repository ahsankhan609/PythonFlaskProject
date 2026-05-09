from typing import Literal

from flask import Flask, redirect, request, url_for
from werkzeug import Response

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index() -> Literal['<h1>Hello World!</h1>']:
    return '<h1>Hello World!</h1>'


@app.route('/greet/<name>', methods=['GET'])  # asking for argument in the url
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
@app.route('/add_2_numbers/<int:n1>/<int:n2>', methods=['GET'])
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


# understanding redirection
@app.route('/student', methods=['GET'])
def student() -> str:
    """
    Description:
    Renders the student home page.

    Example:
    >>> http://localhost:5555/student
    """
    return "Welcome student, to your Home Page."


@app.route('/faculty', methods=['GET'])
def faculty() -> str:
    """
    Description:
    Renders the faculty home page.

    Example:
    >>> http://localhost:5555/faculty
    """
    return "Welcome faculty, to your Home Page."


@app.route('/college/<level>', methods=['GET'])
def college_level(level: str) -> Response | tuple[str, int]:
    """
    Description:
    Redirects to the appropriate home page based on the college level.

    Args:
        level (str): The user role — either 'student' or 'faculty'.

    Example:
    >>> http://localhost:5555/college/student
    >>> http://localhost:5555/college/faculty
    """
    if level == 'student':
        return redirect(url_for('student'))
    elif level == 'faculty':
        return redirect(url_for('faculty'))
    else:
        return f"Unknown level '{level}'. Use 'student' or 'faculty'.", 404


# Configure Endpoint
if __name__ == '__main__':
    # when run on Production make it False
    app.run(host='0.0.0.0', port=5555, debug=True)

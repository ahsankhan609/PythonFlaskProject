from flask import Flask, request

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


@app.route('/my_route', methods=['POST', 'GET'])
def my_route():
    # Get query parameters (e.g., ?name=John&age=30)
    name = request.args.get('name')  # Get 'name' parameter from query string
    age = request.args.get('age')    # Get 'age' parameter from query string

    # Get form data
    if request.method == 'POST':
        # Handle POST request
        return 'This is a POST request'
    else:
        # Return the values in the response
        return f"This is a Get Request . Name: {name}, Age: {age}"
    # use this URL for example
    # http://localhost:5555/my_route?name=ali&age=42


# Configure Endpoint
if __name__ == '__main__':
    # when run on Production make it False
    app.run(host='localhost', port=5555, debug=True)

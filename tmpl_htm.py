from flask import Flask, render_template

app = Flask(__name__, template_folder='templates', static_folder='static')


@app.route('/')
def index():
    pg_content = {
        'greeting': 'Good Morning',
        'name': 'John Smith',
        'my_list': [10, 20, 30, 40, 50]
    }
    return render_template('index.html', content=pg_content)


@app.route('/other')
def other():
    pg_text = '''
    Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
    '''
    return render_template('other.html', content=pg_text)


@app.route('/form')
def form():
    return render_template('form.html')

# creating our custom filter


@app.template_filter('reverse_string')
def reverse_string(s):
    return s[::-1]

# Define the custom filter that bold every 5th word


def bold_every_fifth_word(paragraph):
    words = paragraph.split()
    for i in range(4, len(words), 5):  # Starting from index 4 (5th word)
        words[i] = f'<strong>{words[i]}</strong>'  # Bold the 5th word
    return ' '.join(words)


# Register the filter's with Flask
app.jinja_env.filters['reverse_string'] = reverse_string
app.jinja_env.filters['bold_5th'] = bold_every_fifth_word


# Configure Endpoint
if __name__ == '__main__':
    # when run on Production make it False
    app.run(host='localhost', port=5555, debug=True)

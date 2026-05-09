from typing import Any

from flask import Flask, render_template, request, redirect

app = Flask(__name__, template_folder='templates', static_folder='static')


@app.route('/', methods=['GET'])
def index() -> str:
    pg_content: dict[str, Any] = {
        'greeting': 'Good Morning',
        'name': 'John Smith',
        'my_list': [10, 20, 30, 40, 50, 'Python', 'Jinja2', 'flask', 'djnago', 'wsgi', 'postgresql', 'sqlite']
    }
    return render_template('index.html', content=pg_content)


@app.route('/other', methods=['GET'])
def other() -> str:
    pg_text = '''
    Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
    '''
    return render_template('other.html', content=pg_text)


@app.route('/form', methods=['GET', 'POST'])
def form() -> str:
    user_data = None
    if request.method == 'POST':
        raw_name: str | None = request.form.get('first_name', '').strip()
        raw_email: str | None = request.form.get('email', '').strip()
        if raw_name and raw_email and '@' in raw_email:
            user_data: dict[str, str] = {
                'name': raw_name,
                'email': raw_email,
            }
    return render_template('form.html', context=user_data)

# creating our custom filter


@app.template_filter('reverse_string')
def reverse_string(s: str) -> Any:
    return s[::-1]

# Define the custom filter that bold every 5th word


def bold_every_fifth_word(paragraph: str) -> str:
    words: list[str] = paragraph.split()
    for i in range(4, len(words), 5):  # Starting from index 4 (5th word)
        words[i] = f'<strong>{words[i]}</strong>'  # Bold the 5th word
    return ' '.join(words)


# Register the custom filter's with Flask
app.jinja_env.filters['reverse_string'] = reverse_string
app.jinja_env.filters['bold_5th'] = bold_every_fifth_word


# Configure Endpoint
if __name__ == '__main__':
    # when run on Production make it False
    app.run(host='0.0.0.0', port=5555, debug=True)

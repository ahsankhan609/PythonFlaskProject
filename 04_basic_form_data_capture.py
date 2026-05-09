from flask import Flask, request, render_template

app = Flask(__name__)


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
    return render_template('04_basic_form_data_capture.html', context=user_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

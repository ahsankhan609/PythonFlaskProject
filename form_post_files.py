import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename  # This is the correct import

app = Flask(__name__, template_folder='templates', static_folder='static')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('form_post_files.html')
    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user_data = {
            'email': email,
            'pass': password,
        }
        if email == 'abc@gmail.com' and password == 'abc123':
            return render_template('form_post_files.html', content=user_data)
        else:
            return "Failed"
    else:
        return ""


# Define the allowed file extensions for images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Folder to store the uploaded files
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Make sure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Helper function to check if the file is an allowed image


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/file_upload', methods=['GET', 'POST'])
def file_upload():
    file_url = None
    file_is_image = False

    if request.method == 'POST':
        # Check if a file is part of the request
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        # If no file is selected
        if file.filename == '':
            return redirect(request.url)

        # If file is selected and it's allowed
        if file and allowed_file(file.filename):
            # Secure the filename and save the file
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Set the URL for the uploaded file
            file_url = url_for('static', filename='uploads/' + filename)
            file_is_image = True
        else:
            # For non-image files, just save the file and show a link
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            file_url = url_for('static', filename='uploads/' + filename)
    return render_template('file_upload.html', file_url=file_url, file_is_image=file_is_image)


# Configure Endpoint
if __name__ == '__main__':
    # when run on Production make it False
    app.run(host='localhost', port=5555, debug=True)

# PythonFlaskProject

This a Full Flask Project. From Basics to Advance concepts.

## Jinja2 Template - Documentation

- [Jinja2 - Template Designer Documentation](https://jinja.palletsprojects.com/en/stable/templates/)
- [Jinja2 - Base Template](https://jinja.palletsprojects.com/en/stable/templates/#base-template)
- [Jinja2 - Super Blocks](https://jinja.palletsprojects.com/en/stable/templates/#super-blocks)

- [Jinja2 - Filters](https://jinja.palletsprojects.com/en/stable/templates/#filters)
- [Jinja2 - List of Builtin Filters](https://jinja.palletsprojects.com/en/stable/templates/#builtin-filters)
- [Jinja2 - Variables](https://jinja.palletsprojects.com/en/stable/templates/#variables)
- [Jinja2 - Comments](https://jinja.palletsprojects.com/en/stable/templates/#comments)

- [Jinja2 - List of Control Structures](https://jinja.palletsprojects.com/en/stable/templates/#list-of-control-structures)
- [Jinja2 - Math](https://jinja.palletsprojects.com/en/stable/templates/#math)
- [Jinja2 - Comparisons](https://jinja.palletsprojects.com/en/stable/templates/#comparisons)

## WTForms

- [Documentation](https://wtforms.readthedocs.io/en/3.2.x/)

## Course Resources

- [Flask Tutorial [HINDI] Kritim Yantra](https://www.youtube.com/playlist?list=PL19fiuet8c3mCnEmLne9TkNbPRC95-FCe) 📚 Feb 23, 2025
- [Learning Flask with Julian Nash](https://www.youtube.com/playlist?list=PLF2JzgCW6-YY_TZCmBrbOpgx5pSNBD0_L) 📚 Mar 28, 2019
- [Blueprints & Using Multiple Python Files](https://www.youtube.com/watch?v=WteIH6J9v64) 📚 Nov 19, 2019
- [Flask Blueprints Make Your Apps Modular & Professional](https://www.youtube.com/watch?v=_LMiUOYDxzE) 📚 Apr 24, 2023
- [Organizing Flask Projects: Blueprints and Templates Explained [HINDI]](https://www.youtube.com/watch?v=w6v9A5peQT8) 📚 Nov 20, 2023
- [Flask Blueprint and MySQL: Step-by-Step Integration Tutorial [HINDI]](https://www.youtube.com/watch?v=03ZNhsgnFpk) 📚 Nov 24, 2023

## Learning outcomes

- Setting up a development environment and installing Flask
- Understanding project structure and organizing your code
- Creating dynamic web applications with routing, templates, and static files
- Handling forms, user input, and integrating databases
- Advanced topics: RESTful APIs, testing, deployment, and security

## Project initiation

Initialize with `UV`

```bash
uv init .
```

add requirements to the environment

```bash
uv add -r requirements.txt
```

activate environment - Windows

```bash
.venv\Scripts\activate
```

activate environment - Linux - MacOs

```bash
source .venv/bin/activate
```

sync project

```bash
uv sync
```

## Course Notes

- Flask is a web application framework written in Python.
- It is developed by **Armin Ronacher** who leads an international group of python enthusiasts (POCCO).
- It is based on **WSGI** toolkit and **jinja2** template engine.

### Blueprint mockup

- create `templates` inside each `app`. It is best approach. `app_name->templates->index.html` . See `flask blueprint` for better understanding

```bash
# create blog app with templates folder
mkdir -p blog/templates
```

```bash
# go to templates folder and create index.html file
cd templates && touch index.html
```

```bash
# create following files in blog app
touch __init__.py
touch routes.py
```

```python
# write following code in blog/__init__.py
from flask import Blueprint
blog = Blueprint('blog',__name__, template_folder='templates')
from blog import routes
```

```python
# write following code in blog/routes.py
from blog import blog
from flask import render_template

@blog.route('/blog')
def blog():
    return render_template('index. html')
```

```python
from blog import blog
app.register_blueprint(blog)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)
```

### Adding Static folder

add this to `html.jinja2` template for rendering `tomato.jpg` image from `images folder` in `static folder` in `root` of project of directory

```html
<img
  src="{{ url_for('static', filename='images/tomato.jpg')}}"
  alt="image-description"
  class="img-fluid}"
  style="max-width: 60%; height: 50%"
  loading="lazy}"
/>
```

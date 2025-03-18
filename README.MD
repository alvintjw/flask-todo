# Flask Todo Application

A simple task management application built with Flask and SQLAlchemy. This application allows users to create, read, update, and delete tasks in a clean web interface.

## Features

- Create new tasks
- View all tasks with their creation dates
- Update existing tasks
- Delete tasks
- SQLite database for data persistence

## Getting Started

### Prerequisites

- Python 3.6+
- Flask
- Flask-SQLAlchemy

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/flask-todo-app.git
cd flask-todo-app
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install flask flask-sqlalchemy
```

4. Initialize the database:
```python
# Run these commands in Python shell
from app import db
db.create_all()
```

5. Run the application:
```bash
python app.py
```

6. Open your browser and navigate to `http://localhost:5000`

## SQLAlchemy Reference Guide

### Basic Query Operations

```python
# Get all records from a table
all_tasks = Todo.query.all()

# Get first record
first_task = Todo.query.first()

# Get by primary key
task = Todo.query.get(1)  # Get task with id=1

# Get or 404 (returns item or raises 404 error)
task = Todo.query.get_or_404(task_id)
```

### Filtering Records

```python
# Filter by a condition
filtered_tasks = Todo.query.filter(Todo.content == 'Learn Flask')

# Filter by multiple conditions (AND)
tasks = Todo.query.filter(Todo.content == 'Learn Flask', Todo.id > 5)

# Filter with OR
from sqlalchemy import or_
tasks = Todo.query.filter(or_(Todo.content == 'Learn Flask', Todo.content == 'Learn SQLAlchemy'))

# LIKE query (case-sensitive)
tasks = Todo.query.filter(Todo.content.like('%Flask%'))

# ILIKE query (case-insensitive)
tasks = Todo.query.filter(Todo.content.ilike('%flask%'))
```

### Sorting Records

```python
# Order by single column ascending (default)
tasks = Todo.query.order_by(Todo.date_created)

# Order by single column descending
tasks = Todo.query.order_by(Todo.date_created.desc())

# Order by multiple columns
tasks = Todo.query.order_by(Todo.content, Todo.date_created.desc())
```

### Limiting Results

```python
# Limit number of results
tasks = Todo.query.limit(5)

# Offset (skip first n results)
tasks = Todo.query.offset(5)

# Pagination
page = 2
per_page = 10
tasks = Todo.query.paginate(page=page, per_page=per_page, error_out=False)
```

### Count Records

```python
# Count all tasks
task_count = Todo.query.count()

# Count filtered tasks
count = Todo.query.filter(Todo.content.contains('Flask')).count()
```

### Creating, Updating, Deleting Records

```python
# Create new record
new_task = Todo(content='Learn SQLAlchemy')
db.session.add(new_task)
db.session.commit()

# Create multiple records at once
tasks = [Todo(content='Task 1'), Todo(content='Task 2')]
db.session.add_all(tasks)
db.session.commit()

# Update record
task = Todo.query.get(1)
task.content = 'Updated content'
db.session.commit()

# Delete record
task = Todo.query.get(1)
db.session.delete(task)
db.session.commit()
```

### Rolling Back Changes

```python
# Rollback changes if something goes wrong
try:
    db.session.add(new_task)
    db.session.commit()
except:
    db.session.rollback()
    raise
```

### Relationships (One-to-Many Example)

```python
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    tasks = db.relationship('Todo', backref='category', lazy=True)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
```

## Jinja2 Template Reference Guide

### Basic Syntax

```jinja
{{ variable }}  <!-- Display a variable -->
{% statement %}  <!-- Execute a statement -->
{# This is a comment #}  <!-- Comments -->
```

### Variables and Expressions

```jinja
{{ task.content }}  <!-- Access object attribute -->
{{ users[0].name }}  <!-- Access list item attribute -->
{{ value|default('N/A') }}  <!-- Use default if value is undefined -->
{{ value|length }}  <!-- Get length of string or collection -->
```

### Control Structures

#### If Statements

```jinja
{% if tasks %}
  <!-- Content to show if tasks exist -->
{% elif condition %}
  <!-- Alternative content -->
{% else %}
  <!-- Content to show if tasks don't exist -->
{% endif %}
```

#### For Loops

```jinja
{% for task in tasks %}
  {{ task.content }}
  
  {{ loop.index }}  <!-- Current iteration (1-indexed) -->
  {{ loop.index0 }}  <!-- Current iteration (0-indexed) -->
  {{ loop.first }}  <!-- True if first iteration -->
  {{ loop.last }}  <!-- True if last iteration -->
  {{ loop.length }}  <!-- Number of items -->
  
  {% if not loop.last %},{% endif %}  <!-- Add comma except after last item -->
{% else %}
  <!-- Content to show if tasks is empty -->
{% endfor %}
```

### Template Inheritance

#### Base Template (base.html)

```jinja
<!DOCTYPE html>
<html>
<head>
  <title>{% block title %}Default Title{% endblock %}</title>
  {% block head %}{% endblock %}
</head>
<body>
  <header>
    {% block header %}{% endblock %}
  </header>
  
  <main>
    {% block body %}{% endblock %}
  </main>
  
  <footer>
    {% block footer %}{% endblock %}
  </footer>
</body>
</html>
```

#### Child Template

```jinja
{% extends 'base.html' %}

{% block title %}My Page Title{% endblock %}

{% block head %}
  {{ super() }}  <!-- Include content from parent block -->
  <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
{% endblock %}

{% block body %}
  <h1>Page Content</h1>
{% endblock %}
```

### Including Templates

```jinja
{% include 'header.html' %}  <!-- Include another template -->
{% include 'snippet.html' with context %}  <!-- Include and pass variables -->
```

### Macros (Reusable Template Functions)

#### Defining Macros

```jinja
{% macro render_task(task) %}
  <div class="task">
    <h3>{{ task.content }}</h3>
    <p>Created on: {{ task.date_created }}</p>
  </div>
{% endmacro %}
```

#### Using Macros

```jinja
<!-- In the same file -->
{{ render_task(task) }}

<!-- From a file with macros -->
{% from 'macros.html' import render_task %}
{{ render_task(task) }}
```

### URL Generation

```jinja
<a href="{{ url_for('index') }}">Home</a>
<a href="{{ url_for('update', id=task.id) }}">Update Task</a>
<a href="{{ url_for('static', filename='style.css') }}">CSS</a>
```

### Filters

```jinja
{{ name|capitalize }}  <!-- Capitalize first letter -->
{{ content|trim }}  <!-- Remove whitespace -->
{{ number|round }}  <!-- Round number -->
{{ list|join(', ') }}  <!-- Join list items with separator -->
{{ date|date("YYYY-MM-DD") }}  <!-- Format date -->
{{ html_content|safe }}  <!-- Mark as safe HTML (don't escape) -->
{{ long_text|truncate(100) }}  <!-- Truncate text -->
```

### Assignments

```jinja
{% set variable = 'value' %}
{% set items = [1, 2, 3] %}
{% set dict = {'key': 'value'} %}
```

### Raw Blocks (No Processing)

```jinja
{% raw %}
  {{ This will not be processed }}
{% endraw %}
```


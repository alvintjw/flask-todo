# Import necessary libraries
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize the Flask app
app = Flask(__name__)

# Configure SQLite database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

# Initialize SQLAlchemy with the app
db = SQLAlchemy(app)

# Define the Todo model representing a task in the database
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each task
    content = db.Column(db.String(200), nullable=False)  # Task description (not nullable)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp for task creation
    
    def __repr__(self):
        """
        Returns a string representation of the Todo object.
        Useful for debugging purposes.
        """
        return '<Task %r>' % self.id


# Route: Home page - Display tasks & handle task creation
@app.route('/', methods=['POST', 'GET'])
def index():
    """
    Handles displaying tasks and creating new tasks.
    
    If the request method is POST:
        - Retrieve the new task from the form.
        - Add the new task to the database.
        - Redirect back to the home page.
    
    If the request method is GET:
        - Fetch all tasks from the database ordered by creation date.
        - Render the index.html template with tasks.
    """
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)  # Add new task to the session
            db.session.commit()  # Commit changes to the database
            return redirect('/')  # Redirect to home page
        except:
            return 'There was an issue adding your task'  # Error handling for database failure
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()  # Fetch tasks sorted by creation date
        return render_template('index.html', tasks=tasks)  # Render template with tasks


# Route: Delete a task by ID
@app.route('/delete/<int:id>')
def delete(id):
    """
    Handles deleting a task by its ID.
    
    - Finds the task using the provided ID.
    - Deletes the task from the database.
    - Redirects to the home page.
    """
    task_to_delete = Todo.query.get_or_404(id)  # Fetch the task or return 404 if not found
    
    try:
        db.session.delete(task_to_delete)  # Delete the task
        db.session.commit()  # Commit changes to the database
        return redirect('/')  # Redirect to home page
    except:
        return 'There was a problem deleting that task'  # Error handling for database failure


# Route: Update an existing task
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    """
    Handles updating a task.
    
    If the request method is POST:
        - Retrieve the updated content from the form.
        - Update the task in the database.
        - Redirect to the home page.

    If the request method is GET:
        - Fetch the task by ID.
        - Render the update.html template with task details.
    """
    task = Todo.query.get_or_404(id)  # Fetch the task or return 404 if not found
    
    if request.method == 'POST':
        task.content = request.form['content']  # Update task content
        
        try:
            db.session.commit()  # Commit changes to the database
            return redirect('/')  # Redirect to home page
        except:
            return 'There was an issue updating your task'  # Error handling for database failure
    else:
        return render_template('update.html', task=task)  # Render update template with task details


# Run the Flask app in debug mode (for development only)
if __name__ == '__main__':
    app.run(debug=True)
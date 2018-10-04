from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy #SQLAlchemy is a class that enables Python applications to "talk to" databases. It is able to work with several SQL-based database engines.

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://get-it-done:launchcode101@localhost:8889/get-it-done'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120)) #Creates a property that will map to a column of type VARCHAR(120) in the task table.
    completed = db.Column(db.Boolean) #Creates a property completed that will map to a column of type BOOL, which is actually a TINYINT column with a constraint that it can only hold 0 or 1.

    def __init__(self, name):
        self.name = name
        self.completed = False

@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        task_name = request.form['task']
        new_task = Task(task_name) #To create an instance of our persistent Task class, we use the same syntax as always.
        db.session.add(new_task)#Our ORM system, SQLAlchemy, does not know about our new object until we notify it 
                                #that we want our object to be stored in the database. This is done by calling db.session.add().
                                # A database session can be thought of as a collection of queries to be run all at once, when we ask the database to commit the session.
        db.session.commit() #Our changes and additions to the database aren't actually run against the database until we commit the session.

'''Every class that extends db.Model will have a query property attached to it. This query object contains lots of 
useful methods for querying the database for data from the associate table(s).

Here, Task.query.all() has the net effect of running: SELECT * FROM task

and then taking the results and turning them into a list of Task objects.
'''
    tasks = Task.query.filter_by(completed=False).all()
    completed_tasks = Task.query.filter_by(completed=True).all()
    return render_template('todos.html', title="Get It Done!", tasks=tasks, completed_tasks=completed_tasks)

@app.route('/delete-task', methods=['POST'])
def delete_task():

    task_id = int(request.form['task-id']) #html returns as a string so, convert to int
    task = Task.query.get(task_id) #Calling query.get() will query for the specific object/row by it's primary key.
    task.completed = True
    db.session.add(task)#In order to save the changes to the given object to the database, we need to add and commit.
    db.session.commit()
    return redirect('/') #return user to a view

'''We added this conditional to allow us to import objects and classes from code outside of this file in a way that
 doesn't run the application. In particular, we'll want to import db and Task within a Python shell.

    if __name__ == '__main__':

Without this check, when importing these items in another setting, app.run() would be called, starting up the 
application server. In those situations, we do not want that to happen.
'''
if __name__ == '__main__':
    app.run()
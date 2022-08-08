from urllib import request
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

#Our flask app instance
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://uncle-sam:1234@localhost:5432/todoApp'

#Our database instance
db = SQLAlchemy(app)

class Todo(db.Model):
    __tablename = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'

@app.route('/todos/add', methods=['POST'])
def getUserInput():
    task_descr = request.form.get('description')
    newTask = Todo(description=task_descr)
    db.session.add(newTask)
    db.session.commit()
    return redirect(url_for('index'))



#Execute db transaction
db.create_all()

#Rendering function HTML
@app.route('/')
def index():
    return render_template('index.html', data = Todo.query.all())
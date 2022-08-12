from email.policy import default
import sys
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#Our flask app instance
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://uncle-sam:1234@localhost:5432/todoApp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

#Our database instance
db = SQLAlchemy(app)

migrate = Migrate(app, db)

class Todo(db.Model):
    __tablename = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'


class TodoList(db.Model):
  __tablename__ = 'todolists'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(), nullable=False)
  todos = db.relationship('Todo', backref='list', lazy=True)


# get form request
# @app.route('/todos/create', methods=['POST'])
# def create_todo():
#     description = request.form.get('description')
#     todo = Todo(description=description)
#     db.session.add(todo)
#     db.session.commit()
#     return redirect(url_for('index'))

@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        description =  request.get_json()['description']
        todo = Todo(description=description)
        body['description'] = todo.description
        db.session.add(todo)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        if error : 
          abort(400);
        return jsonify(body)

#get checkbox request
@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
  try:
    completed = request.get_json()['completed']
    todo = Todo.query.get(todo_id)
    todo.completed = completed
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return redirect(url_for('index'))


#get remove request
@app.route('/todos/<todo_id>/delete_todo', methods=['DELETE'])
def deleteTask(todo_id):
  try:
    deleted = request.get_json()['deleted']
    todo = Todo.query.get(todo_id)
    if deleted :
      db.session.delete(todo) 
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return redirect(url_for('index'))

    



#Execute db transaction
db.create_all()

#Rendering function HTML
@app.route('/list/<list_id>')
def get_list_id(list_id):
  return render_template('index.html', data=Todo.query.filter_by(list_id=list_id).order_by('id').all())

@app.route('/')
def index():
  return redirect(url_for('get_list_id', list_id=1))
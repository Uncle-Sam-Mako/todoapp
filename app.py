import sys
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
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

# get form request
# @app.route('/todos/add', methods=['POST'])
# def getUserInput():
#     description = request.form.get('description')
#     todo = Todo(description = description)
#     db.session.add(todo)
#     db.session.commit()
#     return redirect(url_for('index'))


#get json request
@app.route('/todos/add', methods=['POST'])
def getUserInput():
    db_error = False
    body = {}
    try:
        description = request.get_json()['description']
        todo = Todo(description2 = description)
        db.session.add(todo)
        db.session.commit()
        body['description'] = todo.description
    except:
        db_error = True
        db.session.rollback()
        print(sys.exc_info)
    finally:
        db.session.close()
    if not db_error:
        return jsonify(body)
    else : abort(400)




#Execute db transaction
db.create_all()

#Rendering function HTML
@app.route('/')
def index():
    return render_template('index.html', data = Todo.query.all())
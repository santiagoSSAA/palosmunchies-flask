from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from sqlalchemy import URL
import os
import pymysql

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure SQLAlchemy to use pymysql
url_object = URL.create(
    os.environ.get('DB_TYPE'),
    username=os.environ.get('USERNAME'),
    password=os.environ.get('PASSWORD'),
    host=os.environ.get('HOST'),
    database=os.environ.get('DATABASE')
)
app.config['SQLALCHEMY_DATABASE_URI'] = url_object.render_as_string(hide_password=False)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
pymysql.install_as_MySQLdb()
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/')
def index():
    tasks = Todo.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    new_task = Todo(task=task)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    task = Todo.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
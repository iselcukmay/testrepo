from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
# Firstly, copied SQLite and Flask's usage codes and our .db's directory. 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/z003resn/PycharmProjects/Kodlama_Egzersizleri/ToDoApp/todo.db'
db = SQLAlchemy(app)

@app.route('/')
def index():
    todos = ToDo.query.all() 
    return render_template("index.html", todos = todos)

@app.route('/complete/<string:id>')
def complete_todo(id):
   todo = ToDo.query.filter_by(id=id).first()

   todo.complete = not todo.complete

   db.session.commit()

   return redirect(url_for("index"))

@app.route('/add', methods = ["POST"])
def add_to_do():
# Getting title
   title = request.form.get("title")

# Creating the object from ToDo class and getting the title and setting complete as False
# Here we did not give the id because we want it as auto-increment
   new_todo = ToDo( title = title, complete = False)

   db.session.add(new_todo)
   db.session.commit()

   return redirect(url_for("index"))

@app.route('/delete/<string:id>')
def delete_todo(id):
   todo = ToDo.query.filter_by(id=id).first()

   db.session.delete(todo)
   db.session.commit()

   return redirect(url_for("index"))

# Secondly, created a class to create our table inside of our db with the related column names(id,title,complete) 
class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean)
# Here below, db.create_all() creates the needed ones, if anyone of them is created before, it's not changing the created ones before.
if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

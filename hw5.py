import sqlite3
from flask import Flask, url_for, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route('/')
def quest():
    return render_template('quest.html')

@app.route("/stats")
def stat():
    return render_template('index.html')

db = sqlite3.connect('test.db')
cur = db.cursor()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    surname = db.Column(db.Text)
    lang = db.Column(db.Text)
    place = db.Column(db.Text)
    gender = db.Column(db.Text)
    education = db.Column(db.Text)
    age = db.Column(db.Integer)

class Questions(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)

class Answers(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    q1 = db.Column(db.Integer)
    q2 = db.Column(db.Integer)

@app.route('/process', methods=['get'])
def answer_process():
    name = request.args.get('name')
    surname = request.args.get('surname')
    lang = request.args.get('lang')
    place = request.args.get('place')
    gender = request.args.get('gender')
    education = request.args.get('education')
    age = request.args.get('age')

    user = User(
        name=name,
        surname=surname,
        lang=lang,
        place=place,
        age=age,
        gender=gender,
        education=education
    )
    db.session.add(user)
    db.session.commit()

    db.session.refresh(user)

    q1 = request.args.get('q1')
    q2 = request.args.get('q2')
    answer = Answers(
        id=user.id,
        q1=q1,
        q2=q2,
    )
    db.session.add(answer)
    db.session.commit()

    return 'Ok'

if __name__ == "__main__":
    app.run()
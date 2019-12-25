import sqlite3
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import random
random.seed = 23
import pandas as pd

app = Flask(__name__)

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
    q3 = db.Column(db.Integer)
    q4 = db.Column(db.Integer)
    q5 = db.Column(db.Integer)

@app.route('/')
def start():
    return render_template('start.html')

@app.route('/quest')
def quest():
    questions = Questions.query.all()
    return render_template('quest.html', questions=questions)

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
    q3 = request.args.get('q3')
    q4 = request.args.get('q4')
    q5 = request.args.get('q5')

    answer = Answers(
        id=user.id,
        q1=q1,
        q2=q2,
        q3=q3,
        q4=q4,
        q5=q5,
    )
    db.session.add(answer)
    db.session.commit()

    return 'Ok'

@app.route("/stats")
def stats():
    all_info = {}

    age_stats = db.session.query(
        func.avg(User.age),
        func.min(User.age),
        func.max(User.age)
    ).one()
    all_info['Средний возраст'] = age_stats[0]
    all_info['Минимальный возраст'] = age_stats[1]
    all_info['Максимальный возраст'] = age_stats[2]

    all_info['Случайное имя'] = random.choice(db.session.query(User.name).all())

    all_info['Кол-во опрошенных'] = User.query.count()  # SELECT COUNT(age) FROM user

    all_info['Медиана 1-го вопроса'] = db.session.query(func.avg(Answers.q1)).one()[0]
    all_info['Медиана 2-го вопроса'] = db.session.query(func.avg(Answers.q2)).one()[0]
    all_info['Медиана 3-го вопроса'] = db.session.query(func.avg(Answers.q3)).one()[0]
    all_info['Медиана 4-го вопроса'] = db.session.query(func.avg(Answers.q4)).one()[0]
    all_info['Медиана 5-го вопроса'] = db.session.query(func.avg(Answers.q5)).one()[0]

    # SELECT q1 FROM answers
    # all_info['q1_answers'] = db.session.query(Answers.q1).all()
    # all_info['q2_answers'] = db.session.query(Answers.q2).all()

    bar_labels = ('Вопрос 1',
                  'Вопрос 2',
                  'Вопрос 3',
                  'Вопрос 4',
                  'Вопрос 5')

    bar_values = (all_info['Медиана 1-го вопроса'],
                  all_info['Медиана 2-го вопроса'],
                  all_info['Медиана 3-го вопроса'],
                  all_info['Медиана 4-го вопроса'],
                  all_info['Медиана 5-го вопроса'])

    df = pd.DataFrame(all_info)
    df = df.to_html()

    return render_template('results.html', all_info=all_info, df=df, title='Медиана ответов на вопросы', max=5, labels=bar_labels, values=bar_values)

if __name__ == "__main__":
    app.run()
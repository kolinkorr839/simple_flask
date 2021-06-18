#!/bin/python3

from elasticsearch import Elasticsearch
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

import os.path


app = Flask(__name__)
db_file = 'students.sqlite3'
app.config ['SQLALCHEMY_DATABASE_URI'] = "sqlite:///%s" % (db_file)
app.config['SECRET_KEY'] = 'ZtFeSuKxInjvEH72'

db = SQLAlchemy(app)

class students(db.Model):
    id = db.Column('student_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    addr = db.Column(db.String(200))
    pin = db.Column(db.String(10))

    def __init__(self, name, city, addr, pin):
        self.name = name
        self.city = city
        self.addr = addr
        self.pin = pin

@app.route('/db_show_all')
def db_show_all():
    all_data = students.query.all()

    # count = students.query.count()
    count = db.session.query(students).count()

    get_some_data = students.query.filter(students.pin == 94597).limit(2)
    return render_template('db_show_all.html',
        all_students=all_data, count=count,
        get_some_data=get_some_data)


@app.route('/db_new', methods=['GET', 'POST'])
def db_new():
    if request.method == 'POST':
       if not request.form['name'] or not request.form['city'] or not request.form['addr']:
          flash('Please enter all the fields', 'error')
       else:
          student = students(request.form['name'], request.form['city'],
             request.form['addr'], request.form['pin'])

          db.session.add(student)
          db.session.commit()

          flash('Record was successfully added')
          return redirect(url_for('db_show_all'))

    return render_template('db_new.html')

@app.route('/')
def welcome():
    return render_template('index.html')


@app.route('/method', methods=['GET', 'POST'])
def method():
    if request.method == 'GET':
        return 'method is %s' % (request.method,)
    if request.method == 'POST':
        return 'POST method.'


@app.route('/pure_css')
def pure_css():
    return render_template('pure_css.html')


@app.route('/form', methods=['GET', 'POST'])
def test_form():
    name = ''
    if request.method == 'POST' and 'username' in request.form:
        name = request.form.get('username')
    return render_template("form.html", name=name)


@app.route('/bmi', methods=['GET', 'POST'])
def bmi_calculator():
    result = ''
    if (request.method == 'POST' and
      'weight' in request.form and
      'height' in request.form):
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        result = float(weight / height**2)

    return render_template("bmi.html", result=result)


if __name__ == '__main__':
    if not os.path.isfile(db_file):
        db.create_all()
    app.run(debug=True)

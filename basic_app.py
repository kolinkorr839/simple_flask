#!/bin/python3

from elasticsearch import Elasticsearch
from flask import Flask, request, render_template

app = Flask(__name__)


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
    app.run(debug=True)

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

@app.route('/elasticsearch_simple')
def elasticsearch_1():
    es = Elasticsearch(['http://localhost:9200'])
    search_query = {
      "query": {
        "term": {
          "variable.raw": "AUTH_API_MYSQL_PORT"
        }
      }
    }

    result = es.search(index='invision-env', body=search_query)
    for hit in result['hits']['hits']:
        print("%(service)s - %(context)s: %(variable)s" % hit['_source'])
    hits = result['hits']['total']['value']
    return render_template("elasticsearch_simple.html", hits=hits, result=result)


@app.route('/blank')
def blank():
    return render_template('blank.html')


@app.route('/elasticsearch_static')
def elasticsearch_2():
    es = Elasticsearch(['http://localhost:9200'])
    search_query = {
      "query": {
        "term": {
          "variable.raw": "AUTH_API_MYSQL_PORT"
        }
      }
    }

    result = es.search(index='invision-env', body=search_query)
    for hit in result['hits']['hits']:
        print("%(service)s - %(context)s: %(variable)s" % hit['_source'])
    hits = result['hits']['total']['value']
    return render_template("elasticsearch_static.html", hits=hits, result=result)


@app.route('/elasticsearch_dynamic', methods=['GET', 'POST'])
def elasticsearch_3():
    es = Elasticsearch(['http://localhost:9200'])

    variable = ''
    if request.method == 'POST':
        variable = request.form['variable']
    else:
        return render_template("elasticsearch_dynamic.html", hits=0, result=0)

    search_query = {
      "query": {
        "term": {
          "variable.raw": "%s" %(variable)
        }
      }
    }

    result = es.search(index='invision-env', body=search_query)
    for hit in result['hits']['hits']:
        print("%(service)s - %(context)s: %(variable)s" % hit['_source'])
    hits = result['hits']['total']['value']
    return render_template("elasticsearch_dynamic.html", hits=hits, result=result)


if __name__ == '__main__':
    app.run(debug=True)

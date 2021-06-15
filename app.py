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


@app.route('/blank')
def blank():
    return render_template('blank.html')


@app.route('/elasticsearch_simple')
def elasticsearch_1():
    query = {
      "query": {
        "term": {
          "variable.raw": "AUTH_API_MYSQL_PORT"
        }
      }
    }
    return base_elasticsearch(query, 'elasticsearch_simple.html')


@app.route('/elasticsearch_static')
def elasticsearch_2():
    query = {
      "query": {
        "term": {
          "variable.raw": "AUTH_API_MYSQL_PORT"
        }
      }
    }

    return base_elasticsearch(query, 'elasticsearch_static.html')


@app.route('/elasticsearch_dynamic', methods=['GET', 'POST'])
def elasticsearch_3():
    variable = ''
    if request.method == 'POST':
        variable = request.form['variable']
    else:
        return render_template("elasticsearch_dynamic.html", hits=0, result=0)

    query = {
      "query": {
        "term": {
          "variable.simple": "%s" %(variable)
        }
      }
    }

    return base_elasticsearch(query, 'elasticsearch_dynamic.html')


@app.route('/elasticsearch_by_service', methods=['GET', 'POST'])
def elasticsearch_4():
    tier = ''
    variable = ''

    if request.method == 'POST':
        variable = request.form['variable']
        if 'tier_options' in request.form:
            tier = request.form['tier_options']
    else:
        return render_template("elasticsearch_by_service.html", hits=0, result=0)

    query = {
      "query": {
        "bool": {
          "must": [
            {
              "regexp": {
                "context.raw": {
                  "value": ".*%s.*" % (tier)
                }
              }
            },
            {
              "terms": {
                "service.raw": [ "%s" % (variable) ]
              }
            }
          ]
        }
      }
    }

    return base_elasticsearch(query, 'elasticsearch_by_service.html')


def base_elasticsearch(query, template):
    es = Elasticsearch(['http://localhost:9200'])

    print(query)
    result = es.search(index='invision-env', body=query, size=20)
    for hit in result['hits']['hits']:
        print("%(service)s - %(context)s: %(variable)s" % hit['_source'])

    hits = result['hits']['total']['value']
    return render_template(template, hits=hits, result=result)


if __name__ == '__main__':
    app.run(debug=True)

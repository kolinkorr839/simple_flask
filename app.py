#!/bin/python3

from elasticsearch import Elasticsearch
from flask import Flask, request, render_template, g, url_for, redirect
from flask_oidc import OpenIDConnect
from okta import UsersClient

app = Flask(__name__)

# https://bit.ly/2TBcxPY
app.config['OIDC_CLIENT_SECRETS'] = 'client_secrets.json'
app.config['OIDC_COOKIE_SECURE'] = False
app.config['OIDC_CALLBACK_ROUTE'] = '/oidc/callback'
app.config['OIDC_SCOPES'] = ['openid', 'email', 'profile']
app.config['SECRET_KEY'] = 'O2XF7t6gbx7kC6ps'
oidc = OpenIDConnect(app)
okta_client = UsersClient('https://dev-96937983.okta.com', '00ztbmTqSgBGnzcZn3xTt-w6ycmuctp01Z758mlkd7')

@app.before_request
def inject_user_into_each_request():
    if oidc.user_loggedin:
        g.user = okta_client.get_user(oidc.user_getfield('sub'))
    else:
        g.user = None

@app.route('/login')
@oidc.require_login
def login():
    return redirect(url_for('.blank'))

@app.route('/logout')
def logout():
    oidc.logout()
    return redirect(url_for('.blank'))

@app.route('/')
@app.route('/blank')
@oidc.require_login
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
def elasticsearch_static():
    query = {
      "query": {
        "term": {
          "variable.raw": "AUTH_API_MYSQL_PORT"
        }
      }
    }

    return base_elasticsearch(query, 'elasticsearch_static.html')


@app.route('/elasticsearch_by_envar', methods=['GET', 'POST'])
def elasticsearch_by_envar_name():
    variable = ''
    if request.method == 'POST':
        variable = request.form['variable']
    else:
        return render_template("elasticsearch_by_envar.html", hits=0, result=0)

    query = {
      "query": {
        "term": {
          "variable.simple": "%s" %(variable)
        }
      }
    }

    return base_elasticsearch(query, 'elasticsearch_by_envar.html')


@app.route('/elasticsearch_by_value', methods=['GET', 'POST'])
def elasticsearch_by_value():
    tier = ''
    variable = ''

    if request.method == 'POST':
        variable = request.form['variable']
        if 'tier_options' in request.form:
            tier = request.form['tier_options']
    else:
        return render_template("elasticsearch_by_value.html", hits=0, result=0)

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
                "value.raw": [ "%s" % (variable) ]
              }
            }
          ]
        }
      }
    }

    return base_elasticsearch(query, 'elasticsearch_by_value.html')


@app.route('/elasticsearch_by_service', methods=['GET', 'POST'])
def elasticsearch_by_service():
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

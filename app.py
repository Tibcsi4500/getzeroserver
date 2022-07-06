import os
from flask import Flask, render_template, request
from google.cloud.sql.connector import Connector
import sqlalchemy
import pymysql
import urllib.request
import json
import requests  

import databaseCalls as db
import util

app = Flask(__name__)

@app.route('/')
def hello():
    pool = util.getpool()
    with pool.connect() as db_conn:
        entries = db_conn.execute("SELECT * from users;").fetchall()
    result = ""
    for row in entries:
        result += str(row) + "<br>"
    return "<html>" + result + "</html>"

#This function is for looking up models - yes it is
@app.route('/modelsearch/', methods = ['GET', 'POST'])
def modelsearch():
    data = util.getBody()
    try:
        modelid = data['modelid']
    except:
        return "Something went wrong"

    try:
        url = 'https://eprel.ec.europa.eu/api/products/washingmachines2019?_page=1&_limit=25&sort0=onMarketStartDateTS&order0=DESC&sort1=energyClass&order1=DESC'
        result = requests.get(url)
        data_json = json.loads(result.text)
        eprelRegistrationNumber = 0
        
        for hit in data_json['hits']:
            if(hit['modelIdentifier'] == modelid):
                eprelRegistrationNumber = str(hit['eprelRegistrationNumber'])
        url = 'https://eprel.ec.europa.eu/api/products/washingmachines2019/' + eprelRegistrationNumber +'/labels?format=PDF'
        
        if(requests.head(url).status_code == 200):
            return url
        else:
            return "Url not valid"
    except Exception as e:
        return "Exception thrown: \n" + e
    except:
        return "o.O"

@app.route('/checkUser/', methods = ['GET', 'POST'])
def checkUser():
    return db.checkUser()

@app.route('/getChallenge/', methods = ['GET', 'POST'])
def getChallenge():
    return db.getChallenge()

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')
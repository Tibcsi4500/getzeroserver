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
        json_file_path = "./ApplianceJSON/washingmachine.json"
        with open(json_file_path, 'r') as j:
            data_json = json.loads(j.read())
        
        # eprelRegistrationNumber = '0'
        
        for hit in data_json['hits']:
            if(hit['modelIdentifier'] == modelid):
                return 1
            else:
                return 0

    #     url = 'https://eprel.ec.europa.eu/api/products/washingmachines2019/' + str(eprelRegistrationNumber) +'/labels?format=PDF'
        
    #     if(requests.head(url).status_code == 200):
    #         return url
    #     else:
    #         return "Url not valid"
    except Exception as e:
        return "Exception thrown: " + str(e)

@app.route('/checkUser/', methods = ['GET', 'POST'])
def checkUser():
    return db.checkUser()

@app.route('/getChallenge/', methods = ['GET', 'POST'])
def getChallenge():
    return db.getChallenge()

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')
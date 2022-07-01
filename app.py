import os
from flask import Flask, render_template, request
from google.cloud.sql.connector import Connector
import sqlalchemy
import pymysql
import urllib.request
import json
import requests  

app = Flask(__name__)
connector = Connector()
#asdasd
#here is another comment
def getconn() -> pymysql.connections.Connection:
    conn: pymysql.connections.Connection = connector.connect(
        "turnkey-banner-354610:europe-west6:example",
        "pymysql",
        user="root",
        password="root",
        db="getzero"
    )
    return conn

def getpool():
    pool = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=getconn,
    )
    return pool

@app.route('/')
def hello():
    pool = getpool()
    with pool.connect() as db_conn:
        entries = db_conn.execute("SELECT * from users;").fetchall()
    result = ""
    for row in entries:
        result += str(row) + "<br>"
    return "<html>" + result + "</html>"

@app.route('/check_user/', methods = ['GET', 'POST'])
def check():
    if (request.method == 'GET'):
        return 'Get'
    elif (request.method == 'POST'):
        data = request.form

        try:
            name = data['name']
            password = data['password']

            pool = getpool()
            with pool.connect() as db_conn:
                SQL = sqlalchemy.text("SELECT 1 AS truth FROM users WHERE users.name = :name AND users.password = :password;")
                is_user = db_conn.execute(SQL, name = name, password = password)

                for row in is_user:
                    return "1"
                return "0"
        except Exception as e:
            return str(e)
        return "Something went wrong"

#This function is for looking up models
@app.route('/modelsearch/', methods = ['GET', 'POST'])
def modelsearch():
    if (request.method == 'GET'):
        return 'Get'
    elif (request.method == 'POST'):
        data = request.form
        modelid = data['modelid']
    
    url = 'https://eprel.ec.europa.eu/api/products/washingmachines2019?_page=1&_limit=25&sort0=onMarketStartDateTS&order0=DESC&sort1=energyClass&order1=DESC'
    result = requests.get(url)
    data_json = json.loads(result.text)
    eprelRegistrationNumber = 0

    try:
        for hit in data_json['hits']:
            if(hit['modelIdentifier'] == modelid):
                eprelRegistrationNumber = hit['eprelRegistrationNumber']
        
        url = 'https://eprel.ec.europa.eu/api/products/washingmachines2019/' + eprelRegistrationNumber +'/labels?format=PDF'
        if(requests.head(url).status_code == 200):
            return url
        else:
            return "Failed"        
    except:
        return "Except"
# def appl():
#     if (request.method == 'GET'):
#         modelid = "WM14URHSPL"
#         index = "washingEfficiencyIndexV2"
#     elif (request.method == 'POST'):
#         modelid = request.form['prod'] #WM14URHSPL
#         index = request.form['password'] # washingEfficiencyIndexV2
#     url = 'https://eprel.ec.europa.eu/api/products/washingmachines2019?_page=1&_limit=25&sort0=onMarketStartDateTS&order0=DESC&sort1=energyClass&order1=DESC'
#     result = requests.get(url)

#     data_json = json.loads(result.text)

#     try:
#         for hit in data_json['hits']:
#             if(hit['modelIdentifier'] == modelid):
#                 return str(hit[index])
#         return "Failed"
#     except:
#         return "Failed"

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')

#THIS COMMENT WAS MADE BY JACK
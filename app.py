import os
from flask import Flask, render_template, request
#from google.cloud.sql.connector import Connector
#import sqlalchemy
#import pymysql
import urllib.request
import json
import requests  

#import databaseCalls as db
import placeholderCalls as db
import util

from pathlib import Path

import io

from cairosvg import svg2png

app = Flask(__name__)

# @app.route('/')
# def hello():
#     pool = util.getpool()
#     with pool.connect() as db_conn:
#        entries = db_conn.execute("SELECT * from users;").fetchall()
#    result = ""
#    for row in entries:
#        result += str(row) + "<br>"
#    return "<html>" + result + "</html>"

@app.route('/')
def hello():
	return "Hi!"


#This function is for looking up models - yes it is
@app.route('/modelsearch/', methods = ['GET', 'POST'])
def modelsearch():
    data = util.getBody()
    try:
        modelid = data['modelIdentifier']
    except:
        return "Something went wrong"

    try:
        json_file_path = "./ApplianceJSON/washingmachine.json"
        with open(json_file_path, 'r') as j:
            data_json = json.loads(j.read())

        model = {}
        
        for hit in data_json['hits']:
            if(hit['modelIdentifier'] == modelid):
                model = hit
        
        if model != {}:
            return model
        else:
            return str(len(data_json['hits']))
    except Exception as e:
        return "Exception thrown: " + str(e)

@app.route('/checkUser/', methods = ['GET', 'POST'])
def checkUser():
    return db.checkUser()

@app.route('/getAcceptedChallengesOfUser/', methods = ['GET', 'POST'])
def getAcceptedChallengesOfUser():
    return db.getAcceptedChallengesOfUser()

@app.route('/incrementChallengeProgress/', methods = ['GET', 'POST'])
def incrementChallengeProgress():
    return db.incrementChallengeProgress()

@app.route('/getUnacceptedChallengesOfUser/', methods = ['GET', 'POST'])
def getUnacceptedChallengesOfUser():
    return db.getUnacceptedChallengesOfUser()

@app.route('/acceptChallengesOfUser/', methods = ['GET', 'POST'])
def acceptChallengesOfUser():
    return db.acceptChallengesOfUser()

@app.route('/lookupid/', methods = ['GET', 'POST'])
def lookup():
    data = util.getBody()
    print(str(data))
    try:
        typetext = data['type']
        modelid = data['modelid']
        path = Path(str(typetext) + ".json")
        print(path)
        jsonfile = open(path)
        response = jsonfile.read()
        data = json.loads(response)
        for hit in data['hits']:
            if(hit['modelIdentifier'] == str(modelid)):
                return hit
        return "Model ID not found"
    except Exception as e:
        return "Something went wrong:" + str(e)


@app.route('/getimage/', methods = ['GET', 'POST'])
def getimage():
    data = util.getBody()

    try:
        eprelid = data['eprelid']
        url = 'https://eprel.ec.europa.eu/label/Label_' + str(eprelid) + '.svg'
        svg = requests.get(url).text
        filelike = io.StringIO()
        imgstream = open("temp_img.png", "rb")
        svg2png(bytestring = svg, write_to = "temp_img.png")
        b = bytearray(imgstream.read())
        return bytearray(b)
    except Exception as e:
        return "Something went wrong: " + str(e)
    return "Something went wrong"

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '4050')
    app.run(debug=False, port=server_port, host='0.0.0.0')
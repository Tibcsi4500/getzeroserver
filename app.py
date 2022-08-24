import os
from flask import Flask, render_template, request
#from google.cloud.sql.connector import Connector
#import sqlalchemy
#import pymysql
#import databaseCalls as db
import placeholderCalls as db
import eprelCalls as eprel

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hi!"

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

@app.route('/lookupmodel/', methods = ['GET', 'POST'])
def lookup():
    return eprel.lookup()

@app.route('/getimage/', methods = ['GET', 'POST'])
def getimage():
    return eprel.getimage()

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '4060')
    app.run(debug=False, port=server_port, host='0.0.0.0')
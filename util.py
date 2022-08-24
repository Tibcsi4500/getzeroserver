import os
from flask import Flask, render_template, request
from google.cloud.sql.connector import Connector
import sqlalchemy
import pymysql
import urllib.request
import json
import requests

# Establishes a connection to the specified mysql cloud instance
def getconn() -> pymysql.connections.Connection:
    connector = Connector()
    conn: pymysql.connections.Connection = connector.connect(
        "turnkey-banner-354610:europe-west6:example",
        "pymysql",
        user="root",
        password="root",
        db="getzero"
    )
    return conn

# Creates handler for the mysql server
def getpool():
    pool = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=getconn,
    )
    return pool

# Returns the parameters passed to the web request
def getBody():
    if (request.method == 'GET'):
        return request.args.to_dict()
    elif (request.method == 'POST'):
        return request.form.to_dict()
    return {}

# Returns whether the specified key is in the specified array
def contains(key, array):
    for element in array:
        if(element == key):
            return True
    return False
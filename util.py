import os
from flask import Flask, render_template, request
from google.cloud.sql.connector import Connector
import sqlalchemy
import pymysql
import urllib.request
import json
import requests

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

def getpool():
    pool = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=getconn,
    )
    return pool

def getBody():
    if (request.method == 'GET'):
        return request.args
    elif (request.method == 'POST'):
        return request.form
    return {}
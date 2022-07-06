import os
from flask import Flask, render_template, request
from google.cloud.sql.connector import Connector
import sqlalchemy
import pymysql
import urllib.request
import json
import requests 

import util

#checks whether the given user credentials are valid
# params: name, password
def checkUser():
    data = util.getBody()
    try:
        name = data['name']
        password = data['password']
        pool = util.getpool()
        with pool.connect() as db_conn:
            SQL = sqlalchemy.text("SELECT 1 AS truth FROM users WHERE users.username = :name AND users.password = :password;")
            is_user = db_conn.execute(SQL, name = name, password = password)
            for _ in is_user:
                return "1"
            return "0"
    except Exception as e:
        return "Something went wrong"
    return "Something went wrong"

def getChallenge():
    data = util.getBody()
    try:
        user = data['userid']
        challenge = data['challengeid']
        pool = util.getpool()
        with pool.connect() as db_conn:
            SQL = sqlalchemy.text("SELECT * FROM challenges WHERE user_id = :user AND challenge_id = :challenge;")
            challenges = db_conn.execute(SQL, user = user, challenge = challenge)
            res = ""
            for row in challenges:
                res += str(row)
            return res
    except Exception as e:
        return "Something went wrong"
    return "Something went wrong"
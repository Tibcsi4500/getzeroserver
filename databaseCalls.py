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

def getAcceptedChallengesOfUser():
    data = util.getBody()
    try:
        user = data['userid']
        pool = util.getpool()
        with pool.connect() as db_conn:
            SQL = sqlalchemy.text(
                "SELECT challenges.challengeid as challengeid, challenges.title as title, ucr.progress as progress FROM challenges, userchallengerelation as ucr " + 
                "WHERE ucr.challengeid = challenges.challengeid AND " +
                "ucr.userid = :user AND ucr.finished = 0;"
                )
            challenges = db_conn.execute(SQL, user = user)
            res = ""
            for row in challenges:
                res += str(row['challengeid']) + ";" + str(row['title']) + ";" + str(row['progress']) + "\n"
            return res
    except Exception as e:
        return "Exception: " + str(e)
    return "Something went wrong"

def incrementChallengeProgress():
    data = util.getBody()
    try:
        user = data['userid']
        challenge = data['challengeid']
        pool = util.getpool()
        with pool.connect() as db_conn:
            SQL = sqlalchemy.text(
                "UPDATE userchallengerelation " + 
                "SET progress = progress + 1 " +
                "WHERE userid = :user AND challengeid = :challenge;"
                )
            db_conn.execute(SQL, user = user, challenge = challenge)

            return "1"
    except Exception as e:
        return "Exception: " + str(e)
    return "Something went wrong"

def getUnacceptedChallengesOfUser():
    data = util.getBody()
    try:
        user = data['userid']
        pool = util.getpool()
        with pool.connect() as db_conn:
            SQL = sqlalchemy.text(
                "SELECT challenges.challengeid as challengeid, challenges.title as title, challenges.description as description FROM challenges " + 
                "WHERE challengeid NOT IN (SELECT challengeid FROM userchallengerelation WHERE userid = :user) ;"
                )
            challenges = db_conn.execute(SQL, user = user)
            res = ""
            for row in challenges:
                res += str(row['challengeid']) + ";" + str(row['title']) + ";" + str(row['description']) + "\n"
            return res
    except Exception as e:
        return "Exception: " + str(e)
    return "Something went wrong"

def acceptChallengesOfUser():
    data = util.getBody()
    try:
        user = data['userid']
        challenges = data['challenges']

        challengelist = challenges.split("-")

        pool = util.getpool()
        with pool.connect() as db_conn:
            for challenge in challengelist:
                SQL = sqlalchemy.text(
                    "INSERT INTO userchallengerelation (userid, challengeid) " +
                    "VALUES (:user , :challenge ) ;"
                    )
                db_conn.execute(SQL, user = user, challenge = challenge)
            return "1"
    except Exception as e:
        return "Exception: " + str(e)
    return "Something went wrong"
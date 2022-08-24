import os
from flask import Flask, render_template, request
from google.cloud.sql.connector import Connector
import sqlalchemy
import pymysql
import urllib.request
import json
import requests 

import util

# Returns the accepted challenges of the user from the mysql db
# Params: 
# userid - the identifier of the user
# !! USES OLD CHALLENGE RETURN FORMAT !!
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

# Increments a challenge's progress for the user in the mysql db
# Params: 
# userid - the identifier of the user
# challengeid - the identifier of the challenge to be incremented
def incrementChallengeProgress():
	data = util.getBody()
	try:
		user = data['userid']
		challenge = data['challengeid']
		
		return "Done"
		
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

# Returns the unaccepted challenges of the user from the mysql db
# Params: 
# userid - the identifier of the user
# !! USES OLD CHALLENGE RETURN FORMAT !!
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

# Accepts the listed challenges for the user in the mysql db
# Params: 
# userid - the identifier of the user
# challenges - the identifiers of the challenges separated by '-'
def acceptChallengesOfUser():
	data = util.getBody()
	try:
		user = data['userid']
		challenges = data['challenges']
		
		return "Done"
		
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
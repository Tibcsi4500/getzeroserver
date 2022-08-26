import util
import json

def getAcceptedChallengesOfUser():
    data = util.getBody()
    try:
        userid = int(data['userid'])
        if('type' in data):
            typetext = data['type']
        else:
            typetext = 'none'
        if('room' in data):
            room = data['room']
        else:
            room = 'none'
        relationsFile = open("relations.txt")
        relations = json.loads(relationsFile.read())
        challengesFile = open("challenges.txt")
        challenges = json.loads(challengesFile.read())
        result = ""
        for relation in relations['relations']:
            if(relation['userid'] == userid):
                for challenge in challenges['challenges']:
                    if(relation['challengeid'] == challenge['challengeid']
                    and (challenge['appliance'] == typetext  or typetext == 'none')
                    and (challenge['room'] == room or room == 'none')):
                        result += challenge['title'] + ";" 
                        result += challenge['description'] + ";" 
                        result += str(challenge['challengeid']) + ";"
                        result += str(relation['progress']) + ";"
                        result += str(challenge['outof']) + ";"
                        result += str(challenge['appliance']) + ";"
                        result += str(challenge['room']) + "\n"
        challengesFile.close()
        relationsFile.close()
        return result
    except Exception as e:
        return "Something went wrong: " + str(e)
    return "Something went wrong"

def getUnacceptedChallengesOfUser():
    data = util.getBody()
    try:
        userid = int(data['userid'])
        if('type' in data):
            typetext = data['type']
        else:
            typetext = 'none'
        if('room' in data):
            room = data['room']
        else:
            room = 'none'
        relationsFile = open("relations.txt")
        relations = json.loads(relationsFile.read())
        challengesFile = open("challenges.txt")
        challenges = json.loads(challengesFile.read())
        acceptedChallenges = []
        result = ""
        for relation in relations['relations']:
            if(relation['userid'] == userid):
                acceptedChallenges.append(relation['challengeid'])
        for challenge in challenges['challenges']:
            if((not util.contains(challenge['challengeid'], acceptedChallenges))
            and (challenge['appliance'] == typetext  or typetext == 'none')
            and (challenge['room'] == room or room == 'none')):
                result += challenge['title'] + ";" 
                result += challenge['description'] + ";" 
                result += str(challenge['challengeid']) + ";"
                result += str(0) + ";"
                result += str(challenge['outof']) + ";"
                result += str(challenge['appliance']) + ";"
                result += str(challenge['room']) + "\n"
        challengesFile.close()
        relationsFile.close()
        return result
    except Exception as e:
        return "Something went wrong: " + str(e)
    return "Something went wrong"

def incrementChallengeProgress():
    data = util.getBody()
    try:
        userid = int(data['userid'])
        challengeid = int(data['challengeid'])
        relationsFile = open("relations.txt")
        relations = json.loads(relationsFile.read())
        relationsFile.close()
        relationsFile = open("relations.txt", "w")
        for relation in relations['relations']:
            if(relation['userid'] == userid and relation['challengeid'] == challengeid):
                relation['progress'] += 1
        
        json.dump(relations, relationsFile)
        relationsFile.close()
        return "1"
    except Exception as e:
        return "Something went wrong: " + str(e)
    return "Something went wrong"

def acceptChallengesOfUser():
    data = util.getBody()
    try:
        userid = int(data['userid'])
        challengeidstring = data['challenges']
        relationsFile = open("relations.txt")
        relations = json.loads(relationsFile.read())
        relationsFile.close()
        relationsFile = open("relations.txt", "w")
        challengeids = challengeidstring.split("-")
        for challengeid in challengeids:
            toInsert = {
                "userid":userid,
                "challengeid":int(challengeid),
                "progress":0
            }
            relations['relations'].append(toInsert)
        
        json.dump(relations, relationsFile)
        relationsFile.close()
        return "1"
    except Exception as e:
        return "Something went wrong: " + str(e)
    return "Something went wrong"
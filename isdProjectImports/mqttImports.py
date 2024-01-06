from flask_mqtt import Mqtt
import json
import random
from datetime import datetime

mqttBrokerPort = 1883
mqttKeepAliveSec = 10
mqttBrokerIP = 'localhost'  # Replace with broker IP if not running locally.
mqttQoSLevel = 1

mqtt = Mqtt()

# Topics
# Registration topics
registrationIncomingTopic = '/registration/Server/#' # + mac address, ESPs will start registration with this topic.
registrationResponeTopic = '/registration/esp/'  # + mac address, server will respond to ESPs with this topic.
# VoteSetup topics
voteSetupTopic = '/setupVote/Setup'  # Vote information is posted here.
voteResyncTopic = '/setupVote/Resync'  # ESPs will request resync with this topic.
# Vote topics
voteIncomingTopic = '/vote/#'  # + votingID, ESPs will send votes to this topic.

initialSubscribeTopics = [registrationIncomingTopic, voteResyncTopic, voteIncomingTopic]

# Decodes JSON string to Python dictionary.
def decodeStringToJSON(json_string):
    try:
        decodedMessage = json.loads(json_string)
        return decodedMessage
    except json.decoder.JSONDecodeError as error:
        with open('log.txt', 'a') as logFile:
            logFile.write(f'{datetime.now()}: decodeStringToJSON(), JSONDecodeError: {error}\n')
        return -1


# Validates that all keywords in keywordList are present in decodedJSON.
def validateKeywordsInJSON(decodedJSON, keywordList, verifycationLevel):
    jsonKeySet = set(decodedJSON.keys())

    if verifycationLevel == 1:
        for keyword in keywordList:
            if keyword not in jsonKeySet:
                return False
        return True

    elif verifycationLevel == 2:
        for keyword in keywordList:
            if keyword not in jsonKeySet or not decodedJSON[keyword] or decodedJSON[keyword] == "NULL":
                return False
        return True

    else:
        raise ValueError("Invalid verification level. Please provide either 1 or 2.")


# Publishes 'message' to MQTT 'topic'.
def publishJSONtoMQTT(topic, message):
    try:
        mqtt.publish(topic, message, qos=mqttQoSLevel)
    except:
        
        with open('log.txt', 'a') as logFile:
            logFile.write(f'{datetime.now()}: publishJSONtoMQTT(), Failed to publish message: {str(message)}to topic: {topic}\n')
        return False
    else:
        return True

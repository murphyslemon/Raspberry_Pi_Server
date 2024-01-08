from flask import Flask, request, jsonify
from flask_mqtt import Mqtt
import json
import random
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from isdProjectImports import credentials
from isdProjectImports import mqttImports
from isdProjectImports import dbFunctions
from isdProjectImports import voteHandling

mqttBrokerPort = 1883
mqttKeepAliveSec = 10
mqttBrokerIP = 'localhost'  # Replace with broker IP if not running locally.
mqttQoSLevel = 1

globalVoteInformation = voteHandling.VoteInformation() # Global vote information object.
globalVoteInformationList = []  # List of global vote information objects.

# Flask app setup.
app = Flask(__name__)

# MQTT setup.
app.config['MQTT_BROKER_URL'] = mqttBrokerIP
app.config['MQTT_BROKER_PORT'] = mqttBrokerPort
app.config['MQTT_KEEPALIVE'] = mqttKeepAliveSec
app.config['MQTT_TLS_ENABLED'] = False

# Database setup.
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{credentials.dbUsername}:{credentials.dbPassword}@{credentials.dbHostname}:{credentials.dbPort}/{credentials.dbName}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Only for confirming that server is running.
@app.route('/')
def index():
    return 'Flask MQTT Server is running!'

# Subscribe to all topics in 'initialSubscribeTopics' list when server is started.
@mqttImports.mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
   if rc == 0:
       for topic in mqttImports.initialSubscribeTopics:
           mqttImports.mqtt.subscribe(topic, qos=1)  # subscribe to each topic
           with open('log.txt', 'a') as logFile:
               logFile.write(f'{datetime.now()}: mqtt.on_connect(), subscribed to topic: {topic}\n')
   else:
       with open('log.txt', 'a') as logFile:
           logFile.write(f'{datetime.now()}: mqtt.on_connect(), connection failed\n')


# MQTT message handling
@mqttImports.mqtt.on_message()
def handle_message(client, userdata, message):
    receivedMessage = message.payload.decode("utf-8")
    receivedTopic = message.topic
    with open('log.txt', 'a') as logFile:
        logFile.write(f'{datetime.now()}: mqtt.on_message(), received message: {receivedMessage} on topic: {receivedTopic}\n')

    # Decode JSON message.
    decodedMessage = mqttImports.decodeStringToJSON(receivedMessage)
    if decodedMessage == -1:
        with open('log.txt', 'a') as logFile:
            logFile.write(f'{datetime.now()}: mqtt.on_message(), JSON decode failed\n')
        return # TODO: maybe add something to notify ESPs about failed JSON decode.

    # Handle received message based on topic.
    
    if receivedTopic.startswith("/registration/Server/") == True:
        with open('log.txt', 'a') as logFile:
            logFile.write(f'{datetime.now()}: mqtt.on_message(), received message on /registration/Server/\n')

        # Extract ESP MAC address from topic.
        macAddress = receivedTopic.split("/")[3]

        # Register ESP in database.
        # Inside mqtt.on_message() in app.py
        registeredESP, registrationStatus = dbFunctions.register_esp(app, macAddress)

        if registrationStatus == True:
            # return uniqueID to ESP.
            mqttImports.mqtt.publish(f'/registration/esp/{macAddress}', f'{{"VotingID":"{registeredESP.DeviceID}"}}', qos=1)
            mqttImports.mqtt.subscribe(f'/registration/ESP/{registeredESP.DeviceID}', qos=1) # Subscribe to ESP's uniqueID topic.

            with open('log.txt', 'a') as logFile:
                logFile.write(f'{datetime.now()}: mqtt.on_message(), ESP registration successful, ESP uniqueID: {registeredESP.DeviceID}, ESP MAC address: {registeredESP.MacAddress}\n')

        else:
            #TODO: add something to notify ESP about failed registration.
            with open('log.txt', 'a') as logFile:
                logFile.write(f'{datetime.now()}: mqtt.on_message(), ESP registration failed\n')

        return # Exit function.

    elif receivedTopic.startswith("/vote/") == True:
        with open('log.txt', 'a') as logFile:
            logFile.write(f'{datetime.now()}: mqtt.on_message(), received message on /vote/\n')

        # Extract ESP ID from topic.
        deviceID = receivedTopic.split("/")[2]
        # Update vote in database.
        if globalVoteInformation.voteEndTime > datetime.now() and globalVoteInformation.voteStartTime < datetime.now():
            dbFunctions.update_vote(deviceID, decodedMessage['vote'])
            
        else:
            with open('log.txt', 'a') as logFile:
                logFile.write(f'{datetime.now()}: mqtt.on_message(), vote not updated, vote is not active\n')
            

    return # Exit function.

# API endpoints

# GET all registered ESPs.
@app.route('/api/getRegisteredESPs', methods=['GET'])
def getRegisteredESPs():
    return dbFunctions.get_registered_esps(app)


# GET all Topics (votes).
@app.route('/api/getTopics', methods=['GET'])
def getTopics():
    return dbFunctions.get_all_topics(app)


# GET Specific Topic (vote).
@app.route('/api/getTopic/<topicID>', methods=['GET'])
def getTopic(topicID):
    return dbFunctions.get_topic(app, topicID)


# Create new Topic (vote).
@app.route('/api/createTopic', methods=['POST'])
def createTopic():
    """Input JSON format

    {
        "Title": "TEXT",
        "Description": "TEXT",
        "StartTime": "YYY-MM-DD HH:MM:SS",
        "EndTime": "YYY-MM-DD HH:MM:SS"
    }
    """
    try:
        data = request.json
        # Validate request.
        if mqttImports.validateKeywordsInJSON(data, ['Title', 'Description', 'StartTime', 'EndTime'], 1) == False:
            with open('log.txt', 'a') as logFile:
                logFile.write(f'{datetime.now()}: createTopic(), Invalid request.\n')
            return jsonify({'message': 'Invalid request.'}), 400

        globalVoteInformation.updateVoteInformation(data['Title'], data['Description'], data['StartTime'], data['EndTime'])

        # Create new topic in database.
        if dbFunctions.create_topic(app, globalVoteInformation) == True:
            # TODO: figure out voteStartTiming.
            return jsonify({'message': 'Topic created successfully.'}), 200
        else:
            return jsonify({'message': 'Topic creation failed.'}), 400

    except Exception as errorMsg:
        with open('log.txt', 'a') as logFile:
            logFile.write(f'{datetime.now()}: createTopic(), Error: {errorMsg}\n')
        return jsonify({'message': 'Internal server error.'}), 500


# Assign user to ESP.
@app.route('/api/assignUserToESP', methods=['POST'])
def assignUserToESP():
    """Input JSON format

    {
        "username": "TEXT",
        "registrationDate": "YYY-MM-DD HH:MM:SS",
        "espID": "INT"
    }
    """
    try:
        data = request.json

        # Validate request.
        if mqttImports.validateKeywordsInJSON(data, ['username', 'registrationDate', 'espID'], 1) == False:
            with open('log.txt', 'a') as logFile:
                logFile.write(f'{datetime.now()}: assignUserToESP(), Invalid request.\n')
            return jsonify({'message': 'Invalid request.'}), 400
        
        dbFunctions.assign_user_to_esp(app, data['username'], data['registrationDate'], data['espID'])
    
        return jsonify({'message': 'User assigned to ESP.'}), 200
    
    except:
        return jsonify({'message': 'Invalid data.'}), 400 # TODO: change return message to something more descriptive.





if __name__ == '__main__':
    # Initialize imported app extensions.
    dbFunctions.db.init_app(app)
    mqttImports.mqtt.init_app(app)

    app.run(host='0.0.0.0', port=5000, use_reloader=False)

    # Log DB boot info to log file.
    with open('log.txt', 'a') as logFile:
        logFile.write(f'{datetime.now()}: Server started.\n')
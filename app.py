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
from isdProjectImports import esp

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

@app.route('/')
def index():
    return 'Flask MQTT Server is running!'

# Subscribe to all topics in 'initialSubscribeTopics' list when server is started.
@mqttImports.mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
   if rc == 0:
       for topic in mqttImports.initialSubscribeTopics:
           mqttImports.mqtt.subscribe(topic, qos=1)  # subscribe to each topic
   else:
       print(f'Connection failed. Code: {rc}')


# MQTT message handling
@mqttImports.mqtt.on_message()
def handle_message(client, userdata, message):
    receivedMessage = message.payload.decode("utf-8")
    receivedTopic = message.topic
    print(f'Received message: {receivedMessage} on topic: {receivedTopic}')

    # Decode JSON message.
    decodedMessage = mqttImports.decodeStringToJSON(receivedMessage)
    if decodedMessage == -1:
        print('JSON decode failed.')
        return # TODO: maybe add something to notify ESPs about failed JSON decode.

    # Handle received message based on topic.
    print(f'starts with /registration/Server/: {receivedTopic.startswith("/registration/Server/")}')
    if receivedTopic.startswith("/registration/Server/") == True:
        for i in range(len(esp.Esp.registeredESPs)):
            if esp.Esp.registeredESPs[i].macAddress == decodedMessage['Mac']:
                print(f'{decodedMessage["Mac"]} ESP already registered.')
                esp.Esp.registeredESPs[i].returnUniqueIDToEsp() # Resends uniqueID to ESP.
                return
            
        esp.Esp(decodedMessage['Mac'])
        print(f'{decodedMessage["Mac"]} ESP registered.')
        esp.Esp.registeredESPs[-1].returnUniqueIDToEsp() # Sends uniqueID to ESP.
        return

    
    return

# API endpoints

# GET all registered ESPs.
@app.route('/api/getRegisteredESPs', methods=['GET'])
def getRegisteredESPs():
    return dbFunctions.get_registered_esps()


# GET all Topics (votes).
@app.route('/api/getTopics', methods=['GET'])
def getTopics():
    return dbFunctions.get_topics()


# GET Specific Topic (vote).
@app.route('/api/getTopic/<topicID>', methods=['GET'])
def getTopic(topicID):
    return dbFunctions.get_topic(topicID)


# Create new Topic (vote).
@app.route('/api/createTopic', methods=['POST'])
def createTopic():
    try:
        # Setup vote information.
        data = request.json
        mqttImports.validateKeywordsInJSON(data, ['title', 'description', 'voteStartTime', 'voteEndTime'], 1)
        globalVoteInformation.updateVoteInformation(data['title'], data['description'], data['voteStartTime'], data['voteEndTime'])

        # Create new topic in database.
        if dbFunctions.create_topic(globalVoteInformation) == True:
            # TODO: figure out voteStartTiming.
            return jsonify({'message': 'Topic created.'}), 200
        else:
            return jsonify({'message': 'Topic creation failed.'}), 400

    except:
        return jsonify({'message': 'Invalid data.'}), 400 # TODO: change return message to something more descriptive.


# Assign user to ESP.
@app.route('/api/assignUserToESP', methods=['POST'])
def assignUserToESP():
    try:
        data = request.json
        dbFunctions.assign_user_to_esp(data['userID'], data['espID'])
    
        return jsonify({'message': 'User assigned to ESP.'}), 200
    
    except:
        return jsonify({'message': 'Invalid data.'}), 400 # TODO: change return message to something more descriptive.

if __name__ == '__main__':
    # Initialize imported app extensions.
    dbFunctions.db.init_app(app)
    mqttImports.mqtt.init_app(app)

    app.run(host='0.0.0.0', port=5000, use_reloader=False)
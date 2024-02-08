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
from isdProjectImports import logHandler
from flask_cors import CORS

mqttBrokerPort = 1883
mqttKeepAliveSec = 10
mqttBrokerIP = 'localhost'  # Replace with broker IP if not running locally.
mqttQoSLevel = 1

globalVoteInformation = voteHandling.VoteInformation() # Global vote information object.
globalVoteInformationList = []  # List of global vote information objects.

# Flask app setup.
app = Flask(__name__)
CORS(app)

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
            logHandler.log(f'handle_message(), Subscribed to topic: {topic}')
   else:
        logHandler.log(f'handle_message(), Connection failed with result code {str(rc)}')


# MQTT message handling
# TODO: Figure out a way to move the case handling to their own functions.
@mqttImports.mqtt.on_message()
def handle_message(client, userdata, message):
    receivedMessage = message.payload.decode("utf-8")
    receivedTopic = message.topic
    logHandler.log(f'handle_message(), Received message: {receivedMessage} on topic: {receivedTopic}')

    # Decode JSON message.
    decodedMessage = mqttImports.decodeStringToJSON(receivedMessage)
    if decodedMessage == -1:
        logHandler.log(f'JSON decode failed.')
        return # TODO: maybe add something to notify ESPs about failed JSON decode.

    # Handle received message based on topic.
    

    # ESP registration handling.
    if receivedTopic.startswith("/registration/Server/") == True:
        logHandler.log(f'handle_message(), Message handling going to ESP registration handling path.')

        # Extract ESP MAC address from topic.
        macAddress = receivedTopic.split("/")[3]

        # Register ESP in database.
        # Inside mqtt.on_message() in app.py
        registeredESP, registrationStatus = dbFunctions.register_esp(app, macAddress)

        if registrationStatus == True:
            # return uniqueID to ESP.
            mqttImports.mqtt.publish(f'/registration/esp/{macAddress}', f'{{"VotingID":"{registeredESP.DeviceID}"}}', qos=1)
            mqttImports.mqtt.subscribe(f'/registration/ESP/{registeredESP.DeviceID}', qos=1) # Subscribe to ESP's uniqueID topic.
            logHandler.log(f'handle_message(), ESP registration successful, ESP uniqueID: {registeredESP.DeviceID}, ESP MAC address: {registeredESP.MacAddress}\n')

        else:
            #TODO: add something to notify ESP about failed registration.
            logHandler.log(f'handle_message(), ESP registration failed, ESP MAC address: {macAddress}\n')

        return # end of ESP registration handling.


    # Vote handling.
    elif receivedTopic.startswith("/vote/") == True:
        logHandler.log(f'handle_message(), Message handling going to vote handling path.')

        # Extract ESP ID from topic.
        deviceID = receivedTopic.split("/")[2]

        # Convert strings to datetime objects
        vote_end_time = datetime.strptime(globalVoteInformation.voteEndTime, '%Y-%m-%d %H:%M:%S')
        vote_start_time = datetime.strptime(globalVoteInformation.voteStartTime, '%Y-%m-%d %H:%M:%S')

        # Test timing restrictions and if vote is for the correct topic.
        if (
            vote_end_time < datetime.now()
            or vote_start_time > datetime.now()
            or decodedMessage['VoteTitle'] != globalVoteInformation.title
        ):
            logHandler.log(f'handle_message(), vote is not active or vote is not for the correct topic, exit function.')
            logHandler.log(f'handle_message(), vote_end_time: {vote_end_time}, vote_start_time: {vote_start_time}, datetime.now(): {datetime.now()}')
            logHandler.log(f'handle_message(), decodedMessage[\'VoteTitle\']: {decodedMessage["VoteTitle"]}, globalVoteInformation.title: {globalVoteInformation.title}')
            return # Vote is not active or vote is not for the correct topic, exit function.
        
        elif dbFunctions.find_if_vote_exists(app, deviceID, globalVoteInformation) == False:
            dbFunctions.create_vote(app, deviceID, decodedMessage['vote'], globalVoteInformation)
            return # Exit function.

        else:
            dbFunctions.update_vote(app, deviceID, decodedMessage['vote'], globalVoteInformation)
            return # Exit function.
    
    # Vote resync handling.
    elif receivedTopic == "/setupVote/Resync":
        logHandler.log(f'handle_message(), Message handling going to vote resync handling path.')
        
        # Create message.
        if globalVoteInformation.voteEndTime < datetime.now():
            resyncMessage = {
            "VoteTitle": globalVoteInformation.title,
            "VoteType": "public", #TODO: Redo once private votes are implemented.
            "VoteStatus": "ended"
            }
        else:
            resyncMessage = {
                "VoteTitle": globalVoteInformation.title,
                "VoteType": "public",
                "VoteStatus": "started"
            }

        # Send vote information to /setupVote/Resync topic.
        mqttImports.publishJSONtoMQTT('/setupVote/Setup', resyncMessage)
        
        return # End of vote handling.

    return # End of function.

# API endpoints

# GET all registered ESPs.
@app.route('/api/getRegisteredESPs', methods=['GET'])
def getRegisteredESPs():
    return dbFunctions.get_registered_esps(app)

@app.route('/api/getUnassignedESPs', methods=['GET'])
def getUnassignedESPs():
    return dbFunctions.get_unassigned_esps(app)


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
    """Input JSON format:
    {
        "Title": "TEXT",
        "Description": "TEXT",
        "StartTime": "YYYY-MM-DD HH:MM:SS",
        "EndTime": "YYYY-MM-DD HH:MM:SS"
    }
    """
    try:
        data = request.json

        # Validate request.
        if mqttImports.validateKeywordsInJSON(data, ['Title', 'Description', 'StartTime', 'EndTime'], 1) == False:
            logHandler.log(f'createTopic(), Invalid request.')
            return jsonify({'message': 'Invalid request.'}), 400

        globalVoteInformation.updateVoteInformation(data['Title'], data['Description'], data['StartTime'], data['EndTime'])

        # Publish vote information to /setupVote/Setup topic.
        if globalVoteInformation.voteEndTime < datetime.now():
            voteInformationJson = f'{{"VoteTitle":"{globalVoteInformation.title}","VoteType":"public","VoteStatus":"ended"}}'
        else:
            voteInformationJson = f'{{"VoteTitle":"{globalVoteInformation.title}","VoteType":"public","VoteStatus":"started"}}'
        mqttImports.publishJSONtoMQTT('/setupVote/Setup', globalVoteInformation.getVoteInformation())

        # Create new topic in database.
        if dbFunctions.create_topic(app, globalVoteInformation) == True:
            # TODO: figure out voteStartTiming.
            return jsonify({'message': 'Topic created successfully.'}), 200
        else:
            return jsonify({'message': 'Topic creation failed.'}), 400

    except Exception as errorMsg:
        logHandler.log(f'createTopic(), Error: {errorMsg}')
        return jsonify({'message': 'Internal server error.'}), 500


# Assign user to ESP.
@app.route('/api/assignUserToESP', methods=['POST'])
def assignUserToESP():
    """Input JSON format:
    {
        "username": "TEXT",
        "espID": "INT"
    }
    """
    try:
        data = request.json

        # Validate request.
        if mqttImports.validateKeywordsInJSON(data, ['username', 'espID'], 1) == False:
            logHandler.log(f'assignUserToESP(), Invalid request.')
            return jsonify({'message': 'Invalid request.'}), 400
        
        return dbFunctions.assign_user_to_esp(app, data['username'], data['espID'])
    
    except Exception as errorMsg:
        logHandler.log(f'assignUserToESP(), Error: {errorMsg}')
        return jsonify({'message': f'{str(errorMsg)}'}), 400


# Unassign ESP
@app.route('/api/unassignESP', methods=['POST'])
def unassignESP():
    """Input JSON format:
    {
        "espID": "INT"
    }
    """
    try:
        data = request.json

        # Validate request.
        if mqttImports.validateKeywordsInJSON(data, ['espID'], 1) == False:
            logHandler.log(f'unassignESP(), Invalid request.')
            return jsonify({'message': 'Invalid request.'}), 400
        
        return dbFunctions.unassign_esp_with_id(app, data['espID'])
    
    except Exception as errorMsg:
        logHandler.log(f'unassignESP(), Error: {errorMsg}')
        return jsonify({'message': f'{str(errorMsg)}'}), 500


# Unassing all ESPs
@app.route('/api/unassignAllESPs', methods=['POST'])
def unassignAllESPs():
    return dbFunctions.unassign_all_esps(app)


@app.route('/api/getVotes/<int:topicID>', methods=['GET'])
def get_votes_by_topic(topicID):
    """
    Endpoint to get votes for a specific topic ID.
    """
    return dbFunctions.get_votes(app, topicID)



if __name__ == '__main__':
    # Initialize imported app extensions.
    dbFunctions.db.init_app(app)
    mqttImports.mqtt.init_app(app)

    app.run(host='0.0.0.0', port=5000, use_reloader=False)

    # Log DB boot info to log file.
    logHandler.log(f'Server started.')

    dbFunctions.find_active_topic(app, globalVoteInformation)
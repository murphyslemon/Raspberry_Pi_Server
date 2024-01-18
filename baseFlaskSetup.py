# DEPRECATED: Do not use!

from flask import Flask
from flask_mqtt import Mqtt
import json
import random

mqttBrokerPort = 1883
mqttKeepAliveSec = 10
mqttBrokerIP = 'localhost'  # Replace with broker IP if not running locally.

# Topics
# Registration topics
registrationIncomingTopic = '/registration/Server/#' # + mac address, ESPs will start registration with this topic.
registrationResponeTopic = '/registration/esp/'  # + mac address, server will respond to ESPs with this topic.
# VoteSetup topics
voteSetupTopic = '/setupVote/Setup'  # Vote information is posted here.
voteResyncTopic = '/setupVote/Resync'  # ESPs will request resync with this topic.
# Vote topics
voteIncomingTopic = '/vote/'  # + votingID, ESPs will send votes to this topic.

# List of all topics to subscribe on server boot.
initialSubscribeTopics = [registrationIncomingTopic, voteResyncTopic]  # List of all topics to subscribe to.

# Flask app setup.
app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = mqttBrokerIP
app.config['MQTT_BROKER_PORT'] = mqttBrokerPort
app.config['MQTT_KEEPALIVE'] = mqttKeepAliveSec
app.config['MQTT_TLS_ENABLED'] = False

mqtt = Mqtt(app)
espList = []  # List of all ESPs that have been registered.

class Esp:

    registredESPs = 0

    def __init__(self, mac_address, registeredUser='NULL',):
        self.mac_address = mac_address
        self.registeredUser = registeredUser

        self.uniqueID = random.randint(1, 10)  # Needs to be changed later.
        self.voteStatus = 'pass'  # default value is pass.

        self.registration_confirmation_topic = registrationResponeTopic + self.mac_address


        Esp.registredESPs += 1


# Subscribe to all topics in 'initialSubscribeTopics' list when server is started.
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
   if rc == 0:
       for topic in initialSubscribeTopics:
           mqtt.subscribe(topic, qos=1)  # subscribe to each topic
   else:
       print(f'Connection failed. Code: {rc}')


@mqtt.on_message()
def handle_message(client, userdata, message):


#@app.route('/')
#def index():
#    return 'Flask MQTT Server is running!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, use_reloader=False)

from flask import Flask
from flask_mqtt import Mqtt
import json
import random

app = Flask(__name__)
app.config["MQTT_BROKER_URL"] = "localhost"  # Replace with broker IP if not running locally.
app.config["MQTT_BROKER_PORT"] = 1883
app.config["MQTT_KEEPALIVE"] = 10
app.config["MQTT_TLS_ENABLED"] = False

# Topics
registration_topic = '/registration/Server/#'
registration_topic_partial = '/registration/Server'
registration_response_topic = '/registration/esp/'  # + mac address

test_receive_topic = '/test/server/receive_message'
test_send_topic = '/test/est/send_message'
all_topics = [registration_topic, test_receive_topic]  # List of all topics to subscribe to.

mqtt = Mqtt(app)
esp_list = []  # List of all ESPs that have been registered.

class Esp:

    registredESPs = 0

    def __init__(self, mac_address, registeredUser='NULL',):
        self.mac_address = mac_address
        self.registeredUser = registeredUser

        self.uniqueID = random.randint(1, 10)  # Needs to be changed later.
        self.voteStatus = 'pass'  # default value is pass.

        self.registration_confirmation_topic = registration_response_topic + self.mac_address


        Esp.registredESPs += 1


# Subscribe to all topics in 'all_topics' list when server is started.
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
   if rc == 0:
       for topic in all_topics:
           mqtt.subscribe(topic, qos=1)  # subscribe to each topic
   else:
       print(f'Connection failed. Code: {rc}')


# Sort incoming messages.
@mqtt.on_message()
def handle_message(client, userdata, message):
    received_message = message.payload.decode("utf-8")

    #print(f'\n\nReceived message on topic {message.topic}: {received_message}')  # Uncomment for debugging to read plain received message.

    # Decode JSON
    decoded_message = decode_json(received_message)

    # Veriify that the message is a JSON object.
    if decoded_message == -1:
        print('Message is not a JSON object.')
        return

    # Example message handling for the registration topic.
    if message.topic.startswith(registration_topic_partial):
        registration_message_handler(decoded_message)

    # Simple test topic.
    elif message.topic == test_receive_topic:
        test_message_handler(decoded_message)


    # Message on unknown topic.        
    else:
        print(f'Received message on not handeled topic: {received_message}')


# Index page, currently only used to verify that the server is running.
@app.route("/")
def index():
    return 'Flask MQTT Server is running!'


def decode_json(json_string):
    try:
        decoded_message = json.loads(json_string)
        print('JSON test passed.')
        return decoded_message
    except json.decoder.JSONDecodeError as error:
        print(f'JSON test failed. Error: {error}')
        return -1


# Check if all keywords are present in the JSON keys.
def check_keywords_in_json(decoded_json, keyword_list):
    # Convert the JSON keys to a set for faster keyword checking.
    json_keys_set = set(decoded_json.keys())

    # Check if all keywords are present in the JSON keys.
    for keyword in keyword_list:
        if keyword not in json_keys_set:
            return False
    
    return True


def try_publish(topic, message):
    try:
        mqtt.publish(topic, message, qos=1)
    except:
        print(f'Failed to publish to topic: {topic}')


# Handle messages in the registration topic.
def registration_message_handler(decoded_message):

    if check_keywords_in_json(decoded_message, ["Mac"]):

        # Check if the ESP is already registered.
        for esp in esp_list:
            if esp.mac_address == decoded_message["Mac"]:
                print(f'ESP with MAC address {decoded_message["Mac"]} is already registered.')

                # Return ESPs uniqueID.
                try_publish(esp.registration_confirmation_topic, f'{{"VotingID":"{esp.uniqueID}"}}')
                return

        # Register ESP.
        esp = Esp(decoded_message["Mac"])
        esp_list.append(esp)
        print(f'ESP with MAC address {decoded_message["Mac"]} has been registered.')

        print(f'Publishing to topic: {registration_response_topic + decoded_message["Mac"]}')
        try_publish(esp.registration_confirmation_topic, f'{{"VotingID":"{esp.uniqueID}"}}')

    else:
        print('Message did not include "Mac" key.')
    return


# Handle messages in the test topic.
def test_message_handler(decoded_message):
    for key, value in decoded_message.items():
        print(f"Key: {key}, Value: {value}")
    
    '''
    If you wish to send a message back.

    message = "Your message here" # Message to send.
    mqtt.publish(test_send_topic, f"{message}", qos=1)
    '''
    return


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, use_reloader=False)

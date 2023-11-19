from flask import Flask
from flask_mqtt import Mqtt

app = Flask(__name__)

# MQTT Configuration
app.config['MQTT_BROKER_URL'] = 'localhost'  # MQTT broker is running on the same machine
app.config['MQTT_BROKER_PORT'] = 1883        # Default port for MQTT
app.config['MQTT_USERNAME'] = ''             # no authentication set yet
app.config['MQTT_PASSWORD'] = ''             # no authentication set yet

mqtt = Mqtt(app)

@app.route('/')
def index():
    return 'Hello from Flask with MQTT!'

@app.route('/publish')
def publish_message():
    mqtt.publish('test/topic', 'Hello from Flask MQTT')
    return 'Message published to MQTT'

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('some/topic')

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    print(f'Received message on {message.topic}: {message.payload.decode()}')

# MQTT event handlers
# add functions to handle MQTT events, like on_connect, on_message, etc.

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

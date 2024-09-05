import paho.mqtt.client as mqtt
from controllers.device_to_server import WeatherController
from Library.DotDictLibrary import DotDictLibrary
import json
import asyncio

class MqttLibraryClass:
    def __init__(self, broker_address, broker_port):
        self.client = mqtt.Client()
        self.broker_address = broker_address
        self.broker_port = broker_port
        # Callback functions
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.subscriptions = []  # Hold subscriptions for later

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected to MQTT broker with result code {rc}")
        if rc == 0:
            # Successfully connected
            for topic, qos in self.subscriptions:
                print(f"Subscribing to {topic} with QoS {qos}")
                client.subscribe(topic, qos=qos)
        else:
            print(f"Failed to connect, return code {rc}")

    def on_message(self, client, userdata, msg):
        try:
            print(f"Message received on topic {msg.topic}: {msg.payload}")
            topic_name = msg.topic
            parts = topic_name.split('/')

            # Deserialize payload into dictionary
            reqdata = DotDictLibrary(json.loads(msg.payload.decode('utf-8')))
            
            # Asynchronous call to process message
            asyncio.create_task(WeatherController.get_weather_data(reqdata, parts[1], parts[2]))
        except Exception as e:
            print(f"Error in on_message: {e}")

    def connect(self):
        self.client.connect(self.broker_address, self.broker_port, 60)
        self.client.loop_start()

    def subscribe(self, topics):
        # Add topics to the subscription list
        for topic, qos in topics:
            self.subscriptions.append((topic, qos))

        # Subscribe immediately if already connected
        if self.client.is_connected():
            for topic, qos in self.subscriptions:
                print(f"Subscribing immediately to {topic} with QoS {qos}")
                self.client.subscribe(topic, qos=qos)

    def publish(self, topic, message, qos=0):
        self.client.publish(topic, message, qos=qos)

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
        print("Disconnected from MQTT broker")

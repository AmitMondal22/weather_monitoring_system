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
        self.subscriptions = []

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        for topic, qos in self.subscriptions:
            print(f"Subscribing to {topic} with QoS {qos}")
            client.subscribe(topic, qos=qos)

    def on_message(self, client, userdata, msg):
        try:
            print(f"Message received on topic {msg.topic}")
            topic_name=msg.topic
            parts = topic_name.split('/')
            # reqdata=DotDictLibrary(json.loads(msg.payload))
            # if parts[0] == "ums":
            reqdata=DotDictLibrary(json.loads(msg.payload.decode('utf-8')))
            
            asyncio.run(WeatherController.get_weather_data(reqdata,parts[1],parts[2]))
        except Exception as e:
            print("Error in on_message",e)
    

    def connect(self):
        self.client.connect(self.broker_address, self.broker_port, 60)
        self.client.loop_start()

    # def subscribe(self, topics):
    #     for topic, qos in topics:
    #         self.subscriptions.append((topic, qos))
    #         if self.client.is_connected():
    #             print("jdsbcjh")
    #             self.client.subscribe(topic, qos=qos)
    def subscribe(self, topics):
        for topic, qos in topics:
            # Check if the topic is already subscribed
            if (topic, qos) not in self.subscriptions:
                self.subscriptions.append((topic, qos))
                if self.client.is_connected():
                    print("Subscribed to topic: ", topic)
                    self.client.subscribe(topic, qos=qos)

    def publish(self, topic, message, qos=0):
        self.client.publish(topic, message, qos=qos)

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
        print("Disconnected from MQTT broker")
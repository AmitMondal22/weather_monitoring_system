from fastapi import APIRouter, HTTPException, Response
from Library.MqttLibraryClass import MqttLibraryClass
from hooks.update_event_hooks import update_topics
from utils.response import errorResponse, successResponse

mqtt_routes = APIRouter()

# Initialize the MQTT client class
mqtt_client = MqttLibraryClass("techavoiot.co.in", 1883)

@mqtt_routes.on_event("startup")
async def startup_event():
    # Connect to the MQTT broker
    mqtt_client.connect()

    # Subscribe to topics asynchronously
    await subscribe_topics()

async def subscribe_topics():
    try:
        # Get the updated topics
        data = await update_topics()
        print("Subscribing to topics:", data)
        mqtt_client.subscribe(data)  # Topics are a list of tuples [(topic, qos), ...]
    except Exception as e:
        print("Error in subscribing to topics:", e)

# Example route for manual publishing
@mqtt_routes.post("/publish/")
async def publish_message(topic: str, message: str):
    try:
        mqtt_client.publish(topic, message)
        return {"message": "Message published successfully"}
    except Exception as e:
        return {"error": str(e)}

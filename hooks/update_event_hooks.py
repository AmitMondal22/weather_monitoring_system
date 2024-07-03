
from db_model.MqttData import mqtt_topic_name
async def update_topics():
    # Retrieve topics from the database
    data = await mqtt_topic_name()

    # Generate EMS topic names
    ems_topics = [("ems/" + data[i]['concatenated_string'], 0) for i in range(len(data))]

    # Generate UPSMS topic names
    upsms_topics = [("UPSMS/" + data[i]['concatenated_string'], 0) for i in range(len(data))]

    # Combine EMS and UPSMS topic lists
    all_topics = ems_topics + upsms_topics

    return all_topics
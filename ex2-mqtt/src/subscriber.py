import paho.mqtt.client as mqtt
import logging
import json

from utils import Statistics
from constants import ENVIRONMENT_TOPIC_BASE

class DeviceSubscriber:
    def __init__(self, subscriber_id, broker, port, statistics: Statistics):
        self.subscriber_id = subscriber_id
        self.broker = broker
        self.port = port
        self.statistics = statistics

        self.client = mqtt.Client(client_id=f"subscriber_{subscriber_id}")
        self.received_messages = {}

        # Callback functions
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

    def on_connect(self, client, userdata, flags, rc):
        """Callback on connection"""
        if rc == 0:
            logging.info(f"Subscriber {self.subscriber_id}: Connected successfully")
            # Subscribe to all environmental topics
            topic_wildcard = f"{ENVIRONMENT_TOPIC_BASE}/#"
            self.client.subscribe(topic_wildcard)
            logging.info(f"Subscriber {self.subscriber_id}: Subscribed to topic: {topic_wildcard}")
            self.statistics.update_stats("active_subscribers")
        else:
            logging.error(f"Subscriber {self.subscriber_id}: Connection failed (RC: {rc})")
            self.statistics.update_stats("errors")

    def on_message(self, client, userdata, msg):
        """Callback on message received"""
        try:
            self.statistics.update_stats("total_received")

            # Parse JSON
            data = json.loads(msg.payload.decode())
            device_id = data.get("id")
            location = data.get("location")
            sensor_type = data.get("sensor_type")
            value = data.get("value")

            # Store statistics
            if device_id not in self.received_messages:
                self.received_messages[device_id] = 0
            self.received_messages[device_id] += 1

            # Log message (limited to avoid console spam)
            if self.statistics.stats["total_received"] % 50 == 0:
                logging.info(f"Subscriber {self.subscriber_id}: Received from Device {device_id} - "
                      f"Location: {location}, Sensor: {sensor_type}, Value: {value}")

        except json.JSONDecodeError:
            logging.error(f"Subscriber {self.subscriber_id}: Failed to parse JSON from {msg.topic}")
            self.statistics.update_stats("errors")
        except Exception as e:
            logging.error(f"Subscriber {self.subscriber_id}: Error - {e}")
            self.statistics.update_stats("errors")

    def on_disconnect(self, client, userdata, rc):
        """Callback on disconnect"""
        self.statistics.update_stats("active_subscribers", -1)

    def run(self):
        """Run subscriber"""
        try:
            self.client.connect(self.broker, self.port, 60)
            logging.info(f"Subscriber {self.subscriber_id}: Listening for messages...")
            self.client.loop_forever()
        except Exception as e:
            logging.error(f"Subscriber {self.subscriber_id}: Error - {e}")
            self.statistics.update_stats("errors")

    def get_summary(self):
        """Get received message summary"""
        return self.received_messages

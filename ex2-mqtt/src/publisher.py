import paho.mqtt.client as mqtt
import logging
import datetime
import random
import json
import time

from utils import Statistics
from constants import (
    ENVIRONMENT_TOPIC_BASE,
    ENVIRONMENT_LOCATIONS,
    ENVIRONMENT_SENSOR_TYPES,
    SENSOR_VALUE_RANGES
)

class DevicePublisher:
    def __init__(self, device_id, broker, port, total_messages_per_device, publish_interval, statistics: Statistics, location=None, sensor_type=None):
        self.device_id = device_id
        self.broker = broker
        self.port = port
        self.total_messages_per_device = total_messages_per_device
        self.publish_interval = publish_interval
        self.statistics = statistics

        self.client = mqtt.Client(client_id=f"publisher_{device_id}")
        
        # Assign location and sensor type
        self.location = location if location else random.choice(ENVIRONMENT_LOCATIONS)
        self.sensor_type = sensor_type if sensor_type else random.choice(ENVIRONMENT_SENSOR_TYPES)
        self.topic = f"{ENVIRONMENT_TOPIC_BASE}/{self.location}/{self.sensor_type}"
        
        self.packet_no = 0
        self.is_connected = False

        # Callback functions
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        self.client.on_disconnect = self.on_disconnect

    def on_connect(self, client, userdata, flags, rc):
        """Callback on connection"""
        if rc == 0:
            self.is_connected = True
            self.statistics.update_stats("active_publishers")
            logging.info(f"Device {self.device_id} ({self.location}/{self.sensor_type}): Connected successfully")
        else:
            logging.error(f"Device {self.device_id} ({self.location}/{self.sensor_type}): Connection failed (RC: {rc})")
            self.statistics.update_stats("errors")

    def on_publish(self, client, userdata, mid):
        """Callback on publish"""
        self.statistics.update_stats("total_published")

    def on_disconnect(self, client, userdata, rc):
        """Callback on disconnect"""
        self.is_connected = False
        self.statistics.update_stats("active_publishers", -1)

    def generate_sensor_data(self):
        """Generate simulated sensor data based on sensor_type"""
        self.packet_no += 1
        min_val, max_val = SENSOR_VALUE_RANGES[self.sensor_type]
        
        # Generate a random value within the defined range for the sensor type
        sensor_value = round(random.uniform(min_val, max_val), 2)

        return {
            "id": self.device_id,
            "location": self.location,
            "sensor_type": self.sensor_type,
            "packet_no": self.packet_no,
            "value": sensor_value,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def publish_data(self):
        """Publish data to broker"""
        try:
            data = self.generate_sensor_data()
            json_data = json.dumps(data)

            result = self.client.publish(self.topic, json_data, qos=1)

            if result.rc != mqtt.MQTT_ERR_SUCCESS:
                logging.error(f"Device {self.device_id} ({self.location}/{self.sensor_type}): Publish failed")
                self.statistics.update_stats("errors")

        except Exception as e:
            logging.error(f"Device {self.device_id} ({self.location}/{self.sensor_type}): Error - {e}")
            self.statistics.update_stats("errors")

    def run(self):
        """Run publisher"""
        try:
            # Connect
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()

            # Wait for connection
            timeout = 10
            start_time = time.time()
            while not self.is_connected and (time.time() - start_time) < timeout:
                time.sleep(0.1)

            if not self.is_connected:
                logging.error(f"Device {self.device_id} ({self.location}/{self.sensor_type}): Connection timeout")
                self.statistics.update_stats("errors")
                return

            # Publish data
            for i in range(self.total_messages_per_device):
                self.publish_data()
                time.sleep(self.publish_interval + random.uniform(-1, 1))

            logging.info(f"Device {self.device_id} ({self.location}/{self.sensor_type}): Finished sending {self.total_messages_per_device} messages")

        except Exception as e:
            logging.error(f"Device {self.device_id} ({self.location}/{self.sensor_type}): Critical error - {e}")
            self.statistics.update_stats("errors")
        finally:
            self.client.loop_stop()
            self.client.disconnect()



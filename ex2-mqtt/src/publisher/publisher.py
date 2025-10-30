import paho.mqtt.client as mqtt
import datetime
import random
import json
import time
import threading
import logging
from typing import Optional, Dict, Any

from src.utils.statistics_utils import Statistics
from src.constants.constants import (
    ENVIRONMENT_TOPIC_BASE,
    ENVIRONMENT_LOCATIONS,
    ENVIRONMENT_SENSOR_TYPES,
    SENSOR_VALUE_RANGES
)
from src.utils.logger_utils import configure_logger

class DevicePublisher:
    """
    Represents a single device that publishes sensor data to an MQTT broker.

    This class handles connecting to the broker, generating simulated sensor data,
    publishing it to a specific topic, and handling the connection lifecycle.
    """

    def __init__(
        self,
        device_id: str,
        broker: str,
        port: int,
        total_messages_per_device: int,
        publish_interval: float,
        statistics: "Statistics",
        location: Optional[str] = None,
        sensor_type: Optional[str] = None,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initializes the DevicePublisher instance.

        Args:
            device_id: A unique identifier for the device.
            broker: The MQTT broker address.
            port: The MQTT broker port.
            total_messages_per_device: The total number of messages to send.
            publish_interval: The base interval between messages in seconds.
            statistics: A Statistics object to record operational metrics.
            location: The physical location of the device. If None, a random one is chosen.
            sensor_type: The type of sensor for the device. If None, a random one is chosen.
            logger: A configured logger instance.
        """
        self.device_id: str = device_id
        self.broker: str = broker
        self.port: int = port
        self.total_messages_per_device: int = total_messages_per_device
        self.publish_interval: float = publish_interval
        self.statistics: "Statistics" = statistics
        self.logger = logger or configure_logger(f'src.publisher_{self.device_id}')

        # Assign location and sensor type, defaulting to random choices if not provided.
        self.location: str = location or random.choice(ENVIRONMENT_LOCATIONS)
        self.sensor_type: str = sensor_type or random.choice(ENVIRONMENT_SENSOR_TYPES)
        
        self.topic: str = f"{ENVIRONMENT_TOPIC_BASE}/{self.location}/{self.sensor_type}"
        self.packet_no: int = 0
        
        # MQTT Client setup
        # Using MQTTv311 is standard. Using a clean session is important for this simulation.
        self.client: mqtt.Client = mqtt.Client(client_id=f"publisher_{self.device_id}", protocol=mqtt.MQTTv311)
        self._setup_callbacks()

        # Use a threading.Event for robust connection synchronization.
        self.connected_event = threading.Event()

    def _setup_callbacks(self) -> None:
        """Assigns callback functions to the MQTT client."""
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        self.client.on_disconnect = self.on_disconnect

    def on_connect(self, client, userdata, flags, rc):
        """Callback invoked upon connection to the MQTT broker."""
        if rc == mqtt.MQTT_ERR_SUCCESS:
            self.logger.info(f"Device {self.device_id} ({self.location}/{self.sensor_type}): Connected successfully")
            self.statistics.update_stats("active_publishers")
            self.connected_event.set()  # Signal that connection is established
        else:
            self.logger.error(f"Device {self.device_id} ({self.location}/{self.sensor_type}): Connection failed (RC: {rc})")
            self.statistics.update_stats("errors")

    def on_publish(self, client, userdata, mid):
        """Callback invoked when a message is successfully published."""
        self.statistics.update_stats("total_published")

    def on_disconnect(self, client, userdata, rc):
        """Callback invoked upon disconnection from the MQTT broker."""
        # A non-zero return code indicates an unexpected disconnect.
        if rc != mqtt.MQTT_ERR_SUCCESS:
            self.logger.warning(
                f"Device {self.device_id} ({self.location}/{self.sensor_type}): "
                f"Unexpectedly disconnected (RC: {rc})."
            )
            self.statistics.update_stats("errors")
        else:
            self.logger.info(f"Device {self.device_id} ({self.location}/{self.sensor_type}): Disconnected cleanly.")

        self.connected_event.clear()  # Reset event on disconnect
        self.statistics.update_stats("active_publishers", -1)

    def _generate_sensor_data(self) -> Dict[str, Any]:
        """Generates a simulated sensor data payload."""
        self.packet_no += 1
        min_val, max_val = SENSOR_VALUE_RANGES[self.sensor_type]
        
        sensor_value = round(random.uniform(min_val, max_val), 2)

        return {
            "id": self.device_id,
            "location": self.location,
            "sensor_type": self.sensor_type,
            "packet_no": self.packet_no,
            "value": sensor_value,
            "timestamp": datetime.datetime.now().isoformat()
        }

    def _publish_data(self) -> None:
        """Generates and publishes a single sensor data message."""
        try:
            payload = self._generate_sensor_data()
            json_payload = json.dumps(payload)

            # Publish with QoS 1 for "at least once" delivery.
            result = self.client.publish(self.topic, json_payload, qos=1)

            if result.rc != mqtt.MQTT_ERR_SUCCESS:
                self.logger.error(
                    f"Device {self.device_id} ({self.location}/{self.sensor_type}): "
                    f"Failed to publish message. MQTT Error: {result.rc}"
                )
                self.statistics.update_stats("errors")

        except Exception as e:
            self.logger.error(
                f"Device {self.device_id} ({self.location}/{self.sensor_type}): "
                f"An exception occurred during publish: {e}"
            )
            self.statistics.update_stats("errors")

    def connect(self) -> bool:
        """
        Connects to the MQTT broker and starts the network loop.

        Returns:
            True if connection is successful within the timeout, False otherwise.
        """
        try:
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()

            # Wait for the on_connect callback to set the event, with a timeout.
            if not self.connected_event.wait(timeout=10.0):
                self.logger.error(f"Device {self.device_id} ({self.location}/{self.sensor_type}): Connection timeout.")
                self.statistics.update_stats("errors")
                self.client.loop_stop()  # Clean up the network loop on failure.
                return False
            
            return True
        except (OSError, ConnectionRefusedError) as e:
            self.logger.error(
                f"Device {self.device_id} ({self.location}/{self.sensor_type}): "
                f"Connection error - {e}"
            )
            self.statistics.update_stats("errors")
            return False

    def disconnect(self) -> None:
        """Disconnects from the broker and stops the network loop."""
        self.client.disconnect()
        self.client.loop_stop()

    def run(self) -> None:
        """
        Executes the full lifecycle of the device publisher:
        connect, publish messages periodically, and disconnect.
        """
        if not self.connect():
            self.logger.error(f"Device {self.device_id}: Halting due to connection failure.")
            return

        try:
            self.logger.info(
                f"Device {self.device_id} ({self.location}/{self.sensor_type}): "
                f"Starting to publish {self.total_messages_per_device} messages."
            )
            for _ in range(self.total_messages_per_device):
                # If disconnected during the loop, stop publishing.
                if not self.connected_event.is_set():
                    self.logger.warning(
                        f"Device {self.device_id} ({self.location}/{self.sensor_type}): "
                        f"Disconnected unexpectedly. Stopping publish loop."
                    )
                    break
                
                self._publish_data()
                
                # Sleep for the interval with a random jitter to prevent thundering herd.
                jitter = random.uniform(-0.1, 0.1) * self.publish_interval
                time.sleep(self.publish_interval + jitter)

            self.logger.info(
                f"Device {self.device_id} ({self.location}/{self.sensor_type}): "
                f"Finished sending messages."
            )

        except Exception as e:
            self.logger.critical(
                f"Device {self.device_id} ({self.location}/{self.sensor_type}): "
                f"A critical error occurred during the run loop: {e}"
            )
            self.statistics.update_stats("errors")
        finally:
            self.logger.info(f"Device {self.device_id}: Shutting down.")
            self.disconnect()
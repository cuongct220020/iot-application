import paho.mqtt.client as mqtt
import json
import threading
import time
import logging
from typing import Dict, Any, Optional

from src.utils.statistics_utils import Statistics
from src.constants.constants import ENVIRONMENT_TOPIC_BASE
from src.utils.logger_utils import configure_logger

class DeviceSubscriber:
    """
    Represents a subscriber client that listens for sensor data from devices.

    Handles connecting to the broker, subscribing to topics, and processing
    incoming messages gracefully.
    """

    def __init__(
        self,
        subscriber_id: str,
        broker: str,
        port: int,
        statistics: "Statistics",
        logger: Optional[logging.Logger] = None
    ):
        """
        Initializes the DeviceSubscriber instance.

        Args:
            subscriber_id: A unique identifier for the subscriber client.
            broker: The MQTT broker address.
            port: The MQTT broker port.
            statistics: A Statistics object to record operational metrics.
            logger: A configured logger instance.
        """
        self.subscriber_id: str = subscriber_id
        self.broker: str = broker
        self.port: int = port
        self.statistics: "Statistics" = statistics
        self.logger = logger or configure_logger(f'src.subscriber_{self.subscriber_id}')

        self.client: mqtt.Client = mqtt.Client(client_id=f"subscriber_{self.subscriber_id}", protocol=mqtt.MQTTv311)
        self._setup_callbacks()

        self.received_messages: Dict[str, int] = {}
        self.connected_event = threading.Event()

    def _setup_callbacks(self) -> None:
        """Assigns callback functions to the MQTT client."""
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

    def on_connect(self, client, userdata, flags, rc):
        """Callback invoked upon connection to the MQTT broker."""
        if rc == 0:
            self.logger.info(f"Subscriber {self.subscriber_id}: Connected successfully")
            self.statistics.update_stats("active_subscribers")
            
            # Subscribe to all environmental topics with QoS 1
            topic_wildcard = f"{ENVIRONMENT_TOPIC_BASE}/#"
            self.client.subscribe(topic_wildcard, qos=1)
            self.logger.info(f"Subscriber {self.subscriber_id}: Subscribed to topic '{topic_wildcard}'")
            
            self.connected_event.set()
        else:
            self.logger.error(f"Subscriber {self.subscriber_id}: Connection failed (RC: {rc})")
            self.statistics.update_stats("errors")

    def on_message(self, client, userdata, msg):
        """Callback invoked when a message is received."""
        try:
            self.statistics.update_stats("total_received")
            payload = msg.payload.decode()
            data = json.loads(payload)

            device_id = data.get("id", "unknown_device")
            
            # Store statistics for received messages
            self.received_messages[device_id] = self.received_messages.get(device_id, 0) + 1

            # Log a message periodically to avoid spamming the console
            if self.statistics.stats["total_received"] % 100 == 0:
                self.logger.info(
                    f"Subscriber {self.subscriber_id}: Received message #{self.statistics.stats['total_received']} "
                    f"from {device_id} on topic {msg.topic}"
                )

        except json.JSONDecodeError:
            self.logger.error(f"Subscriber {self.subscriber_id}: Failed to parse JSON from topic {msg.topic}")
            self.statistics.update_stats("errors")
        except Exception as e:
            self.logger.error(f"Subscriber {self.subscriber_id}: Error processing message - {e}")
            self.statistics.update_stats("errors")

    def on_disconnect(self, client, userdata, rc):
        """Callback invoked upon disconnection from the MQTT broker."""
        if rc != mqtt.MQTT_ERR_SUCCESS:
            self.logger.warning(f"Subscriber {self.subscriber_id}: Unexpectedly disconnected (RC: {rc}).")
            self.statistics.update_stats("errors")
        else:
            self.logger.info(f"Subscriber {self.subscriber_id}: Disconnected cleanly.")
            
        self.connected_event.clear()
        self.statistics.update_stats("active_subscribers", -1)

    def connect(self) -> bool:
        """
        Connects to the MQTT broker and starts the network loop.

        Returns:
            True if connection is successful within the timeout, False otherwise.
        """
        try:
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()

            if not self.connected_event.wait(timeout=10.0):
                self.logger.error(f"Subscriber {self.subscriber_id}: Connection timeout.")
                self.statistics.update_stats("errors")
                self.client.loop_stop()
                return False
            
            return True
        except (OSError, ConnectionRefusedError) as e:
            self.logger.error(f"Subscriber {self.subscriber_id}: Connection error - {e}")
            self.statistics.update_stats("errors")
            return False

    def disconnect(self) -> None:
        """Disconnects from the broker and stops the network loop."""
        self.logger.info(f"Subscriber {self.subscriber_id}: Disconnecting...")
        self.client.disconnect()
        self.client.loop_stop()

    def run(self) -> None:
        """
        Runs the subscriber, listening for messages until interrupted.
        This is a blocking call that will run until a KeyboardInterrupt.
        """
        if not self.connect():
            self.logger.critical(f"Subscriber {self.subscriber_id}: Halting due to connection failure.")
            return

        self.logger.info(f"Subscriber {self.subscriber_id}: Listening for messages... Press Ctrl+C to stop.")
        
        try:
            # Keep the main thread alive while the background loop processes messages.
            while self.connected_event.is_set():
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.info(f"Subscriber {self.subscriber_id}: Shutdown signal received.")
        finally:
            self.disconnect()

    def get_summary(self) -> Dict[str, int]:
        """Returns a summary of received messages per device."""
        return self.received_messages

import paho.mqtt.client as mqtt
import time
from typing import Any

from src.constants.constants import BROKER, PORT
from src.utils.logger_utils import configure_logger

logger = configure_logger('src.misc.check_broker_connection', log_file_name='general.log')

from src.constants.constants import (
    MQTT_RC_SUCCESS,
    MQTT_RC_UNACCEPTABLE_PROTOCOL_VERSION,
    MQTT_RC_INVALID_CLIENT_ID,
    MQTT_RC_SERVER_UNAVAILABLE,
    MQTT_RC_BAD_USERNAME_OR_PASSWORD,
    MQTT_RC_NOT_AUTHORIZED
)

def check_broker_connection(broker_address: str, port: int) -> bool:
    """
    Tests the connection to the MQTT broker.

    Args:
        broker_address: The address of the MQTT broker.
        port: The port of the MQTT broker.

    Returns:
        True if the connection is successful, False otherwise.
    """
    connected_flag = False

    def on_connect(client: mqtt.Client, userdata: Any, flags: dict, rc: int) -> None:
        nonlocal connected_flag
        if rc == MQTT_RC_SUCCESS:
            logger.info("Successfully connected to MQTT broker.")
            logger.info("Broker is running normally.")
            connected_flag = True
            client.disconnect()
        else:
            logger.error(f"Connection failed with error code: {rc}")
            logger.error("Common error codes:")
            if rc == MQTT_RC_UNACCEPTABLE_PROTOCOL_VERSION:
                logger.error("  1: Connection refused - incorrect protocol version")
            elif rc == MQTT_RC_INVALID_CLIENT_ID:
                logger.error("  2: Connection refused - invalid client identifier")
            elif rc == MQTT_RC_SERVER_UNAVAILABLE:
                logger.error("  3: Connection refused - server unavailable")
            elif rc == MQTT_RC_BAD_USERNAME_OR_PASSWORD:
                logger.error("  4: Connection refused - bad username or password")
            elif rc == MQTT_RC_NOT_AUTHORIZED:
                logger.error("  5: Connection refused - not authorized")
            else:
                logger.error(f"  {rc}: Unknown connection refused error")
            connected_flag = False

    client = mqtt.Client(client_id="test_client")
    client.on_connect = on_connect

    try:
        logger.info(f"Attempting to connect to broker at {broker_address}:{port}...")
        client.connect(broker_address, port, 60)
        client.loop_start()
        time.sleep(3)  # Allow time for connection and on_connect callback
        client.loop_stop()
        return connected_flag
    except ConnectionRefusedError:
        logger.error("Connection refused. Ensure the broker is running and accessible.")
        return False
    except Exception as e:
        logger.error(f"An unexpected error occurred during connection attempt: {e}")
        logger.error("Suggestions:")
        logger.error("  - Check if the broker is running.")
        logger.error("  - Verify the IP address and port.")
        logger.error("  - Check firewall settings.")
        return False


if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("MQTT BROKER CONNECTION CHECK")
    logger.info("=" * 60)
    logger.info(f"Broker: {BROKER}:{PORT}\n")

    logger.info("Step 1: Basic connection test")
    connection_successful = check_broker_connection(BROKER, PORT)

    if connection_successful:
        logger.info("\n" + "=" * 60)
        logger.info("Step 2: EMQX Broker Information")
        logger.info("=" * 60)
        logger.info("\nCheck EMQX Dashboard:")
        logger.info("  - Dashboard: http://localhost:18083")
        logger.info("  - Username: admin")
        logger.info("  - Password: public")
        logger.info("  - Review: Connections, Subscriptions, Topics")
        logger.info("=" * 60)
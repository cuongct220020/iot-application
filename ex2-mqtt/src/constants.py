
# MQTT Broker
BROKER = "localhost"
PORT = 1883

# Environment Monitoring Topics
ENVIRONMENT_TOPIC_BASE = "iot/environment"
ENVIRONMENT_LOCATIONS = ["city_center", "park_north", "industrial_zone", "street_123"]
ENVIRONMENT_SENSOR_TYPES = ["temperature", "humidity", "pressure", "air_quality"]

# Sensor Value Ranges
SENSOR_VALUE_RANGES = {
    "temperature": (20.0, 40.0),  # Celsius
    "humidity": (40.0, 90.0),     # Percentage
    "pressure": (900.0, 1100.0),  # hPa
    "air_quality": (0.0, 500.0)   # AQI
}

# Simulation
NUM_PUBLISHERS = 100
TOTAL_MESSAGES_PER_DEVICE = 10
PUBLISH_INTERVAL = 5  # seconds
NUM_SUBSCRIBERS = 3 # Number of subscribers

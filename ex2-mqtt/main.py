import logging
import argparse

from src.simulation import Simulation
from src.constants import (
    BROKER,
    PORT,
    NUM_PUBLISHERS,
    ENVIRONMENT_TOPIC_BASE,
    NUM_SUBSCRIBERS
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_args():
    parser = argparse.ArgumentParser(description="MQTT IoT Device Simulation")
    parser.add_argument(
        "--publisher-configs",
        nargs='*',
        help="Specify publisher configurations as 'location,sensor_type' pairs. E.g., --publisher-configs city_center,humidity park_north,air_quality"
    )
    return parser.parse_args()

def main():
    args = parse_args()

    print("=" * 70)
    logging.info("100 MQTT DEVICES SIMULATION PROGRAM")
    print("=" * 70)
    logging.info(f"Broker: {BROKER}:{PORT}")
    logging.info(f"Number of publishers: {NUM_PUBLISHERS}")
    logging.info(f"Number of subscribers: {NUM_SUBSCRIBERS}")
    logging.info(f"Topic pattern: {ENVIRONMENT_TOPIC_BASE}/{{location}}/{{sensor_type}}")
    print("=" * 70)

    simulation = Simulation()

    # Process publisher configurations from CLI
    publisher_configs = []
    if args.publisher_configs:
        for config_str in args.publisher_configs:
            parts = config_str.split(',')
            if len(parts) == 2:
                publisher_configs.append((parts[0].strip(), parts[1].strip()))
            else:
                logging.warning(f"Invalid publisher config format: {config_str}. Expected 'location,sensor_type'. Skipping.")

    while True:
        logging.info("\nMENU:")
        logging.info("1. Run Full Simulation (Subscriber + Publishers)")
        logging.info("2. Run Publishers Only")
        logging.info("3. Run Subscriber Only")
        logging.info("4. Exit")
        if publisher_configs:
            logging.info(f"   (Using custom publisher configs: {publisher_configs})")

        choice = input("\nSelect an option (1-4): ").strip()

        if choice == "1":
            simulation.run_full_simulation(publisher_configs if publisher_configs else None)

        elif choice == "2":
            simulation.run_publishers_only(publisher_configs if publisher_configs else None)

        elif choice == "3":
            simulation.run_subscriber_only()

        elif choice == "4":
            logging.info("\nGoodbye!")
            break
        else:
            logging.warning("\nInvalid choice!")


if __name__ == "__main__":
    main()
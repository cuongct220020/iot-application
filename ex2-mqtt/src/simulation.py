import threading
import time
import logging
import math

from publisher import DevicePublisher
from subscriber import DeviceSubscriber
from utils import Statistics
from constants import (
    BROKER,
    PORT,
    NUM_PUBLISHERS,
    TOTAL_MESSAGES_PER_DEVICE,
    PUBLISH_INTERVAL,
    NUM_SUBSCRIBERS,
    ENVIRONMENT_TOPIC_BASE
)

class Simulation:
    def __init__(self):
        self.statistics = Statistics()
        self.subscribers = []
        self.monitor_thread = None

    def _run_subscribers(self):
        """Run multiple subscribers in separate threads"""
        subscriber_threads = []
        for i in range(1, NUM_SUBSCRIBERS + 1):
            subscriber = DeviceSubscriber(
                i,
                BROKER, PORT, self.statistics
            )
            self.subscribers.append(subscriber)
            subscriber_thread = threading.Thread(target=subscriber.run, daemon=True)
            subscriber_threads.append(subscriber_thread)
            subscriber_thread.start()
        return self.subscribers

    def _run_publishers(self, publisher_configs=None):
        """Run all publishers in separate threads, with optional configurations"""
        logging.info(f"\nStarting simulation for {NUM_PUBLISHERS} devices...")
        logging.info(
            f"Each device sends {TOTAL_MESSAGES_PER_DEVICE} messages, every {PUBLISH_INTERVAL}s"
        )
        logging.info(f"Publishing to topics under: {ENVIRONMENT_TOPIC_BASE}/{{location}}/{{sensor_type}}")

        publishers = []
        threads = []

        if publisher_configs:
            # Distribute publishers based on provided configurations
            num_configs = len(publisher_configs)
            publishers_per_config = math.ceil(NUM_PUBLISHERS / num_configs)
            
            device_id_counter = 1
            for config_index, (location, sensor_type) in enumerate(publisher_configs):
                for _ in range(publishers_per_config):
                    if device_id_counter > NUM_PUBLISHERS:
                        break
                    publisher = DevicePublisher(
                        device_id_counter,
                        BROKER,
                        PORT,
                        TOTAL_MESSAGES_PER_DEVICE,
                        PUBLISH_INTERVAL,
                        self.statistics,
                        location=location,
                        sensor_type=sensor_type
                    )
                    publishers.append(publisher)

                    thread = threading.Thread(target=publisher.run, daemon=True)
                    threads.append(thread)
                    thread.start()

                    device_id_counter += 1
                    time.sleep(0.05) # Small delay to avoid overload
                if device_id_counter > NUM_PUBLISHERS:
                    break
        else:
            # Randomly assign location and sensor type (default behavior)
            for i in range(1, NUM_PUBLISHERS + 1):
                publisher = DevicePublisher(
                    i,
                    BROKER,
                    PORT,
                    TOTAL_MESSAGES_PER_DEVICE,
                    PUBLISH_INTERVAL,
                    self.statistics,
                )
                publishers.append(publisher)

                thread = threading.Thread(target=publisher.run, daemon=True)
                threads.append(thread)
                thread.start()

                # Small delay to avoid overload
                time.sleep(0.05)

        logging.info(f"Started {NUM_PUBLISHERS} publishers\n")

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        logging.info("\nAll publishers finished!")

    def _monitor_stats(self):
        """Print statistics periodically"""
        while True:
            time.sleep(10)
            self.statistics.print_stats()

    def run_full_simulation(self, publisher_configs=None):
        logging.info("RUNNING FULL SIMULATION")

        # Start subscribers first
        self._run_subscribers()
        time.sleep(2)  # Wait for subscribers to be ready

        # Start monitor
        self.monitor_thread = threading.Thread(target=self._monitor_stats, daemon=True)
        self.monitor_thread.start()

        # Run publishers
        self._run_publishers(publisher_configs)

        # Wait for all messages to be received
        logging.info("\nWaiting for all messages to be received...")
        time.sleep(10)

        # Print final results
        self.statistics.print_stats()
        if self.subscribers:
            logging.info("\nSUMMARY BY DEVICE (from first subscriber):")
            # For simplicity, we'll get summary from the first subscriber
            # In a real scenario, you might aggregate summaries from all subscribers
            summary = self.subscribers[0].get_summary()
            for device_id in sorted(summary.keys()):
                logging.info(f"  Device {device_id:3d}: Received {summary[device_id]:3d} messages")

        logging.info("\nSimulation complete!")

    def run_publishers_only(self, publisher_configs=None):
        logging.info("RUNNING PUBLISHERS ONLY")
        self._run_publishers(publisher_configs)
        self.statistics.print_stats()

    def run_subscriber_only(self):
        logging.info("RUNNING SUBSCRIBER ONLY")
        self._run_subscribers()
        self.monitor_thread = threading.Thread(target=self._monitor_stats, daemon=True)
        self.monitor_thread.start()

        try:
            logging.info("Listening... (Press Ctrl+C to stop)")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logging.info("\nSubscribers stopped")

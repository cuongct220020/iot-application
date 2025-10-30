import threading
import time
import math
from datetime import datetime

from src.publisher.publisher import DevicePublisher
from src.subscriber.subscriber import DeviceSubscriber
from src.utils.statistics_utils import Statistics
from src.constants.constants import (
    BROKER,
    PORT,
    TOTAL_MESSAGES_PER_DEVICE,
    PUBLISH_INTERVAL,
    ENVIRONMENT_TOPIC_BASE
)
from src.utils.logger_utils import configure_logger

class Simulation:
    def __init__(self):
        self.statistics = Statistics()
        self.subscribers = []
        self.monitor_thread = None
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.general_logger = configure_logger('src.simulation', log_file_name=f"general_activity_{self.timestamp}.log")

    def _run_subscribers(self, num_subscribers):
        """Run multiple subscribers in separate threads"""
        subscriber_threads = []
        for i in range(1, num_subscribers + 1):
            subscriber_logger = configure_logger(f'src.subscriber_{i}', log_file_name=f"subscriber_activity_{self.timestamp}.log")
            subscriber = DeviceSubscriber(
                i, BROKER, PORT, self.statistics, logger=subscriber_logger
            )
            self.subscribers.append(subscriber)
            subscriber_thread = threading.Thread(target=subscriber.run, daemon=True)
            subscriber_threads.append(subscriber_thread)
            subscriber_thread.start()
        return self.subscribers

    def _run_publishers(self, num_publishers, publisher_configs=None):
        """Run all publishers in separate threads, with optional configurations"""
        self.general_logger.info(f"\nStarting simulation for {num_publishers} devices...")
        self.general_logger.info(
            f"Each device sends {TOTAL_MESSAGES_PER_DEVICE} messages, every {PUBLISH_INTERVAL}s"
        )
        self.general_logger.info(f"Publishing to topics under: {ENVIRONMENT_TOPIC_BASE}/{{location}}/{{sensor_type}}")

        publishers = []
        threads = []

        if publisher_configs:
            # Distribute publishers based on provided configurations
            num_configs = len(publisher_configs)
            publishers_per_config = math.ceil(num_publishers / num_configs)
            
            device_id_counter = 1
            for config_index, (location, sensor_type) in enumerate(publisher_configs):
                for _ in range(publishers_per_config):
                    if device_id_counter > num_publishers:
                        break
                    publisher_logger = configure_logger(f'src.publisher_{device_id_counter}', log_file_name=f"publisher_activity_{self.timestamp}.log")
                    publisher = DevicePublisher(
                        device_id_counter,
                        BROKER,
                        PORT,
                        TOTAL_MESSAGES_PER_DEVICE,
                        PUBLISH_INTERVAL,
                        self.statistics,
                        location=location,
                        sensor_type=sensor_type,
                        logger=publisher_logger
                    )
                    publishers.append(publisher)

                    thread = threading.Thread(target=publisher.run, daemon=True)
                    threads.append(thread)
                    thread.start()

                    device_id_counter += 1
                    time.sleep(0.05) # Small delay to avoid overload
                if device_id_counter > num_publishers:
                    break
        else:
            # Randomly assign location and sensor type (default behavior)
            for i in range(1, num_publishers + 1):
                publisher_logger = configure_logger(f'src.publisher_{i}', log_file_name=f"publisher_activity_{self.timestamp}.log")
                publisher = DevicePublisher(
                    i,
                    BROKER,
                    PORT,
                    TOTAL_MESSAGES_PER_DEVICE,
                    PUBLISH_INTERVAL,
                    self.statistics,
                    logger=publisher_logger
                )
                publishers.append(publisher)

                thread = threading.Thread(target=publisher.run, daemon=True)
                threads.append(thread)
                thread.start()

                # Small delay to avoid overload
                time.sleep(0.05)

        self.general_logger.info(f"Started {num_publishers} publishers\n")

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        self.general_logger.info("\nAll publishers finished!")

    def _monitor_stats(self):
        """Print statistics periodically"""
        stats_logger = configure_logger('src.statistics', log_file_name=f"statistics_updates_{self.timestamp}.log")
        while True:
            time.sleep(10)
            self.statistics.print_stats(logger=stats_logger)

    def run_full_simulation(self, num_publishers, num_subscribers, publisher_configs=None):
        self.general_logger.info("RUNNING FULL SIMULATION")

        # Start subscribers first
        self._run_subscribers(num_subscribers)
        time.sleep(2)  # Wait for subscribers to be ready

        # Start monitor
        self.monitor_thread = threading.Thread(target=self._monitor_stats, daemon=True)
        self.monitor_thread.start()

        # Run publishers
        self._run_publishers(num_publishers, publisher_configs)

        # Wait for all messages to be received
        self.general_logger.info("\nWaiting for all messages to be received...")
        time.sleep(10)

        # Print final results
        stats_logger = configure_logger('src.final_statistics', log_file_name=f"statistics_updates_{self.timestamp}.log")
        self.statistics.print_stats(logger=stats_logger)
        if self.subscribers:
            self.general_logger.info("\nSUMMARY BY DEVICE (from first subscriber):")
            # For simplicity, we'll get summary from the first subscriber
            # In a real scenario, you might aggregate summaries from all subscribers
            summary = self.subscribers[0].get_summary()
            for device_id in sorted(summary.keys()):
                self.general_logger.info(f"  Device {device_id:3d}: Received {summary[device_id]:3d} messages")

        self.general_logger.info("\nSimulation complete!")

    def run_publishers_only(self, num_publishers, publisher_configs=None):
        self.general_logger.info("RUNNING PUBLISHERS ONLY")
        self._run_publishers(num_publishers, publisher_configs)
        stats_logger = configure_logger('src.final_statistics', log_file_name=f"statistics_updates_{self.timestamp}.log")
        self.statistics.print_stats(logger=stats_logger)

    def run_subscriber_only(self, num_subscribers):
        self.general_logger.info("RUNNING SUBSCRIBER ONLY")
        self._run_subscribers(num_subscribers)
        self.monitor_thread = threading.Thread(target=self._monitor_stats, daemon=True)
        self.monitor_thread.start()

        try:
            self.general_logger.info("Listening... (Press Ctrl+C to stop)")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.general_logger.info("\nSubscribers stopped")

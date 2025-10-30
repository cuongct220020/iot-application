import logging
import threading
from src.utils.logger_utils import configure_logger

# Get a logger specifically for statistics
stats_logger = configure_logger('statistics', log_file_name='statistics.log')

class Statistics:
    def __init__(self):
        self.stats = {
            "total_published": 0,
            "total_received": 0,
            "active_publishers": 0,
            "active_subscribers": 0,
            "errors": 0
        }
        self.lock = threading.Lock()

    def update_stats(self, key, value=1):
        """Update thread-safe statistics"""
        with self.lock:
            self.stats[key] += value

    def print_stats(self, logger=stats_logger):
        """Print statistics"""
        with self.lock:
            print("\n" + "=" * 70)
            stats_logger.info("REAL-TIME STATISTICS")
            print("=" * 70)
            stats_logger.info(f"Total messages published: {self.stats['total_published']}")
            stats_logger.info(f"Total messages received:  {self.stats['total_received']}")
            stats_logger.info(f"Active publishers:        {self.stats['active_publishers']}")
            stats_logger.info(f"Active subscribers:       {self.stats['active_subscribers']}")
            stats_logger.info(f"Errors:                   {self.stats['errors']}")
            print("=" * 70 + "\n")

    def get_stats(self):
        """Get current statistics"""
        with self.lock:
            return self.stats.copy()
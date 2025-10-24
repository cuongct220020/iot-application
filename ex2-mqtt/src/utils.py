import logging
import threading

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

    def print_stats(self):
        """Print statistics"""
        with self.lock:
            print("\n" + "=" * 70)
            logging.info("REAL-TIME STATISTICS")
            print("=" * 70)
            logging.info(f"Total messages published: {self.stats['total_published']}")
            logging.info(f"Total messages received:  {self.stats['total_received']}")
            logging.info(f"Active publishers:        {self.stats['active_publishers']}")
            logging.info(f"Active subscribers:       {self.stats['active_subscribers']}")
            logging.info(f"Errors:                   {self.stats['errors']}")
            print("=" * 70 + "\n")

    def get_stats(self):
        """Get current statistics"""
        with self.lock:
            return self.stats.copy()
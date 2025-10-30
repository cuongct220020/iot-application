import click
from datetime import datetime

from src.simulation import Simulation
from src.constants.constants import (
    BROKER,
    PORT,
    ENVIRONMENT_TOPIC_BASE
)
from src.utils.logger_utils import configure_logger


@click.command()
@click.option('--publishers', default=100, help='Number of publisher devices to simulate.', show_default=True)
@click.option('--subscribers', default=3, help='Number of subscriber clients to simulate.', show_default=True)
@click.option('--mode', type=click.Choice(['full', 'pub-only', 'sub-only'], case_sensitive=False), default='full', help='The simulation mode to run.', show_default=True)
def run(publishers, subscribers, mode):
    """Runs a simulation of MQTT IoT devices."""
    simulation = Simulation()
    logger = configure_logger('cli.commands', log_file_name=f"general_activity_{simulation.timestamp}.log")

    logger.info("=" * 70)
    logger.info("MQTT DEVICES SIMULATION PROGRAM")
    logger.info("=" * 70)
    logger.info(f"Broker: {BROKER}:{PORT}")
    logger.info(f"Mode: {mode}")

    if mode in ('full', 'pub-only'):
        logger.info(f"Number of publishers: {publishers}")
    if mode in ('full', 'sub-only'):
        logger.info(f"Number of subscribers: {subscribers}")
    
    logger.info(f"Topic pattern: {ENVIRONMENT_TOPIC_BASE}/{{location}}/{{sensor_type}}")
    logger.info("=" * 70)

    if mode == 'full':
        simulation.run_full_simulation(num_publishers=publishers, num_subscribers=subscribers)
    elif mode == 'pub-only':
        simulation.run_publishers_only(num_publishers=publishers)
    elif mode == 'sub-only':
        simulation.run_subscriber_only(num_subscribers=subscribers)
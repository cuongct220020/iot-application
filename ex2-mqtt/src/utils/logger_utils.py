import logging
import os

def configure_logger(name="mqtt_app", level=logging.INFO, log_file_name=None):
    """
    Configures a logger to write to the console and optionally to a file.

    Args:
        name (str): The name of the logger.
        level (int): The logging level.
        log_file_name (str, optional): The name of the file to log to. Defaults to None.

    Returns:
        logging.Logger: The configured logger.
    """
    logger = logging.getLogger(name)
    
    # Prevent adding duplicate handlers to the same logger instance
    if logger.handlers:
        return logger
        
    logger.setLevel(level)

    # Define a more structured and informative log format
    log_format = '[%(asctime)s] [%(levelname)s] [%(name)s:%(lineno)d] - %(message)s'
    formatter = logging.Formatter(log_format)

    # --- Console Handler ---
    # Always log to the console for immediate feedback
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # --- File Handler (Optional) ---
    # If a log file name is provided, add a file handler
    if log_file_name:
        logs_dir = "logs"
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)

        file_path = os.path.join(logs_dir, log_file_name)

        # Use 'a' mode to append to the log file if it already exists
        file_handler = logging.FileHandler(file_path, mode='a', encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

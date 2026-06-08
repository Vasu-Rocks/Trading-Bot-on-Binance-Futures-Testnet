import logging
import sys
from pathlib import Path

def setup_logging():
    # Anchor the log file relative to the project root
    log_file = Path(__file__).parent.parent / "trading_bot.log"
    
    logger = logging.getLogger("trading_bot")
    logger.setLevel(logging.DEBUG)
    
    # Avoid adding handlers multiple times
    if logger.hasHandlers():
        return logger

    formatter = logging.Formatter("%(asctime)s | %(levelname)-8s | %(module)s | %(message)s")
    
    # File Handler (Audit Trail)
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    # Console Handler (User Experience)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logging()

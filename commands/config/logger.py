
# commands/config/logger.py
import logging

# =============== LOGGING SETUP

# configure basic logging settings
logging.basicConfig(
    # set default log level to INFO
    level=logging.INFO,
    # set the log message format
    format="%(levelname)s: %(message)s."
)
# create a logger instance for this module
logger = logging.getLogger(__name__)
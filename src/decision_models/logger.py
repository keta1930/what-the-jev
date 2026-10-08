"""Console logging setup for CLI runs; library use keeps the host's logging config."""

import logging
import sys

LOG_FORMAT = '%(asctime)s %(levelname)s %(name)s: %(message)s'


def configure_logging(level: int = logging.INFO) -> None:
    """Configure console logging for a standalone run, keeping existing handlers and level."""
    logger = logging.getLogger('decision_models')
    if logger.hasHandlers():
        return
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt='%H:%M:%S'))
    logger.addHandler(handler)
    logger.setLevel(level)
    logger.propagate = False

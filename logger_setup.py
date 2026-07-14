"""
One place to configure logging for the whole app.

Why a rotating file handler: a plain FileHandler grows forever. In a
long-running production process that becomes a disk-space problem you won't
notice until it's a real problem. RotatingFileHandler caps it automatically.
"""

import logging
import os
from logging.handlers import RotatingFileHandler

from config import Config


def setup_logging(app):
    log_dir = os.path.dirname(Config.LOG_FILE)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = RotatingFileHandler(
        Config.LOG_FILE, maxBytes=1_000_000, backupCount=3
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    level = getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO)

    # Attach to the ROOT logger, not just app.logger. database.py and the
    # route blueprints each do `logging.getLogger(__name__)` — those are
    # separate logger objects that only pick up output if the root logger
    # (their common ancestor) has handlers. Attaching only to app.logger
    # was silently dropping every log line from database.py.
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    # Quiet down Werkzeug's per-request access log noise in production,
    # but keep it in debug so you can see requests while developing.
    if not app.debug:
        logging.getLogger("werkzeug").setLevel(logging.WARNING)

    return app.logger

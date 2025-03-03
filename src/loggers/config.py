import json
import logging
import logging.config
from pathlib import Path

from .formats import FORMATS

# Path to the JSON logging configuration file
LOG_CONFIG_FILE = Path(__file__).parent / "config.json"


class ColorizedFormatter(logging.Formatter):
    """Formatter for colorized log messages"""

    def format(self, record: logging.LogRecord) -> str:
        """Formats the log record with color based on the log level"""
        log_fmt = FORMATS.get(record.levelno, FORMATS[logging.INFO])
        formatter = logging.Formatter(log_fmt, "%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


class JSONFormatter(logging.Formatter):
    """Formatter for JSONL logs"""

    def format(self, record: logging.LogRecord) -> str:
        """Formats the log record as a JSON string."""
        log_entry = {
            "timestamp": self.formatTime(record, "%Y-%m-%d %H:%M:%S"),
            "level": record.levelname,
            "module": record.module,
            "message": record.getMessage(),
        }
        return json.dumps(log_entry, ensure_ascii=False)


def setup():
    """Loads the logging configuration and creates necessary directories"""
    with open(LOG_CONFIG_FILE, "r", encoding="utf8") as f:
        config = json.load(f)

    # Extract log file paths and create directories if they don't exist
    log_dirs = set(
        Path(handler["filename"]).parent
        for handler in config.get("handlers", {}).values()
        if "filename" in handler
    )
    for log_dir in log_dirs:
        log_dir.mkdir(parents=True, exist_ok=True)

    logging.config.dictConfig(config)
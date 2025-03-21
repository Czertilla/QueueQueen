import json
import logging
import logging.config
from pathlib import Path
import sys
import traceback
from html import escape

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
        if record.exc_info:
            log_entry["exception"] = {
                "type": str(record.exc_info[0].__name__),  # Название исключения
                "message": str(record.exc_info[1]),  # Текст ошибки
                "traceback": "".join(traceback.format_exception(*record.exc_info))  # Полный traceback
            }
        return json.dumps(log_entry, ensure_ascii=False)
    

class TGFormatter(logging.Formatter):

    def format(self, record: logging.LogRecord) -> str:
        return f"""
<b>timestamp</b>: <code>{self.formatTime(record, "%Y-%m-%d %H:%M:%S")}</code>
<b>logger</b>: {record.name}
<b>module</b>: {record.module}
<b>message</b>: {record.getMessage()}
<b>exception_type</b>: {"" if record.exc_info is None else record.exc_info[0].__name__}
<b>exception_message</b>: { "" if record.exc_info is None else record.exc_info[1]}
    """


def handle_exception(exc_type, exc_value, exc_traceback):
    """Глобальный обработчик необработанных исключений."""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    # Получаем последнюю точку, где произошла ошибка
    tb_last_frame = traceback.extract_tb(exc_traceback)[-1]  # Последний кадр

    logging.critical(
        f"Unhandled exception in {tb_last_frame.filename}:{tb_last_frame.lineno}",
        exc_info=(exc_type, exc_value, exc_traceback)
    )

sys.excepthook = handle_exception

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

import json
import logging
import logging.config
from pathlib import Path
from .formats import FORMATS

# Путь к JSON-конфигурации логирования
LOG_CONFIG_FILE = Path(__file__).parent / "config.json"

class ColorizedFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_fmt = FORMATS.get(record.levelno, FORMATS[logging.INFO])
        formatter = logging.Formatter(log_fmt, "%Y-%m-%d %H:%M:%S")
        return formatter.format(record)

class JSONFormatter(logging.Formatter):
    """Форматтер для JSONL логов (без лишних пробелов)."""
    
    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": self.formatTime(record, "%Y-%m-%d %H:%M:%S"),
            "level": record.levelname,
            "module": record.module,
            "message": record.getMessage(),
        }
        return json.dumps(log_entry, ensure_ascii=False)

def setup():
    """Загружает конфигурацию логирования и создаёт нужные папки."""
    with open(LOG_CONFIG_FILE, "r", encoding="utf8") as f:
        config = json.load(f)

    # Извлекаем пути к файлам логов и создаём папки, если их нет
    log_dirs = set(Path(handler["filename"]).parent for handler in config.get("handlers", {}).values() if "filename" in handler)
    for log_dir in log_dirs:
        log_dir.mkdir(parents=True, exist_ok=True)

    logging.config.dictConfig(config)

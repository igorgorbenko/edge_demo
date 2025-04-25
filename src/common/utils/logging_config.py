import logging
import sys
from datetime import datetime

class CustomFormatter(logging.Formatter):
    """Кастомный форматтер для логов с цветами и расширенной информацией"""
    
    # Цвета для разных уровней логирования
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    
    # Формат: [Время] [Уровень] [Файл:Строка в методе] Сообщение
    format_str = "%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d in %(funcName)s] %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format_str + reset,
        logging.INFO: grey + format_str + reset,
        logging.WARNING: yellow + format_str + reset,
        logging.ERROR: red + format_str + reset,
        logging.CRITICAL: bold_red + format_str + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)

def setup_logging(service_name: str, level: int = logging.INFO):
    """Настройка логгера с кастомным форматтером"""
    
    logger = logging.getLogger(service_name)
    logger.setLevel(level)

    # Обработчик для вывода в консоль
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(CustomFormatter())
    
    # Очищаем существующие обработчики и добавляем новый
    logger.handlers.clear()
    logger.addHandler(console_handler)
    
    return logger 
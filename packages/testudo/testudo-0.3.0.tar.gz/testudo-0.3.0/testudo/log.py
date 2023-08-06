from sys import stdout

from loguru import logger as log


config = {
    "handlers": [
        {"sink": stdout, "colorize": True, "level": "INFO",
         "format": "{time} | <level>{level} | {message}</level>"}
    ]
}
log.configure(**config)

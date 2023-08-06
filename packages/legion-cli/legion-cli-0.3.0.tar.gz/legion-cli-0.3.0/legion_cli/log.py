from sys import stdout

from loguru import logger as log


config = {
    "handlers": [
        {"sink": stdout, "colorize": True, "level": "INFO",
         "format": "{time} | <level>{level} | [{extra[rmq_server]}] {message}</level>"}
    ],
    "extra": {"rmq_server": ""}
}
log.configure(**config)

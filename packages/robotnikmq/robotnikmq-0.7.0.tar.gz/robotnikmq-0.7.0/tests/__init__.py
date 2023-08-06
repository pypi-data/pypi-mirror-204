from sys import stdout

from robotnikmq import log

config = {
    "handlers": [
        {"sink": stdout, "colorize": True, "filter": "robotnikmq", "level": "DEBUG",
         "format": "{time} | <level>{level} | {file.path}:{line}[{extra[rmq_server]}] {message}</level>"},
    ],
    "extra": {"rmq_server": ""}
}

log.configure(**config)
log.enable("robotnikmq")

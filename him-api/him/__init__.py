import logging.config

LOGGING_CONF = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"default": {"level": "INFO", "class": "logging.StreamHandler"}},
    "loggers": {
        "": {  # root logger
            "handlers": ["default"],
            "level": "WARNING",
            "propagate": False,
        },
        "him": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

logging.config.dictConfig(LOGGING_CONF)

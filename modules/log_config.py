LOG_LEVEL: str = "DEBUG"
FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging_config = {
    "version": 1, # mandatory field
    # if you want to overwrite existing loggers' configs
    "disable_existing_loggers": False,
    "formatters": {
        "basic": {
            "format": FORMAT,
        }
    },
    "handlers": {
        "console": {
            "formatter": "basic",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
            "level": LOG_LEVEL,
        }
    },
    "loggers": {
        "api": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "search": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "importer": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "runner": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": False,
        }
    },
}

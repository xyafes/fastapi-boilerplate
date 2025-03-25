import uvloop
import logging
from os import environ
from logging.handlers import RotatingFileHandler

# URI for websockets connection
uri = environ.get("URI")

# Auth token for websockets authentication
auth = environ.get("AUTH")

# Token for the API
token = f"Token {environ.get("TOKEN")}"

# Debug mode
debug = bool(environ.get("DEBUG", 1))

# Broker URL for celery
broker_url = environ.get("BROKER_URL")

# Log path
log_path = "/opt/logs/app.log"

# Configure logging and write logs to the console and local file
log_formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

# Rotating file handler (5MB per file, keep last 5 backups)
log_handler = RotatingFileHandler(log_path, maxBytes=5 * 1024 * 1024, backupCount=5)
log_handler.setFormatter(log_formatter)


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(log_handler)
    return logger


# Create loggers for different components
fastapi_logger = get_logger("fastapi")
celery_logger = get_logger("source")

# Postgres connection string
db_host = environ.get("DATABASE_HOST")
db_port = environ.get("DATABASE_PORT")
db_user = environ.get("POSTGRES_USER")
db_password = environ.get("POSTGRES_PASSWORD")
db_name = environ.get("POSTGRES_DB")


# Configure the database connection
tortoise_orm = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": db_host,
                "port": db_port,
                "user": db_user,
                "password": db_password,
                "database": db_name,
            },
        }
    },
    "apps": {
        "models": {
            "models": ["source.models", "aerich.models"],
            "default_connection": "default",
        }
    },
    "use_tz": False,
    "timezone": "UTC",
}

# Configure the celery connection
celery = {
    "task_ignore_result": True,
    "result_expires": 30,
    "broker_connection_retry_on_startup": True,
    "worker_max_tasks_per_child": 200,
    "task_serializer": "json",
    "result_serializer": "json",
    "accept_content": ["json"],
    "enable_utc": True,
    "timezone": "UTC",
    "imports": [
        "source.tasks",
        "source.app.example_ws",
    ],
    "queues": ["default", "start_ws"],
    "task_routes": {
        "source.tasks.listen_ws": {"queue": "start_ws"},
        "source.tasks.regular_task": {"queue": "default"},
        "source.app.example_ws.take_message": {"queue": "default"},
    },
    "beat_schedule": {
        "start_get_streamers": {
            "task": "source.tasks.listen_ws",
            "schedule": 60.0 * 25,  # 25 minutes
        },
        "regular_task": {
            "task": "source.tasks.regular_task",
            "schedule": 30.0,  # 30 seconds
        },
    },
}

uv_event = uvloop.EventLoopPolicy()

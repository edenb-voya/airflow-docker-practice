import logging
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from redis import Redis

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("webserver_config.py is being loaded")

# Create a Redis client
redis_client = Redis(host='airflow-redis', port=6379, db=0)

# Configure Flask-Limiter to use Redis as the storage backend
def configure_limiter(app):
    logger.debug("Configuring Flask-Limiter with Redis")
    limiter = Limiter(
        get_remote_address,
        app=app,
        storage_uri="redis://airflow-redis:6379/0",
        storage_options={"socket_connect_timeout": 30},
        strategy="fixed-window", # or "moving-window"
    )
    return limiter

# Apply the configuration to the Flask app
def init_app(app):
    logger.debug("Initializing Flask app with custom configuration")
    configure_limiter(app)
    app.config['RATELIMIT_STORAGE_URL'] = "redis://airflow-redis:6379/0"
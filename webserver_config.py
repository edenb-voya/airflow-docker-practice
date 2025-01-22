from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
....

limiter = Limiter(
  get_remote_address,
  app=app,
  storage_uri="redis://airflow-redis:6379/0",
  storage_options={"socket_connect_timeout": 30},
  strategy="fixed-window", # or "moving-window"
)
from __future__ import absolute_import
import os, json, logging, redis
import time

from .worker import app
from .tda_stock import get_recommend_options


logger = logging.getLogger(__name__)
redis_client = redis.Redis(host=os.environ.get("REDIS_HOST", "redis"),
            port=int(os.environ.get("REDIS_PORT", "6379")),
            decode_responses=True)

@app.task(bind=True, name='recommend_options_exe', default_retry_delay=10)
def recommend_options_exe(self, ticker):
    try:
        get_recommend_options(ticker)

    except Exception as exc:
        raise self.retry(exc=exc)

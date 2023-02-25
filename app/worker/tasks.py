from __future__ import absolute_import
import logging

from .worker import app
from .tda_stock import get_recommend_options


logger = logging.getLogger(__name__)

@app.task(bind=True, name='recommend_options_exe', default_retry_delay=10)
def recommend_options_exe(self, ticker):
    try:
        get_recommend_options(ticker)

    except Exception as exc:
        raise self.retry(exc=exc)

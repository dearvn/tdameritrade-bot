"""
Implementation of various trading strategies.

"""
import os, json, logging, pytz, redis
import pandas as pd
from datetime import datetime
from app.tdameritrade.client import TDClient
import pusher
import pandas_ta as ta

log = logging.getLogger(__name__)
redis_client = redis.Redis(host=os.environ.get("REDIS_HOST", "redis"),
            port=int(os.environ.get("REDIS_PORT", "6379")),
            decode_responses=True)


def get_data_ticker(ticker, interval):
    c = TDClient()
    period_type = 'day'
    period = 1
    frequency_type = 'minute'
    frequency = 1

    if (interval == '5m'):
        frequency = 5
        period = 2
    elif (interval == '10m'):
        frequency = 10
        period = 5
    elif (interval == '15m'):
        frequency = 15
        period = 7
    elif (interval == '30m'):
        frequency = 30
        period = 10
    elif (interval == '1h'):
        frequency = 30
        period = 2
    elif (interval == '1d'):
        period_type = 'month'
        period = 6
        frequency_type = 'daily'
        frequency = 1

    resp = c.history(symbol=ticker,
                               periodType=period_type,
                               period=period,
                               frequencyType=frequency_type,
                               frequency=frequency)

    if 'candles' not in resp:
        return None
    candles = resp['candles']

    if (interval == '1h'):
        datas = []
        for item in candles:
            date_time = datetime.fromtimestamp(item['datetime'] / 1000)
            m = date_time.minute
            if m == 0:
                datas.append(item)
    else:
        datas = candles

    now = datetime.now(pytz.timezone("America/Los_Angeles"))
    h = now.hour
    m = now.minute
    if interval != '1m' and (m >= 30 and h == 6 or h > 6 and h <= 19):
        quote = c.quote(ticker)
        if quote != None and quote[ticker]:
            quote = quote[ticker]
            s = {"close": float(quote['lastPrice']), "open": float(quote['openPrice']),
                 "high": float(quote['highPrice']),
                 "low": float(quote['lowPrice']), "volume": int(quote['totalVolume']),
                 "datetime": int(quote['tradeTimeInLong'])}
            datas.append(s)

    return datas

def get_recommend_30m(ticker):
    datas = get_data_ticker(ticker, '30m')
    if len(datas) < 200:
        return;

    data10ms = get_data_ticker(ticker, '10m')
    if datas == None or len(datas) == 0 or data10ms == None or len(data10ms) == 0:
        print("Not found data {0}".format(ticker))
        return

    index = ['datetime']
    df = pd.DataFrame.from_records(datas, index=index)
    df10m = pd.DataFrame.from_records(data10ms, index=index)

    wma_11 = df.ta.wma(length=11)
    wma11 = wma_11.iloc[-1]
    wma11_1 = wma_11.iloc[-2]

    wma_48 = df.ta.wma(length=48)
    wma48 = wma_48.iloc[-1]
    wma48_2 = wma_48.iloc[-2]

    wma_200 = df.ta.wma(length=200)
    wma200 = wma_200.iloc[-1]

    wma_200_10m = df10m.ta.wma(length=200)
    wma200_10m = wma_200_10m.iloc[-1]

    price = datas[-1]['close']
    price_2= datas[-2]['close']

    low = datas[-1]['low']
    high = datas[-1]['high']

    wma200_10m_pct = 0
    if price > wma200_10m:
        wma200_10m_pct = wma200_10m/price
    else:
        wma200_10m_pct = price/wma200_10m

    is_away_call = 0
    is_away_put = 0
    away_call = -99
    away_put = 99
    ema_away = 0
    signal = ''
    if low < wma200:
        if wma11_1 < wma11:
            ema_away = 1 - wma200 / low
            if (1 - wma200 / low) * 100 <= away_call:
                is_away_call = 1
                signal = 'buy'
        else:
            ema_away = -1 * (low / wma200)
            if (-1 * (low / wma200) * 100 <= away_call):
                is_away_call = 2
                signal = 'buy'
    elif high > wma200:
        if wma11_1 < wma11:
            ema_away = wma200 / high
            if (wma200 / high) * 100 >= away_put:
                is_away_put = 1
                signal = 'sell'
        else:
            ema_away = high / wma200
            if (high / wma200)*100 >= away_put:
                is_away_put = 2
                signal = 'sell'

    ema_down = 0
    ema_down_price = 0
    ema_up_price = 0
    if price < wma48 and price_2 > wma48_2:
        ema_down = 1
        ema_down_price = price
    ema_up = 0
    if price > wma48 and price_2 < wma48_2:
        ema_up = 1
        ema_up_price = price

    output = {}
    output['symbol'] = ticker
    output['interval'] = '30'
    output['price'] = price
    output['last_price'] = price_2
    output['ema11'] = round(wma11, 2)
    output['ema48'] = round(wma48, 2)
    output['ema200_10m'] = round(wma200_10m_pct*100, 2)
    output['ema_down'] = ema_down
    output['ema_up'] = ema_up
    output['ema_away'] = round(ema_away*100, 2)
    output['call_type'] = is_away_call
    output['put_type'] = is_away_put
    output['signal'] = signal
    if ema_up_price:
        output['ema_up_price'] = ema_up_price
        output['ema_down_price'] = 0
    if ema_down_price:
        output['ema_down_price'] = ema_down_price
        output['ema_up_price'] = 0

    body = {}
    body[ticker] = output

    return body

def get_recommend_options(ticker):
    try:
        body = get_recommend_30m(ticker)
        pusher_app_id = os.environ.get('PUSHER_APP_ID')
        pusher_key = os.environ.get('PUSHER_KEY')
        pusher_secret = os.environ.get('PUSHER_SECRET')

        pusher_client = pusher.Pusher(pusher_app_id, pusher_key, pusher_secret, cluster=u'us2')
        pusher_client.trigger([u'recommend'], u'update-python', json.dumps(body))

    except AssertionError as e:
        print("error", ticker, e)
        log.exception(e)
    except Exception as e:
        print("error", ticker, e)
        log.exception(e)

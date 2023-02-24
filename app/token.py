from tda import auth, client

import json

# authenticate
try:
    API_KEY = ''
    ACCOUNT_ID = ''
    REDIRECT_URI = 'https://dev.local'
    TOKEN_PATH = '../app/worker/token.pickle'
    CHROMEDRIVER_PATH = '../app/worker/chromedriver'

    c = auth.client_from_token_file(TOKEN_PATH, API_KEY)
except FileNotFoundError:
    from selenium import webdriver
    with webdriver.Chrome(executable_path=CHROMEDRIVER_PATH) as driver:
        c = auth.client_from_login_flow(
            driver, API_KEY, REDIRECT_URI, TOKEN_PATH)

# get price history for a symbol
r = c.get_price_history('AAPL',
        period_type=client.Client.PriceHistory.PeriodType.YEAR,
        period=client.Client.PriceHistory.Period.TWENTY_YEARS,
        frequency_type=client.Client.PriceHistory.FrequencyType.DAILY,
        frequency=client.Client.PriceHistory.Frequency.DAILY)

print(json.dumps(r.json(), indent=4))
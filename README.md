# tdameritrade-bot
TD Ameritrade Bot is an artificial intelligence-powered chatbot that provides clients with personalized, real-time investment advice. This cutting-edge technology uses machine learning algorithms to analyze financial markets, identify trends and recommend personalized investments for users. With TD Ameritrade Bot, users can get tailored investment advice from the comfort of their homes, making it easier and more convenient than ever to manage their portfolios. The Bot's intuitive interface and advanced technology make it a great tool for both novice and experienced investors alike. TD Ameritrade Bot is an innovative way to stay on top of the markets and make smart investments that can help you reach your financial goals.

A simple bot to tracking ticker to trade option on TDA

![Alt text](https://github.com/dearvn/tdameritrade-bot/raw/main/recommend.png?raw=true "UI")

## Run on local to develop

```
# Create an isolated Python virtual environment
pip install virtualenv
virtualenv ./virtualenv --python=$(which python3)

# Activate the virtualenv
. virtualenv/bin/activate

# Install Python requirements
pip install -r requirements.txt

# Install app-*
pip install -e .
pip install -e ./app


```

# Create a pusher app to send signal

# Create a app from TDAmeritrade
# Download chromedriver and get refresh token

```
python -m app.token
```
# Get refresh-token

# Set variable param on local

```
export TDAMERITRADE_CLIENT_ID=
export TDAMERITRADE_REFRESH_TOKEN=
export PUSHER_APP_ID=
export PUSHER_KEY=
export PUSHER_SECRET=
```

# Local test

```
python -m app.test-tda
```

## Run by docker

* Edit params in env.evn

# Run docker

```
docker-compose build
docker-compose up -d

docker exec -i -t tdameritrade-bot_app_1  /bin/bash

python manage.py runserver 0.0.0.0:8000


```

## Rest Api

http://0.0.0.0:8000/recommend-options-get
Method: GET
Params: tickers = ['AAPL','TSLA']


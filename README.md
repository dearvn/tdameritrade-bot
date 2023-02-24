# tdameritrade-bot
TD Ameritrade Bot is an artificial intelligence-powered chatbot that provides clients with personalized, real-time investment advice. This cutting-edge technology uses machine learning algorithms to analyze financial markets, identify trends and recommend personalized investments for users. With TD Ameritrade Bot, users can get tailored investment advice from the comfort of their homes, making it easier and more convenient than ever to manage their portfolios. The Bot's intuitive interface and advanced technology make it a great tool for both novice and experienced investors alike. TD Ameritrade Bot is an innovative way to stay on top of the markets and make smart investments that can help you reach your financial goals.

A simple bot to tracking ticker to trade option on TDA

![Alt text](https://github.com/dearvn/tdameritrade-bot/raw/main/recommend.png?raw=true "UI")

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

# Run docker

docker-compose build
docker-compose up -d

```

# Create a pusher app to send signal

# Create a app from TDAmeritrade
# Download chromedriver and get refresh token

```
python -m app.token
```
# Get refresh-token


# Local test

```
python -m app.test-tda
```

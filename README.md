# Him 🍆🍑💦

Tinder is not fair game when you are a man. Even if you spend a lot of money in Boosts, you won't get 50+ matches per day like women do.

That's until you use "Him".

Him is here to re-establish genders equality on Tinder.

## Features

- Like profile depending on `RADIUS` until `MAX_LIKE` is reached
- Send the first message from `FIRST_MESSAGES`
- Chat with your matches using OpenAI davinci

## Prerequisites

You will need:
- You will need a Tinder account obviously
- You will need Docker
- You need to be logged in to your Tinder account and get the `X-Auth-Token` with your browser debug tool
- You need an [OpenAI](https://beta.openai.com) secret key


## Installation 💻

You need Docker & Docker Compose

For a fresh install:

```bash
cp .env-dist .env # Edit to your needs.
make start
make collectstatic
make migrate
make load-fixtures
```
http://0.0.0.0:8000


For developpements:
```bash
make stop
make dev-start
```

## Test ⚡

Please run the test and codestyle before making a PR:

```bash
make pip-dev
make test
make codestyle
```

## To run the bot

```bash
make bot-run
```

## Train the bot

If you want to train the bot:
```bash
export OPENAI_API_KEY="sk-8RDxVvLFzgN0MDtPpXZVT4BldkFJJk2xZCVyKwWM4OJQPPBV"

# Train the model
openai api fine_tunes.create -m davinci --n_epochs 2 -t ./train_data/train.jsonl --suffix "tinder"

```

<img src="./docs/chat-bot.png" alt="isolated" width="1024"/>

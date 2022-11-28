# Him 

## Installation 💻

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

The bot is a Django command that will like profiles, send first messages and chat with you matches.
Look at the `config.yml` if you want to disable some features.

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

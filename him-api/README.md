# Him 

## Installation 💻

For a fresh install:

```bash
# Copy configuration files and edit them to your needs
cp .env-dist .env && cp config-dist.yml config.yml
```
In config.yml there are 3 important values to set:
- `x_auth_token`: login to Tinder on your brower and get this values in any headers from their API call.
- `openai_secret`: your OpenAI secret key
- `openai_engine`: your OpenAI engine
- `your_profile.id`: go to Tinder web and find your profile id in an API request

Then setup the project by running the following commands:
```bash
make start
make collectstatic
make migrate
make load-fixtures
```

You should now be able to call 4 different urls:
- http://0.0.0.0:8000
- http://0.0.0.0:8000/bot/like
- http://0.0.0.0:8000/bot/send-first-messages/
- http://0.0.0.0:8000/bot/chat-with-matches/


For developpements:
```bash
make stop
make dev-start
```
**Note**: there is no watch, so you will need to restart docker you make changes to files


## Test ⚡

Please run the test and codestyle before making a PR:

```bash
make pip-dev
make test
make codestyle
```
## Train the bot

If you want to train the bot:
```bash
export OPENAI_API_KEY="sk-8RDxVvLFzgN0MDtPpXZVT4BldkFJJk2xZCVyKwWM4OJQPPBV"

# Train the model
openai api fine_tunes.create -m davinci --n_epochs 2 -t ./train_data/train.jsonl --suffix "tinder"

```

<img src="./docs/chat-bot.png" alt="isolated" width="1024"/>

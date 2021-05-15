#!/bin/bash

. /home/amogh/.local/share/virtualenvs/covid-chatbot-pzGr4qv0/bin/activate

fuser -k 8000/tcp
fuser -k 5005/tcp
fuser -k 5055/tcp

cd rasa-bot
rasa run actions -vv &
docker run -p 8000:8000 rasa/duckling &

# rasa run -m models --enable-api --cors "*" --debug


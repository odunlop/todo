#!/usr/bin/env bash

# Create test board, get test board ID, run tests and delete test board when done
curl -s --request POST --url "https://api.trello.com/1/boards/?name=TestBoard&key=${TRELLO_API}&token=${TRELLO_TOKEN}" | jq .id > id &&\
str_id=$(cat id) &&\
regex='"([0-9a-fA-F]{24})"' &&\
[[ ${str_id} =~ ${regex} ]] &&\
export TRELLO_BOARD_ID="${BASH_REMATCH[1]}" &&\
curl -s --request POST --url "https://api.trello.com/1/boards/${TRELLO_BOARD_ID}/labels?name=TestLabel&color=black&key=${TRELLO_API}&token=${TRELLO_TOKEN}" &&\
pytest ./tests/test_trello.py
curl -s --request DELETE --url "https://api.trello.com/1/boards/${TRELLO_BOARD_ID}?key=${TRELLO_API}&token=${TRELLO_TOKEN}"
rm -f id
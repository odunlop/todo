#!/usr/bin/env bash

RAND=$(openssl rand -hex 2)
export BOARD_NAME="TestBoard${RAND}"

# Create test board, get test board ID, run tests and delete test board when done
curl -s --request POST --url "https://api.trello.com/1/boards/?name=${BOARD_NAME}&key=${TRELLO_API}&token=${TRELLO_TOKEN}" | jq .id > id &&\
str_id=$(cat id) &&\
regex='"([0-9a-fA-F]{24})"' &&\
[[ ${str_id} =~ ${regex} ]] &&\
export TRELLO_BOARD_ID="${BASH_REMATCH[1]}" &&\
curl -s --request POST --url "https://api.trello.com/1/boards/${TRELLO_BOARD_ID}/labels?name=TestLabel&color=black&key=${TRELLO_API}&token=${TRELLO_TOKEN}" > /dev/null 2>&1 &&\
pytest ./tests/test_trello.py
exit_code=$?
curl -s --request DELETE --url "https://api.trello.com/1/boards/${TRELLO_BOARD_ID}?key=${TRELLO_API}&token=${TRELLO_TOKEN}" > /dev/null 2>&1
rm -f id
# Below is needed so failing tests make GitHub pipeline fail
exit $exit_code

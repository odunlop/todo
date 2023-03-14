import unittest
import sys
import requests
import os
import json

sys.path.append('../todo')
import trello
sys.path.remove('../todo')

api_key = os.environ.get('TRELLO_API')
token = os.environ.get('TRELLO_TOKEN')
member_name = os.environ.get('TRELLO_NAME')

def get_member_id(name):
    url = f"https://api.trello.com/1/members/{name}"

    headers = {
    "Accept": "application/json"
    }

    query = {
    'key': api_key,
    'token': token
    }

    response = requests.request(
    "GET",
    url,
    headers=headers,
    params=query
    )

    response = json.loads(response.text)
    return response["id"]

def board_id(id):
    url = f"https://api.trello.com/1/members/{id}/boards"

    headers = {
        "Accept": "application/json"
    }

    query = {
        'key': api_key,
        'token': token
    }

    response = requests.request(
        "GET",
        url,
        headers=headers,
        params=query
    )

    boards = json.loads(response.text)

    for board in boards:
        if board["name"] == "TestBoard":
            return board["id"]

b_id = board_id(get_member_id(member_name))

class TestTrello(unittest.TestCase):

    def test_get_list_(self):
        lists = trello.get_lists(b_id)
        example_list = ["To Do", "Doing", "Done"]
        test_list = []

        for list in lists:
            test_list.append(list["name"])
        self.assertTrue(example_list, test_list)

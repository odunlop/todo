from cProfile import label
from cgi import test
import unittest
import sys
import requests
import os
import json
import random
import string

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

    ### LISTS ###
    def test_get_list_(self):
        lists = trello.get_lists(b_id)
        example_list = ["To Do", "Doing", "Done"]
        test_list = []

        for list in lists:
            test_list.append(list["name"])

        self.assertEqual(example_list, test_list)

    def test_get_list_id(self):
        lists = trello.get_lists(b_id)
        l_id = trello.get_todo_list_id(lists)
        self.assertRegex(l_id, "^[0-9a-fA-F]{24}$")
    
    ### LABELS ###
    def test_all_labels(self):
        labels = trello.get_all_labels(b_id)
        example_labels = ['', '', '', '', '', '', 'TestLabel']
        test_labels = []

        for label in labels:
            test_labels.append(label["name"])

        self.assertEqual(example_labels, test_labels)

    def test_all_free_labels(self):
        labels = trello.get_all_labels(b_id)
        free_labels = trello.get_free_labels(labels)
        self.assertEqual(6, len(free_labels))
    
    def test_avaliable_colour(self):
        labels = trello.get_all_labels(b_id)
        colour = trello.give_avaliable_colour(labels)
        self.assertEqual(colour, "yellow")
    
    def test_amend_label(self):
        labels = trello.get_all_labels(b_id)
        label_id = (trello.get_free_labels(labels))[0]
        name = "Testing Amending"
        trello.amend_label(label_id, name)
        new_labels = trello.get_all_labels(b_id)
        self.assertEqual(new_labels[0]["name"], name)

    def test_create_label(self):
        name = "Testing Creating"
        trello.new_label(b_id, name, "black_dark")
        new_labels = trello.get_all_labels(b_id)
        self.assertEqual(new_labels[-1]["name"], name)
    
    def test_label_project_amend(self):
        labels = trello.get_all_labels(b_id)
        name = "Label Project [A]"
        trello.label_project(b_id, name, labels)
        new_labels = trello.get_all_labels(b_id)
        self.assertEqual(new_labels[1]["name"], name)
    
    def test_label_project_create(self):
        num = 4
        for n in range(num):
            labels = trello.get_all_labels(b_id)
            label_id = (trello.get_free_labels(labels))[0]
            name = ''.join(random.choices(string.ascii_uppercase +string.digits, k=6))
            trello.amend_label(label_id, name)
        labels = trello.get_all_labels(b_id)
        name = "Label Project [B]"
        trello.label_project(b_id, name, labels)
        new_labels = trello.get_all_labels(b_id)
        self.assertEqual(new_labels[-1]["name"], name)

    def test_get_project_label(self):
        name = "TestLabel"
        label_id = trello.get_project_label(b_id, name)
        self.assertRegex(label_id, "^[0-9a-fA-F]{24}$")
    
    def test_get_repo_name(self):
        self.assertEqual(trello.get_repo_name(), "todo")

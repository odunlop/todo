import os
import requests
import json
import get_todo
from git import Repo

api_key = os.environ.get('TRELLO_API')
token = os.environ.get('TRELLO_TOKEN')
label_choice = os.environ.get('LABEL_TICKETS')
board_id_hardcoded = "6409b884e0650c7206272710"

### BOARDS ###
def get_board_id(url):
    headers = {
        "Accept": "application/json"
    }

    query = {
        'key': api_key,
        'token': token
    }

    response = requests.request(
        "GET",
        f"{url}.json",
        headers=headers,
        params=query
    )
    data = json.loads(response.text)
    return data["id"]

### LISTS ###
def get_lists(board_id):
    url = f"https://api.trello.com/1/boards/{board_id}/lists"
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

    lists = json.loads(response.text)
    return lists

def get_todo_list_id(lists):
    for list in lists:
        if list["name"] == "To Do":
            return list["id"]
    pass


### LABELS ###
def get_all_labels(board_id):
    url = f"https://api.trello.com/1/boards/{board_id}/labels"

    query = {
        'key': api_key,
        'token': token
    }

    response = requests.request(
        "GET",
        url,
        params=query
    )

    return json.loads(response.text)

def get_free_labels(labels):
    free_labels = []
    for label in labels:
        if label["name"] == "":
            free_labels.append(label["id"])
    return free_labels

def give_avaliable_colour(labels):
    # have an array with all colours, if already one with name filled in, skip
    label_colours = ['green', 'yellow', 'orange', 'red', 'purple', 'blue', 'sky', 'lime', 'pink', 'black', "green_light", "green_dark", "yellow_light", "yellow_dark", "orange_light", "orange_dark", "red_light", "red_dark", "purple_light", "purple_dark", "blue_light", "blue_dark", "sky_light", "sky_dark", "lime_light", "lime_light", "pink_light", "pink_dark", "black_light", "black_dark"]
    
    colours_in_use = []

    for label in labels:
        if label["name"] != "":
            colours_in_use.append(label["color"])
    
    for colour in colours_in_use:
        label_colours.remove(colour)
    
    print(label_colours)

    return label_colours[0]

def amend_label(label_id, repo_name):
    url = f"https://api.trello.com/1/labels/{label_id}"

    query = {
        'key': api_key,
        'token': token,
        'name': repo_name
    }

    response = requests.request(
        "PUT",
        url,
        params=query
    )

    return json.loads(response.text)

def new_label(board_id, repo_name, colour):
    colour = colour
    url = f"https://api.trello.com/1/boards/{board_id}/labels"

    query = {
        "name": repo_name,
        "color": colour,
        "key": api_key,
        "token": token
    }

    response = requests.request(
        "POST",
        url,
        params=query
    )

    return json.loads(response.text)

def label_project(board_id, repo_name, labels):
    # Check if any avaliable labels are free, otherwise creqte
    free_labels = get_free_labels(labels)
    if free_labels != []:
        label = amend_label(free_labels[0], repo_name)
    else:
        colour = give_avaliable_colour(labels)
        label = new_label(board_id, repo_name, colour)
    
    print("Label for project created")
    return label["id"]

def get_project_label(board_id, repo_name):
    labels = get_all_labels(board_id)
    exists = False
    # check if there's a label, if not run label_project
    # we get this by looking through all labels for same name
    for label in labels:
        if label["name"] == repo_name:
            exists = True
            return label["id"]
    
    if exists == False:
        label_id = label_project(board_id, repo_name, labels)
        return label_id

def get_repo_name():
    repo = Repo(".")
    repo_name = repo.remotes.origin.url.split('.git')[0].split('/')[-1]
    return repo_name

### CARDS ###
def get_cards_in_list(id):
    url = f"https://api.trello.com/1/lists/{id}/cards"

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

    return json.loads(response.text)

def label_card(card_id, label_id):
    url = f"https://api.trello.com/1/cards/{card_id}/idLabels"

    query = {
        'key': api_key,
        'token': token,
        'value': label_id
    }

    response = requests.request(
        "POST",
        url,
        params=query
    )

    return json.loads(response.text)

def new_card(list_id, name, desc, label_id):
    url = "https://api.trello.com/1/cards"

    headers = {
        "Accept": "application/json"
    }

    query = {
        'idList': list_id,
        'key': api_key,
        'token': token,
        'name': name,
        'desc': desc,
        'pos': 'bottom'
    }

    response = requests.request(
        "POST",
        url,
        headers=headers,
        params=query
    )

    json_response = json.loads(response.text)

    if label_choice == "True":
        label_card(json_response["id"], label_id)

    return json_response["id"], json_response["idShort"]

# TO_DO: Response if no new tickets
def write_todos(dir, list_id, repo_name, board_id):
    todo_tickets = []
    files = get_todo.list_all_files(dir)
    todos_list = get_todo.get_new_todos(files)
    label = get_project_label(board_id, repo_name)
    if todos_list == {}:
        print("No new tickets")
        return None
    print("Updating Trello", end="", flush=True)
    for file, todos in todos_list.items():
        for todo, line_number in todos.items():
            id, short_id = new_card(list_id, todo, f"**Location:** `{file}:{line_number}`", label)
            ticket = {
                "id": id,
                "idShort": short_id,
                "content": todo,
                "origin": file,
                "line_number": line_number
            }
            todo_tickets.append(ticket)
            print(".", end="", flush=True)        
    return todo_tickets

def remember_todo(tickets):
    for ticket in tickets:
        with open(rf"{ticket['origin']}", "r+") as file:
            data = file.read()
            data = data.replace(ticket["content"], f"{ticket['content']} [[{ticket['id']}]]")
        with open(rf"{ticket['origin']}", "w") as file:
            file.write(data)


# THINGS TO DO:

# 1) Ensure there is a To Do column and either (a) create one if not or (b) give error message telling them to make one

# 2) Checks if placed in Done??? Maybe allow users to configure the name of their "done" column 

# 3) Checks if existing cards still exist in thingy

# 4) Response if no new tickets

# 5) Think about how I want to proceed with persisting data
import os
import requests
import json
import get_todo

api_key = os.environ.get('TRELLO_API')
token = os.environ.get('TRELLO_TOKEN')
board_id = "6409b884e0650c7206272710"

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
        if list["name"] == "TO-DO":
            return list["id"]
    pass

def new_card(list_id, name, desc):
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

    print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))



# Get list of Todos and write them

def write_todos(dir, list_id):
    files = get_todo.list_all_files(dir)
    todos_list = get_todo.get_all_todos(files)
    for file, todos in todos_list.items():
        for todo, line_number in todos.items():
            new_card(list_id, todo, f"**Location:** `{file}:{line_number}`")



lists = get_lists(board_id)
print(lists)
list_id = get_todo_list_id(lists)
dir = "."
write_todos(dir, list_id)
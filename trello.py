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

    json_response = json.loads(response.text)
    return json_response["id"], json_response["idShort"]

def write_todos(dir, list_id):
    todo_tickets = []
    files = get_todo.list_all_files(dir)
    todos_list = get_todo.get_all_todos(files)
    print("Updating Trello", end="", flush=True)
    for file, todos in todos_list.items():
        for todo, line_number in todos.items():
            id, short_id = new_card(list_id, todo, f"**Location:** `{file}:{line_number}`")
            # print(id)
            # print(short_id)
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

# Now we want to get the todos back with their corresponding ids....

# And then add the id to the line....

# Then when it goes to check, it finds a card with the same shortid and checks the long ids match (long ids stored in a .todo file??? maybe use the python to yml thing)
# ALSO need to make sure it's not in "in progress" or any other list in the board

lists = get_lists(board_id)
list_id = get_todo_list_id(lists)
dir = "."
tickets = write_todos(dir, list_id)

for ticket in tickets:
    print(ticket)
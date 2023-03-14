import trello
import os

board_id_hardcoded = "6409b884e0650c7206272710"
board_url = "https://trello.com/b/KZItRtcg/api-testing"

board_id = trello.get_board_id(board_url)
lists = trello.get_lists(board_id)
list_id = trello.get_todo_list_id(lists)
dir = "."
repo_name = trello.get_repo_name()
tickets = trello.write_todos(dir, list_id, repo_name, board_id)
trello.remember_todo(tickets)

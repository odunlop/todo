import code_docs
import sys
import os
import glob
import re
import colorama
from colorama import Fore, Style

# TO_DO: Write some tests

def list_all_files(dir):
    list = glob.glob(dir + '/**/*', recursive=True)
    files = []
    for file in list:
        if os.path.isfile(file):
            files.append(file)
    return files

def get_new_todos(files):
    regex_list = [
        "(?:\[(\d*)\])\s?(?:(?:#)|(?:\/\/)|(?:–\s–)|(?:%))\sTO-DO:\s?(.*)\n?", # General match
        "\[(\d*)\]\s<!--\sTO-DO:\s(.*)\s-->", # HTML match
        "\[(\d*)\]\s\/\*\sTO-DO:\s(.*)\s\*" # CSS match
    ]
    result = {}
    for file in files:
        lines = get_lines(file)
        comments = get_comments(lines, regex_list)
        result[file] = comments
    return result

# Add some sort of logging so we can tell users which files got skipped for content issues
def get_lines(filepath):
    try:
        file = open(filepath, "r") #the code that raises the error
        lines = []
        count = 0
        result = file.readlines()
        for line in result:
            count += 1
            lines.append(f"[{count}] {line}")
    except:
        pass
    return lines

def get_comments(lines, regex_list):
    todos = {}
    existing_todo_pattern = "TO-DO:\s.*(\[\[(\S+)\]\])"
    for line in lines:
        for regex in regex_list:
            already_exists = re.search(rf"{existing_todo_pattern}", line)
            result = code_docs.find_match(line, regex)
            if already_exists:
                pass
            elif result[0] == True:
                todos[result[1].group(2)] = result[1].group(1)
    return todos

def write_todos(todos):
    f = open("trello.txt", "a")
    for file, todos in todos.items():
        for todo, line_number in todos.items():
            f.write(f"Task: {todo} ({file}:{line_number})\n\n")
    f.close()

# Extract to seperate file
files = list_all_files(".")
result = get_new_todos(files)
f = open("trello.txt", "w")
f.write("PRETEND TELLO BOARD\n\n")
f.close()
write_todos(result)

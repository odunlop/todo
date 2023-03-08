import code_docs
import sys
import os
import glob
import colorama
from colorama import Fore, Style

# TO-DO: Write some tests

def list_all_files(dir):
    list = glob.glob(dir + '/**/*', recursive=True)
    files = []
    for file in list:
        if os.path.isfile(file):
            files.append(file)
    return files

def get_all_todos(files):
    result = {}
    comment_match = "(?:\[(\d*)\])\s(?:(?:#)|(?:\/\/)|(?:–\s–)|(?:<!--)|(?:\/\*)|(?:%))\sTO-DO:\s?(.*)\n?"
    for file in files:
        lines = get_lines(file)
        comments = get_comments(lines, comment_match)
        result[file] = comments
    return result

# TO-DO: Add some sort of logging so we can tell users which files got skipped for content issues
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

def get_comments(lines, comment_match):
    todos = {}
    for line in lines:
        result = code_docs.find_match(line, comment_match)
        if result[0]:
            # steps.append(f"{result[1].group(1)}. {result[1].group(9)}")
            todos[result[1].group(2)] = result[1].group(1)
    return todos

def write_todos(todos):
    f = open("trello.txt", "a")
    for file, todos in todos.items():
        for todo, line_number in todos.items():
            f.write(f"Task: {todo} ({file}:{line_number})\n\n")
    f.close()

# TO-DO: Extract to seperate file
files = list_all_files(".")
result = get_all_todos(files)
f = open("trello.txt", "w")
f.write("PRETEND TELLO BOARD\n\n")
f.close()
write_todos(result)

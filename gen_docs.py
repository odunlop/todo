"""
TEXT HERE
"""

import re
import os
import sys
import colorama
from colorama import Fore, Style


class InvalidFileName(Exception):
    "Raised when the input value is less than 18"
    pass

############### IDENTIFY FILES ###############

def find_match(line, regex):
    match = re.search(rf'{regex}', line)
    if match:
        return True, match
    else:
        return False, None

def find_overwrite_section(lines):
    files = []
    count = 0
    readme_match = "{{ Documentation Section:\s(.*)\s}}"
    for line in lines:
        result = find_match(line, readme_match)
        if result[0]:
            count += 1
            file = result[1].group(1)
            files.append(file)
    print(f"{count} Files found...")
    for file in files:
        print(Fore.BLUE + f"    {file}")
    print(Style.RESET_ALL)
    return files



############### FIND LINES ###############


def get_lines(filepath):
    try:
        file = open(filepath, "r") #the code that raises the error
    except OSError:
        sys.tracebacklimit = 0
        raise OSError("Invalid filepath provided:" + Fore.RED + f"\n    {filepath}") from None
    return file.readlines()



############### PRINT STEPS ###############

def get_comments(lines):
    steps = []
    comment_match = "##-\s(.*)\n"
    count = 0
    for line in lines:
        result = find_match(line, comment_match)
        if result[0]:
            count += 1
            steps.append(f"{count}. {result[1].group(1)}")
    return steps

############### LOOP THROUGH FILES FOR COMMENTS ###############

def check_files(files):
    result = {}
    for file in files:
        lines = get_lines(file)
        comments = get_comments(lines)
        result[file] = comments
    return result

############### SEARCH AND REPLACE? ###############

def duplicate_data(template_filepath, readme_filepath):
    with open(template_filepath, "r+") as f:
        data = f.read()
        if (os.path.exists(readme_filepath) == True):
            os.remove(readme_filepath)
            # create file
        readme = open(readme_filepath, "w")
        readme.writelines(data)
        readme.close()


def format_comments(comments):
    #we want a  string with /n at the end
    string = "\n".join(comments)
    return string

def search_and_replace(dictionary):

    for filepath, comments in dictionary.items():

        # THIS WILL BE CHANGED TO MATCH FILEPATH SPECIFICALY
        regex = "{{ Documentation Section:\s(" + filepath + ")\s}}"

        formatted_comments = format_comments(comments)

        with open("README.md", "r+") as f:
            
            # Reading the file data and store
            # it in a file variable
            file = f.read()

            # Replacing the pattern with the string
            # in the file data
            
            file = re.sub(regex, formatted_comments, file)

            # Setting the position to the top
            # of the page to insert data
            f.seek(0)

            # Writing replaced data in the file
            f.write(file)

            # Writing replaced data in the file
            f.truncate()
    
    return "Replaced"

# comments = ['1. This is a test', '2. Second test']
# format_comments(comments)

# ##- Open the file
# dockerfile = open("Dockerfile", "r")
# ##- Break the file up into lines
# Lines = dockerfile.readlines()
# ##- Identify which lines are documentation regex
# steps = get_comments(Lines)
# ##- Print out the formatted product
# print(steps)


#### CHECK IF ANY CHANGES
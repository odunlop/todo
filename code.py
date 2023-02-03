"""
TEXT HERE
"""

import re
from pathlib import Path
import os


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
    print(f"{count} Files found")
    return files



############### FIND LINES ###############

def get_lines(filepath):
    file = open(filepath, "r")
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

def duplicate_data():
    with open("README.md.gotmpl", "r+") as f:
        data = f.read()
        if (os.path.exists("README.md") == True):
            os.remove("README.md")
            # create file
        readme = open("README.md", "w")
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
            # f.truncate()
    
    return "Replaced"

comments = ['1. This is a test', '2. Second test']
format_comments(comments)

# ##- Open the file
# dockerfile = open("Dockerfile", "r")
# ##- Break the file up into lines
# Lines = dockerfile.readlines()
# ##- Identify which lines are documentation regex
# steps = get_comments(Lines)
# ##- Print out the formatted product
# print(steps)


# [ ] Go through README and find all files
# [ ] Put those filenames in list
lines = get_lines("README.md.gotmpl")
files = find_overwrite_section(lines)
# [ ] Loop through files, for each file generate a list with steps
dictionary = check_files(files)
# [ ] Copy README.md.gotmpl data to README
duplicate_data()
# [ ] Go back and overwrite the section with the matching filename
search_and_replace(dictionary)

#### NEED TO BUILD VALIDATOR FOR FILEPATH
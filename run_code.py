import gen_docs

# [ ] Go through README and find all files
# [ ] Put those filenames in list
lines = gen_docs.get_lines("README.md.gotmpl")
files = gen_docs.find_overwrite_section(lines)
# [ ] Loop through files, for each file generate a list with steps
dictionary = gen_docs.check_files(files)
# [ ] Copy README.md.gotmpl data to README
gen_docs.duplicate_data("README.md.gotmpl", "README.md")
# [ ] Go back and overwrite the section with the matching filename
gen_docs.search_and_replace(dictionary)
print("README Updated")
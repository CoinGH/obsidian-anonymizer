# ♥♥♥♥♥♥♥   ♥♥♥♥♥♥♥♥
# ♥         ♥
# ♥         ♥   ♥♥♥♥♥
# ♥         ♥        ♥
# ♥♥♥♥♥♥♥   ♥♥♥♥♥♥♥♥

import json
import re
import pathlib as pl
from tqdm import tqdm
import uuid

#Introduction
print("Hello user!\nThis program is making your markdown files - secure\nMade by CoinGH\n","."*64)

#Searching for folder
while True:
    path = pl.Path(input("Enter path to folder: "))
    if path.exists():
        if path.is_dir():
            print("Folder Founded Successfully!")
            break
        else:
            print("It's not a folder!")
    else:
        print("Folder not found! Try again!")

print("."*64)

#Creating lists
md_files = list(path.rglob('*.md'))
canvas_files = list(path.rglob('*.canvas'))

print(str(len(md_files)) + " markdown files found!")
print(str(len(canvas_files)) + " canvas files found!")

print("."*64)

#Lists of links
dictionary_of_links = {}

with tqdm(total=len(md_files), desc="Progress") as pbar: #Progress Bar
    #Filenames to Dictionary
    for current_file in md_files:
        note_name = current_file.stem
        pbar.update(1) #Updating Progress Bar

        unique_id = uuid.uuid4().hex[:8]
        new_filename = f"file_{unique_id}"
        dictionary_of_links[note_name] = new_filename

print(f"\nChanged {len(dictionary_of_links)} links in .md files!")

#Replacement Function
def replacer(match):
    original_link = match.group(1)
    parts = original_link.split("|", 1)
    target_note_name = parts[0]
    if target_note_name in dictionary_of_links:
        return f"[[{dictionary_of_links[target_note_name]}]]"
    else:
        return match.group(0)

#Replace links in files
for current_file in md_files:
    with open(current_file, "r", encoding='utf-8') as f:
        all_file_content = f.read()

    new_file_content = re.sub(r'\[\[(.*?)]]', replacer, all_file_content)
    with open(current_file, "w", encoding='utf-8') as f:
        f.write(new_file_content)

# Replace file names
    original_filename = current_file.stem
    if original_filename in dictionary_of_links:
        new_filename = dictionary_of_links[original_filename]
        new_path = current_file.parent / f"{new_filename}.md"
        current_file.rename(new_path)

print("."*64)

#Save to JSON (dump)
with open(path / "dictionary_prefs_md.json", "w", encoding='utf-8') as f:
    json.dump(dictionary_of_links, f, ensure_ascii=False, indent=4)
print("Changes was saved in dictionary_prefs.json")

print("."*64)

#For .canvas files
for current_file in canvas_files:
    with open(current_file, "r", encoding='utf-8') as f:
        canvas_data = json.load(f)
        for node in canvas_data["nodes"]:
            if node["type"] == "text":
                pass
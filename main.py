import json
import re
import pathlib as pl
from tqdm import tqdm
import uuid

#Indroduction
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
links = {}
counter = 0
all_note_names = set()

with tqdm(total=len(md_files), desc="Progress") as pbar:

    for md_file in md_files:
        note_name = md_file.stem
        all_note_names.add(note_name)
        pbar.update(1)

    for note_name in all_note_names:
        unique_id = uuid.uuid4().hex[:8]
        new_name = f"file_{unique_id}.md"
        links[note_name] = new_name
        counter += 1

print(f"\nChanged {len(links)} links in .md files!")

for md_file in md_files:
    with open(md_file, "r", encoding='utf-8') as f:
        str1 = f.read()
    def replacer(match):
        og_link = match.group(1)
        parts = og_link.split("|", 1)
        target_note = parts[0]
        if target_note in links:
            return f"[[{links[target_note]}]]"
        else:
            return match.group(0)

    new_con = re.sub(r'\[\[(.*?)]]', replacer, str1)

    with open(md_file, "w", encoding='utf-8') as f:
        f.write(new_con)

for md_file in md_files:
    og_name = md_file.stem

    if og_name in links:
        new_name = links[og_name]
        new_path = md_file.parent / f"{new_name}.md"
        md_file.rename(new_path)

print("."*64)

#Save to JSON (dump)
with open(path / "links_prefs.json", "w", encoding='utf-8') as f:
    json.dump(links, f, ensure_ascii=False, indent=4)
print("Changes was saved in links_prefs.json")
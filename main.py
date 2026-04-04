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
import time

#Introduction
print("Hello User!\nThis program is making your markdown files -> secure\nMade by CoinGH\n","."*64)

def folder_checker(path1):
    if path1.exists():
        if path1.is_dir():
            print("Folder Founded Successfully!")
            return 67
        else:
            print("It's not a folder!")
            return 0
    else:
        print("Folder not found! Try again!")
        return 0

#Searching for folder
while True:
    path = pl.Path(input("Enter path to folder: "))
    i = folder_checker(path)
    if i == 67:
        break

print("."*64)

folders_to_encrypt = set()

print("Do you want to choose manually, folders to encrypt?\nType 'Y' for Yes, or 'N' for No")
if input().upper().strip() == "Y":
    print("." * 64)
    print("Start typying links one by one!\nIf you are done, type 'stop'")
    while True:
        temp = input("Enter folder path to encrypt: ")
        if temp.lower().strip() == "stop":
            break
        print("-" * 64)
        i = folder_checker(pl.Path(temp))
        print("And added to the list!\nPlease, type next one...")
        print("-" * 64)
        if i == 67:
            folders_to_encrypt.add(pl.Path(temp))

#Creating lists
md_files = list(path.rglob('*.md'))
canvas_files = list(path.rglob('*.canvas'))

print(str(len(md_files)) + " markdown files found!")
print(str(len(canvas_files)) + " canvas files found!")

print("."*64)

#Lists of links
dictionary_of_links = {}

with tqdm(total=len(md_files), desc="Progress .md", colour="blue") as pbar_md: #Progress Bar
    #Filenames to Dictionary
    for current_file in md_files:
        if not folders_to_encrypt or any(current_file.is_relative_to(folder) for folder in folders_to_encrypt):
            note_name = current_file.stem

            unique_id = uuid.uuid4().hex[:8]
            new_filename = f"file_{unique_id}"
            dictionary_of_links[note_name] = new_filename
        pbar_md.update(1)  # Updating Progress Bar

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
with open(path / 'AllInOne.md', 'w', encoding='utf-8') as f1:
    for current_file in md_files:
        with open(current_file, "r", encoding='utf-8') as f:
            all_file_content = f.read()
        new_file_content = re.sub(r'\[\[(.*?)]]', replacer, all_file_content)
        removing_aliases = re.sub(r'(?s)^---.*?---\n', '', new_file_content)
        final_content = removing_aliases + f"\n\nOriginal Folder Path for Context -> {current_file.parent.relative_to(path).as_posix()}"  # For me to save relative file path to the end of file
        with open(current_file, "w", encoding='utf-8') as f:
            f.write(final_content)
        f1.write("\n" * 2)

        # Виправлено: беремо нову назву зі словника, або залишаємо стару, якщо її там немає
        new_doc_name = dictionary_of_links.get(current_file.stem, current_file.stem)
        f1.write(f"# File Name: {new_doc_name}\n\n")

        f1.write(final_content)

        # Виправлено відступ: перейменування має бути всередині циклу for
        original_filename = current_file.stem
        if original_filename in dictionary_of_links:
            new_filename = dictionary_of_links[original_filename]
            new_path = current_file.parent / f"{new_filename}.md"
            current_file.rename(new_path)

print("."*64)

#Save results to JSON (dump)
with open(path / "dictionary_prefs_md.json", "w", encoding='utf-8') as f:
    json.dump(dictionary_of_links, f, ensure_ascii=False, indent=4)
print("Changes was saved in dictionary_prefs.json")

print("."*64)

#For .canvas files
with tqdm(total=len(canvas_files), desc="Progress .canvas", colour="yellow") as pbar_canvas:
    for current_file in canvas_files:
        with open(current_file, "r", encoding='utf-8') as f:
            canvas_data = json.load(f)
            for node in canvas_data["nodes"]:
                if node["type"] == "text":
                    node["text"] = re.sub(r'\[\[(.*?)]]', replacer, node["text"])
                elif node["type"] == "file":
                    canvas_file_path = pl.PurePosixPath(node["file"])
                    name_without_extension = canvas_file_path.stem
                    if name_without_extension in dictionary_of_links:
                        new_filename = dictionary_of_links[name_without_extension]
                        node["file"] = str(canvas_file_path.with_name(new_filename))
        with open(current_file, "w", encoding='utf-8') as f:
            json.dump(canvas_data, f, ensure_ascii=False, indent=4)
        pbar_canvas.update(1)
print(f"Changed {len(canvas_files)} links in .canvas files!\n", "."*64, "\nThanks for Using!!!\nCreated by CoinGH :)\n", "."*64)
time.sleep(6.7)
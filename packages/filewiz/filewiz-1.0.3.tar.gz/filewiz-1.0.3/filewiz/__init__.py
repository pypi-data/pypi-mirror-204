from pathlib import Path
import re
import sys

from wizlib.rlinput import rlinput

PATTERN = re.compile(r'\d{8}\-([a-zA-Z0-9-]+)\.(\w+)')

def get_parts(root:Path, sub:str):
    """Return a set of past filename parts"""
    parts = set()
    for year in root.iterdir():
        if year.name.isdigit():
            subdir = year / sub
            if subdir.is_dir():
                for file in subdir.iterdir():
                    match = re.match(PATTERN, file.name)
                    if match:
                        parts.add(match.groups()[0])
    return parts

def move_file(source, root_dir:str):
    """Ask the user some questions then move the file"""
    root = Path(root_dir).expanduser()
    sourcepath = Path(source).expanduser()
    assert sourcepath.is_file()
    extension = sourcepath.suffix
    print("Only handling accounts")
    date = input("Date: ")
    account = input("Account: ")
    parts = get_parts(root, account)
    part = rlinput("Part: ", options=parts)
    year = date[:4]
    dirpath = root / year / account
    if not dirpath.exists():
        confirm = rlinput(f"Create {dirpath}? ", default="yes")
        if confirm.startswith('y'):
            dirpath.mkdir(parents=True)
    targetpath = dirpath / f"{date}-{part}{extension}"
    if targetpath.exists():
        print(f"File exists at {targetpath}")
    else:
        confirm = rlinput(f"Move file to {targetpath}? ", default="yes")
        if confirm.startswith('y'):
            sourcepath.rename(targetpath)

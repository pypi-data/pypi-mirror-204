import json
import os
from typing import List, TypedDict

KUKI_PATH = os.path.join(os.getcwd(), "kuki.json")


class Kuki(TypedDict):
    package: str
    version: str
    description: str
    author: str
    git: str
    dependencies: List[str]


def generate_json(package: str, description="", author="", git=""):
    overwrite = ""
    if os.path.exists(KUKI_PATH):
        overwrite = input("kuki.json already exists, overwrite: (yes) ").strip()
        overwrite = overwrite.trim
    if overwrite or overwrite.lower() in ["n", "no"]:
        return
    kuki: Kuki = {
        "package": package,
        "version": "0.0.1",
        "description": description,
        "author": author,
        "git": git,
    }
    kuki_json = json.dumps(kuki, indent=2)
    print("About to write to {}".format(KUKI_PATH))
    print()
    print(kuki_json)
    proceed = input("Is this OK? (yes) ").strip()
    if not proceed or proceed.lower() == "yes":
        dump_json(kuki_json)


def init():
    dir = os.path.basename(os.getcwd())
    package = input("package name: ({}) ".format(dir)).strip()
    if not package:
        package = dir
    description = input("description: ").strip()
    git = input("git repository: ").strip()
    author = input("author: ").strip()

    generate_json(package, description, author, git)


def dump_json(json: str):
    with open(KUKI_PATH, "w") as out:
        out.write(json)


def exits():
    return os.path.exists(KUKI_PATH)


def roll_up_version(type: str):
    kuki: Kuki = json.load(KUKI_PATH)
    [major, minor, patch] = list(map(int, kuki["version"].split(".")))
    if type == "patch":
        patch += 1
    elif type == "minor":
        minor += 1
        patch = 0
    elif type == "major":
        major += 1
        minor = 0
        patch = 0
    version = "{}.{}.{}".format(major, minor, patch)
    kuki.version = version
    dump_json(json.dumps(kuki, indent=2))

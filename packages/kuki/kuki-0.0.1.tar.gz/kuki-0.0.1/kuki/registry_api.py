import json

import requests
from requests.auth import HTTPBasicAuth

from . import config_api

config = config_api.read_config()
registry = config.get("registry", "http://0.0.0.0:4873/")
token = config.get("token", "")

user_url = registry + "-/user/org.couchdb.user:"
search_url = registry + "-/v1/search?text={}"


def add_user(user: str, password: str, email: str):
    payload = {"name": user, "password": password, "email": email}
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    r = requests.put(user_url + user, json.dumps(payload), headers=headers)

    if r.status_code == 201:
        print("the user {} has been added".format(user))
        token = r.json()["token"]
        config_api.update_config("token", token)
    else:
        print("failed to add user: " + user)
        print("status code: {}, error: {}".format(r.status_code, r.json()["error"]))


def login(user: str, password: str):
    basic_auth = HTTPBasicAuth(user, password)
    payload = {"name": user, "password": password}
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    r = requests.put(user_url + user, json.dumps(payload), headers=headers, auth=basic_auth)
    if r.status_code == 201:
        print("you are authenticated as '{}'".format(user))
        token = r.json()["token"]
        config_api.update_config("token", token)
    else:
        print("failed to authenticated as '{}'".format(user))
        print("status code: {}, error: {}".format(r.status_code, r.json()["error"]))


def search_package(package: str):
    r = requests.get(search_url.format(package))
    print(
        "{:25.25} | {:30.30} | {:30.30} | {:10.10} | {:10.10} | {:20.20}".format(
            "NAME", "DESCRIPTION", "AUTHOR", "DATE", "VERSION", "KEYWORDS"
        )
    )
    for obj in r.json()["objects"]:
        pkg = obj["package"]
        print(
            "{:25.25} | {:30.30} | {:30.30} | {:10.10} | {:10.10} | {:20.20}".format(
                pkg["name"],
                pkg["description"],
                pkg["author"]["name"],
                pkg["time"]["modified"],
                pkg["dist-tags"]["latest"],
                " ".join(pkg["keywords"]),
            )
        )

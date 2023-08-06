import json
from pathlib import Path
from typing import TypedDict

CONFIG_FILEPATH = Path.joinpath(Path.home(), ".kukirc.json")


class Kukirc(TypedDict):
    registry: str
    token: str


def read_config() -> Kukirc:
    if not Path.exists(CONFIG_FILEPATH):
        with open(CONFIG_FILEPATH, "w") as handle:
            handle.write(json.dumps({}))
        return {}
    else:
        with open(CONFIG_FILEPATH, "r") as handle:
            return json.load(handle)


def update_config(field: str, value: str):
    print("update registry to " + value)
    kukirc = read_config()
    kukirc[field] = value
    write_config(kukirc)


def write_config(config: Kukirc):
    print("update kukirc")
    with open(CONFIG_FILEPATH, "w") as handle:
        handle.write(json.dumps(config, indent=2))

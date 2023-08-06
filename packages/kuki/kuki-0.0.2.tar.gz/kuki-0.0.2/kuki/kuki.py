import argparse

from . import config_api, kukijson, registry_api

parser = argparse.ArgumentParser(description="Kdb Ultimate pacKage Installer CLI")

group = parser.add_mutually_exclusive_group()

group.add_argument(
    "-a",
    "--adduser",
    action="store_true",
    default=False,
    help="add an user to the registry site",
)

group.add_argument(
    "-c",
    "--config",
    type=str,
    help="config kukirc, use format 'field=value'",
)

group.add_argument(
    "-d",
    "--download",
    type=str,
    help="download a kdb package of latest version, use '@' to specify a version",
)


group.add_argument(
    "-i",
    "--install",
    type=str,
    help="install a kdb package of latest version, use '@' to specify a version",
)

group.add_argument(
    "--init",
    action="store_true",
    default=False,
    help="init a kdb package",
)

group.add_argument(
    "--login",
    action="store_true",
    default=False,
    help="login to registry",
)

group.add_argument(
    "-p",
    "--publish",
    action="store_true",
    default=False,
    help="publish a kdb package using kuki.json",
)

group.add_argument(
    "-s",
    "--search",
    type=str,
    help="search a kdb package",
)


group.add_argument(
    "-u",
    "--uninstall",
    type=str,
    help="uninstall a kdb package, use '@' to specify a version",
)

group.add_argument(
    "-v",
    "--version",
    type=str,
    choices=["patch", "minor", "major"],
    help="roll up version(patch, minor, major)",
)

args = parser.parse_args()


def main():
    if args.config:
        arg_dict = dict()
        for arg in args.config.split(" "):
            key, value = arg.split("=")
            arg_dict[key] = value
        for key in ["token", "registry"]:
            if arg_dict.get(key):
                config_api.update_config(key, arg_dict.get(key))
    elif args.init:
        kukijson.init()
    elif args.adduser:
        user = input("Username: ")
        password = input("Password: ")
        email = input("Email: ")
        registry_api.add_user(user, password, email)
    elif args.login:
        user = input("Username: ")
        password = input("Password: ")
        registry_api.login(user, password)
    elif args.search:
        registry_api.search_package(args.search)
    else:
        if not kukijson.exits():
            print(
                "kuki.json is not generated yet, use 'kuki --init' to initialize the package first"
            )
            return
        elif args.version:
            kukijson.roll_up_version(args.version)
        elif args.publish:
            pass

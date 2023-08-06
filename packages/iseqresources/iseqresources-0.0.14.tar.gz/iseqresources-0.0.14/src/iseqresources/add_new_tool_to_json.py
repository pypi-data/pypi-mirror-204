#!/usr/bin/env python3

import argparse
from iseqresources.add_tool import AddTool
from utils import utils
import os


__version__ = '0.0.14'


GITLAB_TOKEN=os.environ.get("GITLAB_TOKEN")


def info_text():
    return '''Press 0 to exit
Press 1 to add a tool from github
Press 2 to add a tool from website
Press 3 to add a tool from website without specific released version'''


def add_tool_or_database(gitlab_token="", json_file="https://gitlab.com/intelliseq/iseqresources/-/raw/main/json/tools.json"):
    if not gitlab_token and json_file.startswith("https://"):
        gitlab_token = utils.get_gitlab_token()
    obj = AddTool(json_file, gitlab_token)
    switcher={
        0: lambda : obj.exit(),
        1: lambda : obj.add_github_tool(),
        2: lambda : obj.add_website_tool_with_released_version(),
        3: lambda : obj.add_website_tool_without_released_version()
    }
    choice = 1
    while choice != 0:
        print(info_text())
        choice = int(input('Enter a number of your choice: '))
        switcher.get(choice, lambda : "ERROR: Invalid Operation")()


def main():
    parser = argparse.ArgumentParser(description='Add new tool to json file')
    parser.add_argument('--input-json', type=str, required=False,
                        help='Json file to which to enter a new field')
    parser.add_argument('--tools', action='store_true', default=False, 
                        help='Add new tool')
    parser.add_argument('--databases', action='store_true', default=False, 
                        help='Add new database')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s {}'.format(__version__))
    args = parser.parse_args()

    if args.input_json:
        add_tool_or_database(
            gitlab_token=GITLAB_TOKEN,
            json_file=args.input_json)
    else:
        if args.databases:
            json_file = "https://gitlab.com/intelliseq/iseqresources/-/raw/main/json/databases.json"
        else:
            json_file = "https://gitlab.com/intelliseq/iseqresources/-/raw/main/json/tools.json"    
        add_tool_or_database(
            gitlab_token=GITLAB_TOKEN, 
            json_file=json_file)


if __name__ == "__main__":
    main()

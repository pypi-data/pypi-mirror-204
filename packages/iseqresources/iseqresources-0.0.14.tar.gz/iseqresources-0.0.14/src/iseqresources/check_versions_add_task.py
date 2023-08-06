#!/usr/bin/env python3

import argparse
from tqdm import tqdm
from utils import utils
from iseqresources.check_version import CheckVersion
from iseqresources.add_task_to_jira import AddTaskToJira
import os


__version__ = '0.0.14'


GITHUB_TOKEN=os.environ.get("GITHUB_TOKEN")
GITLAB_TOKEN=os.environ.get("GITLAB_TOKEN")
JIRA_EMAIL=os.environ.get("JIRA_EMAIL")
JIRA_TOKEN=os.environ.get("JIRA_TOKEN")


def check_for_new_version(github_token, jira_email, jira_token, gitlab_token="", 
                        json_file="https://gitlab.com/intelliseq/iseqresources/-/raw/main/json/tools.json", 
                        info_json="https://gitlab.com/intelliseq/iseqresources/-/raw/main/json/info.json"):
    if not gitlab_token and json_file.startswith("https://"):
        gitlab_token = utils.get_gitlab_token()
    resources_dict = utils.load_json(json_file, gitlab_token)
    jira_project_info = utils.load_json(info_json, gitlab_token)
    if not github_token:
        github_token = utils.get_github_token()
    if not jira_email:
        jira_email, jira_token = utils.get_jira_auth(server=jira_project_info['server'], epic_id=jira_project_info['epic_id'])
    test_name = {
        "github": lambda : obj.check_github_repo(),
        "url-check": lambda : obj.check_url_with_released_version(),
        "update-every-nth-month": lambda : obj.check_url_without_released_version()
    }
    for tool_or_database in tqdm(resources_dict):
        obj = CheckVersion(tool_or_database, github_token)
        create_task_in_jira = test_name.get(tool_or_database["test"], lambda : "ERROR: Invalid test")()
        # create task in jira if there is new version of tool/database
        if create_task_in_jira:
            jira = AddTaskToJira(tool_or_database, jira_email, jira_token, jira_project_info=jira_project_info)
            jira.add_task_to_jira()
    if json_file.startswith("https://"):
        file = json_file.split("/")[-1]
        utils.save_json_to_gitlab(resources_dict, gitlab_token, file)
    else:
        utils.save_json(json_file, resources_dict)


def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--input-json', type=str, required=False,
                        help='Json file to which to enter a new field')
    parser.add_argument('--info-json', type=str, required=False,
                        help='Json file with info about JIRA project (server, epic_id and project_id)')
    parser.add_argument('--tools', action='store_true', default=False, 
                        help='Check tools newest versions')
    parser.add_argument('--databases', action='store_true', default=False, 
                        help='Check databases newest versions')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s {}'.format(__version__))
    args = parser.parse_args()
    
    if args.input_json:
        check_for_new_version(github_token=GITHUB_TOKEN,
            gitlab_token=GITLAB_TOKEN,
            jira_email=JIRA_EMAIL,
            jira_token=JIRA_TOKEN,
            json_file=args.input_json, 
            info_json=args.info_json)
    else:
        if args.databases:
            json_file = "https://gitlab.com/intelliseq/iseqresources/-/raw/main/json/databases.json"
        else:
            json_file = "https://gitlab.com/intelliseq/iseqresources/-/raw/main/json/tools.json"
        check_for_new_version(github_token=GITHUB_TOKEN,
            gitlab_token=GITLAB_TOKEN,
            jira_email=JIRA_EMAIL,
            jira_token=JIRA_TOKEN,
            json_file=json_file)


if __name__ == "__main__":
    main()

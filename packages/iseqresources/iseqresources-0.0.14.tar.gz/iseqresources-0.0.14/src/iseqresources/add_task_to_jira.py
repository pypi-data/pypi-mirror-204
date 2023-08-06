from jira import JIRA


class AddTaskToJira:
    
    def __init__(self, tool: dict, email: str, token: str, jira_project_info: dict):
        self.tool = tool
        self.email = email
        self.token = token
        self.server = jira_project_info["server"]
        self.epic_id = jira_project_info["epic_id"]
        self.project_key = jira_project_info["project_key"]
        self.jira_connection = self.jira_auth()
        self.epic = self.connect_epic()

    def jira_auth(self):
        return JIRA(basic_auth=(self.email, self.token), server=self.server)

    def connect_epic(self):
        return self.jira_connection.issue(self.epic_id)

    def create_issue_dict(self):
        tasks = "\n* ".join(self.tool["update_task"])
        dockers = ""
        if "update_docker" in self.tool:
            dockers = "\n* ".join(self.tool["update_docker"])
        main_text = f'Obecna wersja narzędzia {self.tool["name"]}: {self.tool["current_version"]}; \n\
              Najnowsza wersja narzędzia: {self.tool["newest_version"]}; \n\
              Należy zaktualizować taski:\n* {tasks} \n\n'
        dockers_text = f" Należy zaktualizować dockery:\n* {dockers}"
        issue_dict = {
            'project': {'key': self.project_key},
            'summary': f'Aktualizacja {self.tool["name"]}',
            'description': main_text + dockers_text if dockers else main_text,
            'issuetype': {'name': 'Task'}
        }
        return issue_dict
    
    def create_issue_dict_subtask_before(self, tool: dict):
        issue_dict_subtask = {
            'project': {'key': self.project_key},
            'summary': f'Aktualizacja bazy {tool["name"]}',
            'description': f'Instrukcja aktualizowania bazy: {tool["how_to_update"]}',
            'issuetype': {'name': 'Task'}
        }
        return issue_dict_subtask
    
    def create_issue_dict_subtask_after(self, tool: dict):
        tasks = "\n* ".join(tool["update_task"])
        dockers = "\n* ".join(tool["update_docker"])
        instruction = f'Instrukcja aktualizowania bazy: {tool["how_to_update"]}; \n'
        main_text = f'Należy zaktualizować taski:\n* {tasks} \n\n\
            Należy zaktualizować dockery:\n* {dockers}'
        issue_dict_subtask = {
            'project': {'key': self.project_key},
            'summary': f'Aktualizacja bazy {tool["name"]}',
            'description': instruction + main_text if tool["how_to_update"] else main_text,
            'issuetype': {'name': 'Task'}
        }
        return issue_dict_subtask
    
    def create_issue_jira(self, task_or_subtask: str, tool: dict):
        task_or_subtask_dict = {
            "task": lambda : self.create_issue_dict(),
            "subtask_before": lambda : self.create_issue_dict_subtask_before(tool),
            "subtask_after": lambda : self.create_issue_dict_subtask_after(tool)
        }
        return self.jira_connection.create_issue(fields=task_or_subtask_dict.get(task_or_subtask, lambda : "ERROR: Invalid Operation")())

    def add_task_to_jira(self):
        # task
        new_issue = self.create_issue_jira("task", {})
        new_issue.update(fields={'parent': {'id': self.epic.id}})
        # subtask
        if "update_database_before" in self.tool:
            for tool in self.tool["update_database_before"]:
                new_issue_subtask = self.create_issue_jira("subtask_before", tool)
                self.jira_connection.create_issue_link(type='blocks', inwardIssue=new_issue_subtask.key, outwardIssue=new_issue.key)
                new_issue_subtask.update(fields={'parent': {'id': self.epic.id}})
        elif "update_database_after" in self.tool:
            for tool in self.tool["update_database_after"]:
                new_issue_subtask = self.create_issue_jira("subtask_after", tool)
                self.jira_connection.create_issue_link(type='is blocked by', inwardIssue=new_issue_subtask.key, outwardIssue=new_issue.key)            
                new_issue_subtask.update(fields={'parent': {'id': self.epic.id}})

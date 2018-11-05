import settings
from todoist.api import TodoistAPI

from datetime import timedelta
from todolist import Todolist


class Todoist(Todolist):
    def __init__(self, list_name=None):
        print("Initializing Todoist API...")
        self.api = TodoistAPI(settings.todoist_key)  # TODO: other users
        self.api.sync()
        self.Project_ID = settings.todoist_project_key# TODO: add option for other projects
        self.project_name = list_name

        '''if list_name is not None:
            projects = self.api.projects
            for project in projects.all('name = ' + list_name):
                if project['name'] == list_name:
                    self.Project_ID = project['id']'''

    def add_task(self, name, desc=None, labels=None, due=None, assign=None):
        
        if labels is not None:
            for label in labels:
                name = name + ' @' + label
        if self.project_name is not None:
            name = name + ' #' + self.project_name
        if due is None:
            task = self.api.items.add(name, self.Project_ID)
        else:
            due = due - timedelta(hours=4)
            task = self.api.items.add(name, self.Project_ID, due_date_utc=due)

        task_id = task['id']

        # PREMIUM!
        #if desc is not None:
        #    self.api.notes.add(task_id, desc)

        print("\tAdded task: Name - " + name)
        self.api.commit()

        # TODO: optional - assign


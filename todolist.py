LABELS = None  # ['Kamat']


class Todolist:
    def __init__(self):
        pass

    def add_task(self, name, desc=None, labels=None, due=None, assign=None):

        pass

    def send_tasks(self, tasks):
        count = 0
        for task in tasks:
            name = task['course'] + ' - ' + task['name']
            desc = 'Due date: ' + task['date_txt']

            self.add_task(name, desc=desc, due=task['date'], labels=LABELS)
            count += 1
        print("Added " + str(count) + " tasks.")

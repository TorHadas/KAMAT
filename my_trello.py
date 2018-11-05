
# pip install py-trello
import settings
from trello import TrelloClient

from datetime import timedelta

from todolist import Todolist


class Trello(Todolist):
    def __init__(self, list_name, board_id):
        print("Initializing Trello API...")
        client = TrelloClient(
            api_key=settings.trello_key,
            api_secret=settings.trello_secret
        )

        self.board = client.get_board(board_id)
        lists = self.board.all_lists()

        for lst in lists:
            if lst.name == list_name:
                self.list = lst
                break
                # TODO : add exception if not found

    def add_task(self, name, desc=None, labels=None, due=None, assign=None):
        if due is None:
            due = "null"
        else:
            due = due - timedelta(hours=7)
            due = str(due)
        self.list.add_card(name, desc, None, due, None, None, assign) # TODO: assign label
        print("\tAdded task: Name - " + name)

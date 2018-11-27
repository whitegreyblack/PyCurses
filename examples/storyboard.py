"""Storyboard.py

Implements a JIRA like board with three major columns:
    Todo: stories/tasks which has been reviewed and in queue to be worked on
    In-Work: stories/tasks which are currently being worked on. Keep it to one
    Done: stories/tasks which have been completed and kept up to review work

Basic outline:
+---------------------+----------------------+----------------------+
|         TODO        |         WORK         |         DONE         |
+---------------------+----------------------+----------------------+
|      Task #XZ       |        Task #XY      |       Task #XX       |
|      Task #YX       |                      |       Task #XW       |
+---------------------+----------------------+----------------------+

Classes:
    Board: Manager object to hold stories.
    Story: Main object to be placed on board. Holds task descriptions.
    Task: Sub stories that may be added to stories.

Operations:
    Board: [ Add | Mov | Rmv | Del ] [ Stories ]
    Story: [ Add | Mov | Rmv | Del ] [ self | Tasks ]
    Task:  [ Add | Del ]

FRONTEND: BLT - keyboard movement, keyboard actions. Mouse later.
BACKEND: SQLite - there needs to be persistence every time program is opened.
         
Notes: Firstly use a text file to hold the DB. Possibly use JSON to hold info.
       For db, will need a way to hold the board, story, task data with their
       own separate tables.
"""
import sqlite3

class Board(object):
    """Should initialize objects by calling database for story data"""
    def __init__(self):
        self.column_todo = [] # these columns will be ordered by:
        self.column_work = [] #     issue number asc;
        self.column_done = [] #     date issued asc;

        self.visible_todo = None
        self.visible_work = None
        self.visible_done = None

    def __repr__(self):
        todos = len(self.column_todo)
        works = len(self.column_work)
        dones = len(self.column_done)
        return f"Board: todo({todos}) work({works}) done({done})"

    @property
    def board(self):
        """Returns a string representation of the board"""
        border_signs = '=' * 8
        divide_signs = '-' * 8
        empty_spaces = ' ' * 8
        todos_header = f"{' '*2}todo{' '*2}"
        works_header = f"{' '*2}work{' '*2}"
        dones_header = f"{' '*2}done{' '*2}"
        return f"""
Board:
+{border_signs}+{border_signs}+{border_signs}+
|{todos_header}|{works_header}|{dones_header}|
+{border_signs}+{border_signs}+{border_signs}+
|{empty_spaces}|{empty_spaces}|{empty_spaces}|
+{divide_signs}+{divide_signs}+{divide_signs}+
|{empty_spaces}|{empty_spaces}|{empty_spaces}|
+{border_signs}+{border_signs}+{border_signs}+
"""[1:]

    def import_json(self, filename):
        """board example layout
        {
            {
            'story 1': {
                'column': 'work',
                'subtask a': 'x',
                'subtask b': 'y'
            },
            'story 2': {
                'column': 'done',
                'subtask a': 'z'
            }
        }
        board[story1][column] = 'done'
        """
        pass

    def import_database(self, tablename):
        pass

    def order_column(self, columnname):
        newcolumnlist = sorted(getattr(self, columnname), 
                               key=lambda x: x.created_date)
        setattr(self, columnname.split("_")[1], newcolumnlist)

    def draw_blt(self):
        """Returns the storyboard as a newline delimited string"""
    
    def draw_term(self):
        """Prints the storyboard using ASCII onto terminal"""
        pass

class Story(object):
    def __init__(self):
        pass

class SubStory(Story):
    def __init__(self):
        pass

class Database(object):
    '''Singleton database object design?'''
    pass
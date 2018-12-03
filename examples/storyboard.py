"""
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
import json
import abc
from examples.calendargrid import YearMonthDay
import itertools

class BoardOptions:
    BoardOff = 0
    TodoOnly = 1
    WorkOnly = 2
    TodoWorkOnly = 3
    DoneOnly = 4
    TodoDoneOnly = 5
    WorkDoneOnly = 6
    TodoWorkDone = 7
    ColorOn = 8

class DataFormat:
    SQLite = 1
    JSON = 2
    YAML = 4

class Status:
    Pipe = 0
    Unassigned = 1
    InDev = 2
    Developed = 3

    states = {
        Pipe: "Todo",
        InDev: "Work",
        Developed: "Done",
    }

    def __init__(self, code):
        self.code = code
        self.name = Status.states[code]
    def __str__(self):
        return f"Status({self.name})"
    def __repr__(self):
        return f"Status(status={self.code}:{self.name})"

class Board(object):
    """Should initialize objects by calling database for story data"""
    def __init__(self, options):
        self.column_todo = [] # these columns will be ordered by:
        self.column_work = [] #     issue number asc;
        self.column_done = [] #     date issued asc;

        self.visible_todo = None
        self.visible_work = None
        self.visible_done = None

        self.options = options
        self.stories = dict()

    def __repr__(self):
        todos = len(self.column_todo)
        works = len(self.column_work)
        dones = len(self.column_done)
        return f"Board: todo({todos}) work({works}) done({done})"

    @property
    def stories(self):
        return self.__stories

    @stories.setter
    def stories(self, value):
        self.__stories = value

    def stories_by_status(self, code):
        return [s for s in self.stories.values() if s.status.code == code]

    @property
    def board(self):
        """Returns a string representation of the board"""
        cell_size = 25
        # base cells
        border_signs = '=' * cell_size
        divide_signs = '-' * cell_size
        empty_spaces = ' ' * cell_size

        todos_header = "TODO".center(cell_size + 1)
        works_header = "WORK".center(cell_size + 3)
        dones_header = "DONE".center(cell_size + 1)

        col_div = " "

        if self.options & BoardOptions.ColorOn == BoardOptions.ColorOn:
            todos_header = f"[bkcolor=#0052cc]{todos_header}[/bkcolor]"
            works_header = f"[bkcolor=#594300]{works_header}[/bkcolor]"
            dones_header = f"[bkcolor=#14892c]{dones_header}[/bkcolor]"        
            col_div = "[bkcolor=black] [/bkcolor]"

        todos = self.stories_by_status(Status.Pipe)
        longest_col = max(len(todos), 0)

        """
        COLOR:
            "#2472c8": blue
            "#cd3131": red
            "#e5e510": yellow
            "#0dbc79": green
        """

        combine = list(itertools.zip_longest(todos, [], []))
        # populate cells now
        inner_cells = []
        for i, (t, w, d) in enumerate(itertools.zip_longest(todos, [], [])):
            todo = t.description[:26].strip().center(cell_size + 1)
            signs = divide_signs
            extra = '-'
            if i == longest_col - 1:
                signs = border_signs
                extra = '='
            row = [todo, f"{empty_spaces}   ", f"{empty_spaces} "]
            if self.options & BoardOptions.ColorOn == BoardOptions.ColorOn:
                for i, (col, color) in enumerate(zip(row, ["#dfe1e6","#ffd351", "#b2d8b9"])):
                    row[i] = f"[bkcolor={color}]{col}[/bkcolor]"
            inner_cells.append(''.join(row))
        inner_cells = ''.join(inner_cells)

        if self.options & BoardOptions.ColorOn == BoardOptions.ColorOn:
            return f"""
+{border_signs}+{border_signs}{'='}+{border_signs}+
{todos_header}{works_header}{dones_header}
{inner_cells}
"""[1:]
        else:
            return inner_cells
    def import_using(self, dataformat, filename):
        if dataformat == DataFormat.SQLite:
            self.import_database(filename)
        elif dataformat == DataFormat.JSON:
            self.import_json(filename)
        elif dataformat == DataFormat.YAML:
            self.import_yaml(filename)
        else:
            raise ValueError("Invalid Dataformat")

    def import_json(self, filename):
        """Handles retrieving of data from reading json file and
        raises any errors during this process.
        """
        with open(filename, 'r') as f:
            data = json.loads(f.read())
        for name, info in data.items():
            s = Story.from_json(name, info)
            self.stories.update({name: s})

    def import_yaml(self, tablename):
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

class BoardItem:
    def __init__(            
        self,
        story_name:str,
        created_date:YearMonthDay, 
        status:int, 
        description:str
    ):
        self.story_name = story_name
        self.created_date = created_date
        self.status = status
        self.description = description
    @abc.abstractmethod
    def from_json(self):
        pass
    def __str__(self):
        story = f"{self.description}, {self.status.name}"
        return f"{self.__class__.__name__}({story})"
    def __str__(self):
        story = f"{self.description}, {self.status.name}"
        return f"{self.__class__.__name__}({story})"

class Story(BoardItem):
    def __init__(self,
                 story_name:str,
                 created_date:YearMonthDay, 
                 status:int, 
                 description:str, 
                 tasks:dict=dict()):
        super().__init__(story_name, 
                         created_date, 
                         status,
                         description)
        self.tasks = tasks
    @classmethod
    def from_json(self, name, info):
        n = name
        c = YearMonthDay.from_json(info['created_date'])
        s = Status(info['status'])
        d = info['description']
        t = {
            Task.from_json(name, info)
                for name, info in info['tasks'].items()
        }
        return Story(n, c, s, d, t)
    def add_task(self, task):
        self.tasks.update(task)

class Task(BoardItem):
    def __init__(
            self, 
            task_name:str,
            created_date:YearMonthDay, 
            status:int, 
            description:str, 
        ):
        super().__init__(task_name,
                         created_date,
                         status,
                         description)
    @classmethod
    def from_json(self, name, info):
        n = name
        c = YearMonthDay.from_json(info['created_date'])
        s = info['status']
        d = info['description']
        return Task(n, c, s, d)

class Database(object):
    '''Singleton database object design?'''
    pass
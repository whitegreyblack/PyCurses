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
"""
import SQLite

class Board(object):
    """Should initialize objects by calling database for story data"""
    def __init__(self):
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
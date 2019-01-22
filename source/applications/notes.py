import curses
import curses.textpad

import datetime

import source.utils as utils
from source.application import Application
from source.controllers import NotesController
from source.database import NoteConnection
from source.models.models import Note, Text
from source.window import (DisplayWindow, HelpWindow, ScrollableWindow, Window,
                           WindowProperty, keypress_a)


class NewNoteWindow(HelpWindow):
    def __init__(self, screen, title_input, note_input, title, showing=False):
        super().__init__(screen, title, showing=False)
        self.title_input = title_input
        self.note_input = note_input
        self.subwin = screen.derwin(self.height, self.width, 2, 2)
        self.note_created = utils.EventHandler()

    def keypress_a(self, sender, **kwargs):
        self.opener = sender
        self.show(self)
        self.focus(self)

        self.clear()
        self.draw()
        self.window.addstr(1, 1, "Title for new note:")
        for i, c in enumerate(utils.divider(self.width)):
            self.window.addch(2, i, c)
        self.title_input.move(0, 0)

        # show the cursor for editing
        curses.curs_set(1)

        self.window.refresh()
        textbox = curses.textpad.Textbox(self.title_input, insert_mode=True)
        title = textbox.edit().strip()
        curses.curs_set(0)
        while not title.strip():
            self.clear()
            self.draw()
            self.window.addstr(1, 1, "Title for new note: ")
            self.window.addstr(6, 1, "Title cannot be empty!", curses.color_pair(3))
            for i, c in enumerate(utils.divider(self.width)):
                self.window.addch(2, i, c)
                self.window.addch(5, i, c)

            # show the cursor for editing
            curses.curs_set(1)
            self.title_input.move(0, 0)
            self.window.refresh()
            textbox = curses.textpad.Textbox(self.title_input, insert_mode=True)
            title = textbox.edit().strip()

        self.clear()
        self.draw()
        self.window.addstr(1, 1, "Note for new note. (Ctrl-G to finish)")
        for i, c in enumerate(utils.divider(self.width)):
            self.window.addch(2, i, c)
        self.note_input.move(0, 0)
        self.window.refresh()
        textbox = curses.textpad.Textbox(self.note_input, insert_mode=True)
        note = textbox.edit()

        print('title: ', title)
        print('note: ', note)
        date = datetime.datetime.today()
        
        model = Note(title, created=date, modified=date, note=note)
        self.on_note_created(model)

        # turn cursor off again
        curses.curs_set(0)

        self.unfocus(self)
        self.hide(self)
        self.refocus_opener(self)

    def on_note_created(self, note):
        self.note_created(self, data=note)

    def keypress_escape(self, sender, **kwargs):
        exit()


class NoteHelpWindow(HelpWindow):
    def keypress_f1(self, sender, **kwargs):
        if sender != self:
            sender.unfocus()
            self.set_opener = sender
            self.focus()
            self.show()
        else:
            self.unfocus()
            self.hide()
            self.refocus_opener()


class NoteScrollableWindow(ScrollableWindow):
    # data added event
    def data_added(self, sender, **kwargs):
        self.data = [d.title for d in kwargs['data']]

    # key events that fire on keypress
    def on_keypress_tab(self):
        self.keypresses.trigger(9, self)
    
    # key event handlers from fired events
    def keypress_btab(self, sender, **kwargs):
        sender.unfocus(self)
        self.focus(self)

    def keypress_down(self, sender, **kwargs):
        temp = self.index + 1
        if temp < len(self.data):
            self.index = temp
            self.data_changed(self)
    
    def keypress_up(self, sender, **kwargs):
        temp = self.index - 1
        if temp >= 0:
            self.index = temp
            self.data_changed(self)


class NoteDisplayWindow(DisplayWindow):
    # key events that fire on keypress
    def on_keypress_btab(self):
        self.keypresses.trigger(curses.KEY_BTAB, self)

    # key event handlers from fired events
    def data_changed(self, sender, **kwargs):
        self.dataobject = kwargs['model']

    def keypress_tab(self, sender, **kwargs):
        print(f"{sender}: tabbing to {sender}")
        sender.unfocus(self)
        self.focus(self)


class NoteApplication(Application):
    def unfocused(self):
        self.focused = None

    def focused(self, sender):
        self.focused = sender

    def focus_changed(self, sender, *args, **kwargs):
        print(f"{self.focused}: changing focus in application.focus_changed")
        self.focused = self.window.currently_focused
        if self.focused == None:
            self.focused = self.window
        print(f"Changed to {self.focused}")

    def build_application(self, rebuild=False, reinsert=False, examples=False):
        """Builds an application to view all notes"""
        screen = self.screen
        height, width = screen.getmaxyx()

        if not examples:
            self.controller = NotesController(
                NoteConnection(rebuild=rebuild), 
                reinsert=reinsert
            )
            self.data = self.controller.request_notes()
        else:
            self.data = [Note.random() for i in range(10)]

        print(self.data)

        self.window.title = 'Note Viewer Example'

        note_display = NoteDisplayWindow(
            screen.subwin(
                height - 2,
                utils.partition(width, 3, 2),
                1,
                utils.partition(width, 3, 1)
            ),
            title="Note viewer",
            dataobj=self.data[0] if self.data else None
        )

        note_explorer = NoteScrollableWindow(
            screen.subwin(
                height - 2,
                utils.partition(width, 3, 1),
                1,
                0
            ),
            title="Notes",
            title_centered=True,
            focused=True,
            data=[n.title for n in self.data],
            data_changed_handlers=(self.data_changed,)
        )

        help_window = NoteHelpWindow(
            screen.subwin(
                height // 3,
                utils.partition(width, 4, 2),
                utils.partition(height, 3, 1),
                utils.partition(width, 4, 1)
            ),
            title="Help Window",
            dataobj=Text.random()
        )

        create_window = NewNoteWindow(
            screen.subwin(
                height // 3,
                utils.partition(width, 4, 2),
                utils.partition(height, 3, 1),
                utils.partition(width, 4, 1)
            ),
            screen.subwin(
                (height // 3) - 7,
                utils.partition(width, 4, 2) - 2,
                utils.partition(height, 3, 1) + 3,
                utils.partition(width, 4, 1) + 1
            ),
            screen.subwin(
                (height // 3) - 4,
                utils.partition(width, 4, 2) - 2,
                utils.partition(height, 3, 1) + 3,
                utils.partition(width, 4, 1) + 1
            ),
            title="Add Note Window",
            showing=False
        )
        create_window.note_created.append(self.data_added)
        # application change event
        # self.on_data_changed.append(note_display.data_changed)

        # main window key press handlers
        self.window.changes.on(('focused', self.focus_changed))
        self.window.keypresses.on(
            (27, self.keypress_escape),
            (curses.KEY_F1, help_window.keypress_f1)
        )

        # scroll window key press handlers
        note_explorer.changes.on(('focused', self.focus_changed))
        note_explorer.keypresses.on(
            (27, self.keypress_escape),
            (9, note_display.keypress_tab),
            (curses.KEY_F1, help_window.keypress_f1),
            (curses.KEY_DOWN, note_explorer.keypress_down),
            (curses.KEY_UP, note_explorer.keypress_up),
            (ord('a'), create_window.keypress_a)
        )
        self.on_data_added.append(note_explorer.data_added)

        # display window key press handlers
        self.on_data_changed.append(note_display.data_changed)
        note_display.changes.on(
            ('focused', self.focus_changed),
            (27, self.keypress_escape),
            (351, note_explorer.keypress_btab),
            (curses.KEY_F1, help_window.keypress_f1)
        )

        # help window key press handlers
        help_window.changes.on(('focused', self.focus_changed))
        help_window.keypresses.on(
            (27, help_window.keypress_f1),
            (curses.KEY_F1, help_window.keypress_f1)
        )

        self.window.add_windows(
            note_explorer, 
            note_display, 
            help_window, 
            create_window
        )

        self.focused = self.window.currently_focused
    
    def build_application_with_properties(self, rebuild):
        """Uses window properties to initialize the windows"""
        pass

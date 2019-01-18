import curses
from source.application import Application
from source.window import (
    Window,
    ScrollableWindow,
    DisplayWindow,
    HelpWindow,
    WindowProperty,
    on_keypress_up,
    on_keypress_down
)
from source.models.models import Text
import source.utils as utils
from source.controllers import NotesController
from source.database import NoteConnection

class NoteWindow(Window):
    def on_keypress_f1(self):
        self.keypresses.trigger(curses.KEY_F1, self)

class NoteHelpWindow(HelpWindow):
    def keypress_f1(self, sender, **kwargs):
        # first things first
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
    def on_keypress_tab(self):
        self.keypresses.trigger(9, self)
    
    def keypress_btab(self, sender, **kwargs):
        sender.unfocus()
        self.focus()

class NoteDisplayWindow(DisplayWindow):
    def on_keypress_btab(self):
        self.keypresses.trigger(curses.KEY_BTAB, self)

    def keypress_tab(self, sender, **kwargs):
        print(f"{sender}: tabbing to {sender}")
        sender.unfocus()
        self.focus()

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

    def build_application(self, rebuild=False):
        """Builds an application to view all notes"""
        screen = self.screen
        height, width = screen.getmaxyx()

        self.controller = NotesController(NoteConnection(rebuild=rebuild))
        self.data = self.controller.request_notes()

        self.window.title = 'Note Viewer Example'

        note_display = NoteDisplayWindow(
            screen.subwin(
                height - 2,
                utils.partition(width, 3, 2),
                1,
                utils.partition(width, 3, 1)
            ),
            title="Note viewer"
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
            data_changed_handlers=(self.on_data_changed,)
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

        # main window key press handlers
        self.window.changes.on('focused', self.focus_changed)
        self.window.keypresses.on(27, self.keypress_escape)
        self.window.keypresses.on(curses.KEY_F1, help_window.keypress_f1)

        # scroll window key press handlers
        note_explorer.changes.on('focused', self.focus_changed)
        note_explorer.keypresses.on(27, self.keypress_escape)
        note_explorer.keypresses.on(9, note_display.keypress_tab)
        note_explorer.keypresses.on(curses.KEY_F1, help_window.keypress_f1)

        # display window key press handlers
        note_display.changes.on('focused', self.focus_changed)
        note_display.keypresses.on(27, self.keypress_escape)
        note_display.keypresses.on(351, note_explorer.keypress_btab)
        note_display.keypresses.on(curses.KEY_F1, help_window.keypress_f1)

        # help window key press handlers
        help_window.changes.on('focused', self.focus_changed)
        help_window.keypresses.on(27, help_window.keypress_f1)
        help_window.keypresses.on(curses.KEY_F1, help_window.keypress_f1)

        self.window.add_windows(note_explorer, note_display, help_window)
        self.focused = self.window.currently_focused
    
    def build_application_with_properties(self, rebuild):
        """Uses window properties to initialize the windows"""
        pass
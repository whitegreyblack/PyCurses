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

class NoteApplication(Application):
    def build_application(self, rebuild=False):
        """Builds an application to view all notes"""
        screen = self.screen
        height, width = screen.getmaxyx()

        self.controller = NotesController(NoteConnection(rebuild=rebuild))
        self.data = self.controller.request_notes()

        self.window.title = 'Note Viewer Example'

        note_display = DisplayWindow(
            screen.subwin(
                height - 2,
                utils.partition(width, 3, 2),
                1,
                utils.partition(width, 3, 1)
            ),
            title="Explorer"
        )

        note_explorer = ScrollableWindow(
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

        help_window = HelpWindow(
            screen.subwin(
                height // 3,
                utils.partition(width, 4, 2),
                utils.partition(height, 3, 1),
                utils.partition(width, 4, 1)
            ),
            title="Help Window",
            dataobj=Text.random(),
        )

        self.window.add_handlers(
            curses.KEY_F1,
            self.window.unfocus,
            help_window.set_opener,
            help_window.focus,
            help_window.show,
            self.on_focus_changed
        )
        note_explorer.add_handler(27, self.on_keypress_escape)
        note_explorer.add_handlers(
            9, 
            note_explorer.unfocus,
            note_display.focus,
            self.on_focus_changed
        )
        note_explorer.add_handlers(
            curses.KEY_F1,
            note_explorer.unfocus,
            help_window.set_opener,
            help_window.focus,
            help_window.show,
            self.on_focus_changed
        )
        note_display.add_handler(27, self.on_keypress_escape)
        note_display.add_handlers(
            351,
            note_display.unfocus,
            note_explorer.focus,
            self.on_focus_changed
        )
        note_display.add_handlers(
            curses.KEY_F1,
            note_display.unfocus,
            help_window.set_opener,
            help_window.focus,
            help_window.show,
            self.on_focus_changed
        )
        help_window.add_handlers(
            27,
            help_window.hide,
            help_window.unfocus,
            help_window.refocus_opener,
            self.on_focus_changed
        )
        help_window.add_handlers(
            curses.KEY_F1,
            help_window.hide,
            help_window.unfocus,
            help_window.refocus_opener,
            self.on_focus_changed
        )

        self.window.add_windows(note_explorer, note_display, help_window)
        self.focused = self.window.currently_focused
    
    def build_application_with_properties(self, rebuild):
        """Uses window properties to initialize the windows"""
        pass
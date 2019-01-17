import curses
from source.application import Application
from source.window import (
    Window,
    ScrollableWindow,
    DisplayWindow,
    WindowProperty
)
import source.utils

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
            )
        )
        self.data_changed_event.append(note_display.on_data_changed)
        self.window.add_window(note_display)

        note_explorer_props = WindowProperty({
            'title': "Notes",
            'title_centered': True,
            'focused': True,            
        })
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
        note_explorer.keypress_up_event = on_keypress_up
        note_explorer.keypress_down_event = on_keypress_down
        self.window.add_window(note_explorer)
        self.events[curses.KEY_DOWN].append(note_explorer.handle_key)
        self.events[curses.KEY_UP].append(note_explorer.handle_key)

        help_window = DisplayWindow(
            screen.subwin(
                height - 12,
                utils.partition(width, 4, 2),
                6,
                utils.partition(width, 4, 1)
            ),
            title="Help",
            dataobj=Text.random(),
            showing=False,
        )
        help_window.add_handler(ord('h'), help_window.toggle_showing)
        self.events[ord('h')].append(help_window.handle_key)
        self.window.add_window(help_window)

        self.focused = self.window.currently_focused
    
    def build_application_with_properties(self, rebuild):
        """Uses window properties to initialize the windows"""
        pass
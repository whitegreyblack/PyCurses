import curses
import curses.textpad
from source.application import Application
from source.window import (
    Window,
    ScrollableWindow,
    DisplayWindow,
    HelpWindow,
    WindowProperty,
    keypress_a
)
from source.models.models import (
    Text,
    Note
)
import source.utils as utils
from source.controllers import NotesController
from source.database import NoteConnection


class NewNoteWindow(Window):
    def __init__(self, screen, title, showing=False):
        super().__init__(screen, title, showing=False)
        self.subwin = screen.derwin(self.height, self.width, 2, 2)

    def keypress_a(self, sender, **kwargs):
        self.show(self)
        self.focus(self)
        self.clear()
        self.draw()
        self.window.refresh()
        # self.subwin.border()
        curses.curs_set(1)
        print(self.width, self.height)
        print(self.window.getmaxyx())
        # self.subwin.move(1, 1)
        textbox = curses.textpad.Textbox(self.subwin, insert_mode=True)
        text = textbox.edit()
        curses.curs_set(1)
        self.draw()
        self.subwin.border()
        self.window.addstr(1, 1, "Added note")
        self.window.refresh()
        self.window.getch()

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
            title="Add Note Window",
            showing=False
        )
        create_window.subwin = screen.subwin(
            (height // 3) - 2,
            utils.partition(width, 4, 2) - 2,
            utils.partition(height, 3, 1) + 1,
            utils.partition(width, 4, 1) + 1
        )
        # application change event
        # self.on_data_changed.append(note_display.data_changed)

        # main window key press handlers
        self.window.changes.on('focused', self.focus_changed)
        self.window.keypresses.on(27, self.keypress_escape)
        self.window.keypresses.on(curses.KEY_F1, help_window.keypress_f1)

        # scroll window key press handlers
        note_explorer.changes.on('focused', self.focus_changed)
        note_explorer.keypresses.on(27, self.keypress_escape)
        note_explorer.keypresses.on(9, note_display.keypress_tab)
        note_explorer.keypresses.on(curses.KEY_F1, help_window.keypress_f1)
        note_explorer.keypresses.on(curses.KEY_DOWN, note_explorer.keypress_down)
        note_explorer.keypresses.on(curses.KEY_UP, note_explorer.keypress_up)
        note_explorer.keypresses.on(ord('a'), create_window.keypress_a)

        # display window key press handlers
        self.on_data_changed.append(note_display.data_changed)
        note_display.changes.on('focused', self.focus_changed)
        note_display.keypresses.on(27, self.keypress_escape)
        note_display.keypresses.on(351, note_explorer.keypress_btab)
        note_display.keypresses.on(curses.KEY_F1, help_window.keypress_f1)

        # help window key press handlers
        help_window.changes.on('focused', self.focus_changed)
        help_window.keypresses.on(27, help_window.keypress_f1)
        help_window.keypresses.on(curses.KEY_F1, help_window.keypress_f1)

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
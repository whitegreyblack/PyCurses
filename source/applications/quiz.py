import curses
from source.applications.application import Application
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
    Question
)
import source.utils as utils
from source.controllers import QuizController
from source.database import QuizConnection


class QuizWindow(Window):
    def on_keypress_f1(self):
        self.keypresses.trigger(curses.KEY_F1, self)


class QuizHelpWindow(HelpWindow):
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


class QuizScrollableWindow(ScrollableWindow):
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


class QuizDisplayWindow(DisplayWindow):
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


class QuizApplication(Application):
    CLI_NAMES = ('question', 'questions', 'quiz', 'quizzes')
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
        """
        Builds an application to view all quizzes
        """
        screen = self.screen
        height, width = screen.getmaxyx()

        if not examples:
            self.controller = QuizController(
                connection=QuizConnection(rebuild=rebuild),
                reinsert=reinsert
            )
            self.data = list(self.controller.request_questions())
        else:
            self.data = [Question.random() for i in range(100)]

        print(self.data)
        self.window.title = 'Quiz Viewer Example'

        quiz_display = QuizDisplayWindow(
            screen.subwin(
                height - 2,
                utils.partition(width, 3, 2),
                1,
                utils.partition(width, 3, 1)
            ),
            title="Quiz viewer",
            dataobj=self.data[0] if self.data else None
        )

        quiz_explorer = QuizScrollableWindow(
            screen.subwin(
                height - 2,
                utils.partition(width, 3, 1),
                1,
                0
            ),
            title="Quizs",
            title_centered=True,
            focused=True,
            data=[q.question for q in self.data],
            data_changed_handlers=(self.data_changed,)
        )

        help_window = QuizHelpWindow(
            screen.subwin(
                height // 3,
                utils.partition(width, 4, 2),
                utils.partition(height, 3, 1),
                utils.partition(width, 4, 1)
            ),
            title="Help Window",
            dataobj=Text.random()
        )

        # application change event
        # self.on_data_changed.append(quiz_display.data_changed)

        # main window key press handlers
        self.window.changes.on('focused', self.focus_changed)
        self.window.keypresses.on(27, self.keypress_escape)
        self.window.keypresses.on(curses.KEY_F1, help_window.keypress_f1)

        # scroll window key press handlers
        quiz_explorer.changes.on('focused', self.focus_changed)
        quiz_explorer.keypresses.on(27, self.keypress_escape)
        quiz_explorer.keypresses.on(9, quiz_display.keypress_tab)
        quiz_explorer.keypresses.on(curses.KEY_F1, help_window.keypress_f1)
        quiz_explorer.keypresses.on(curses.KEY_DOWN, quiz_explorer.keypress_down)
        quiz_explorer.keypresses.on(curses.KEY_UP, quiz_explorer.keypress_up)

        # display window key press handlers
        self.on_data_changed.append(quiz_display.data_changed)
        quiz_display.changes.on('focused', self.focus_changed)
        quiz_display.keypresses.on(27, self.keypress_escape)
        quiz_display.keypresses.on(351, quiz_explorer.keypress_btab)
        quiz_display.keypresses.on(curses.KEY_F1, help_window.keypress_f1)

        # help window key press handlers
        help_window.changes.on('focused', self.focus_changed)
        help_window.keypresses.on(27, help_window.keypress_f1)
        help_window.keypresses.on(curses.KEY_F1, help_window.keypress_f1)

        self.window.add_windows(quiz_explorer, quiz_display, help_window)
        self.focused = self.window.currently_focused
    
    def build_application_with_properties(self, rebuild):
        """Uses window properties to initialize the windows"""
        pass

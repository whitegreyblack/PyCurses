import curses
from source.application import Application
from source.window import (
    Window,
    ScrollableWindow,
    DisplayWindow,
)
import source.utils

class TaskApplication(Application):
    def build_application(self, rebuild):
        """Build window objects and handlers for a todo task list app"""
        screen = self.screen
        height, width = screen.getmaxyx()

        self.data = [
            Task(f"task {i}", random.randint(0, 3), datetime.datetime.today())
                for i in range(50)
        ]

        self.window.title = "Tasks To Do"

        task_win = DisplayWindow(
            screen.subwin(
                utils.partition(height-2, 2, 1),
                width,
                utils.partition(height, 2, 1),
                0
            )
        )
        self.data_changed_event.append(task_win.on_data_changed)

        none_win = ScrollableWindow(
            screen.subwin(
                (height // 2) - 1,
                utils.partition(width, 4, 1),
                1, 
                0
            ),
            title="No Status",
            title_centered=True,
            data=[task.title for task in self.data if task.status_id == 0],
            data_changed_handlers=(self.on_data_changed,)
        )

        todo_win = ScrollableWindow(
            screen.subwin(
                (height // 2) - 1,
                utils.partition(width, 4, 1),
                1,
                utils.partition(width, 4, 1)
            ),
            title="Todo",
            title_centered=True,
            focused=True,
            data=[task.title for task in self.data if task.status_id == 1],
            data_changed_handlers=(self.on_data_changed,),
            eventmap=EventMap.fromkeys((
                ord('\t'),          # 9
                curses.KEY_BTAB,    # 351
                curses.KEY_DOWN,    # 258
                curses.KEY_UP,      # 259
                27
            ))
        )

        work_win = ScrollableWindow(
            screen.subwin(
                (height // 2) - 1,
                utils.partition(width, 4, 1),
                1,
                utils.partition(width, 4, 2)
            ),
            title="In-progress",
            title_centered=True,
            data=[task.title for task in self.data if task.status_id == 2],
            data_changed_handlers=(self.on_data_changed,)
        )

        done_win = ScrollableWindow(
            screen.subwin(
                (height // 2) - 1,
                utils.partition(width, 4, 1),
                1,
                utils.partition(width, 4, 3)
            ),
            title="Finished",
            title_centered=True,
            data=[task.title for task in self.data if task.status_id == 3],
            data_changed_handlers=(self.on_data_changed,)
        )

        # tasks without statuses
        none_win.add_handler(258, on_keypress_down)
        none_win.add_handler(259, on_keypress_up)
        none_win.add_handler(27, self.on_keypress_escape)
        none_win.add_handlers(9, (
            none_win.unfocus,
            todo_win.focus, 
            self.on_focus_changed
        ))

        # tasks in todo list
        todo_win.add_handler(258, on_keypress_down)
        todo_win.add_handler(259, on_keypress_up)
        todo_win.add_handler(27, self.on_keypress_escape)
        todo_win.add_handlers(351, (
            todo_win.unfocus,
            none_win.focus, 
            self.on_focus_changed
        ))
        todo_win.add_handlers(9, (
            todo_win.unfocus,
            work_win.focus, 
            self.on_focus_changed
        ))
        
        # in work tasks
        work_win.add_handler(258, on_keypress_down)
        work_win.add_handler(259, on_keypress_up)
        work_win.add_handler(27, self.on_keypress_escape)
        work_win.add_handlers(351, (
            work_win.unfocus,
            todo_win.focus, 
            self.on_focus_changed
        ))
        work_win.add_handlers(9, (
            work_win.unfocus,
            done_win.focus, 
            self.on_focus_changed
        ))

        # finished tasks
        done_win.add_handler(258, on_keypress_down)
        done_win.add_handler(259, on_keypress_up)
        done_win.add_handler(27, self.on_keypress_escape)
        done_win.add_handlers(351, (
            done_win.unfocus,
            work_win.focus, 
            self.on_focus_changed
        ))

        self.window.add_windows(
            none_win,
            todo_win,
            work_win,
            done_win,
            task_win
        )

        self.focused = self.window.currently_focused
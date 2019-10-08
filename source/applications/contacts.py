import random
from source.applications.application import Application
from source.window import (
    Window,
    WindowProperty,
    DisplayWindow,
    ScrollableWindow,
    PromptWindow
)
from source.database import PersonConnection
from source.controllers import PersonController 
from source.models.models import Person
import source.utils as utils

sample_first_male = [
    "Bob",
    "Robert",
    "william",
    "Bill",
]
sample_first_female = []
sample_middle_male = []
sample_middle_female = []
sample_last = [
    "McGregor",
    "Telrany",
]

class Name:
    def __init__(self, name):
        names = name.split()
        # assume either two or three names given corresponding to a person's
        # first, middle?, last name
        try:
            self.first, self.middle, self.last = names
        except:
            self.first, self.last = names
            self.middle = None

    def __str__(self):
        if self.middle:
            fullname = f"{self.first} {self.middle} {self.last}"
        else:
            fullname = f"{self.first} {self.last}"
        return fullname

    def __repr__(self):
        f, m, l = self.first, self.middle, self.last
        return f"Name(first={f}, middle={m}, last={l})"

    def __lt__(self, other):
        return unicode(self.first) < unicode(other.first)

    @staticmethod
    def random(self):
        pass

class Contact:
    def __init__(self, name, number, company=None):
        self.name = name
        self.number = number
        self.company = company

    def __repr__(self):
        # don't really need company info during repr
        return f"Contact(name={self.name}, number={self.number})"

class ContactsApplication(Application):
    CLI_NAMES = ('contact', 'contacts', 'names', 'people')
    def build_application(self, rebuild=False, reinsert=False, examples=False):
        """Work on window recursion and tree"""
        screen = self.screen
        height, width = screen.getmaxyx()

        self.controller = PersonController(
            PersonConnection(rebuild=rebuild), 
            reinsert=reinsert
        )

        # if no real data is present use fakedata to generate data
        if rebuild:
            self.data = [ self.controller.request_persons() ]
        else:
            self.data = [ Person.random() for _ in range(10) ]

        # main window
        self.window.title = 'Application Example 1'

        # display window
        display = DisplayWindow(
            screen.subwin(
                11,
                utils.partition(width, 5, length=3),
                1, 
                utils.partition(width, 5, length=2)
            ),
            title="Profile"
        )
        # self.on_data_changed.append(display.on_data_changed)

        # scroll window
        scroller = ScrollableWindow(
            screen.subwin(
                height - 2, 
                utils.partition(width, 5, length=2), 
                1, 
                0
            ),
            title="Directory",
            data=[str(n.name) for n in self.data],
            focused=True,
            # data_changed_handlers=(self.on_data_changed,)
        )

        # secondary display -- currently unused
        # adding sub windows to parent window
        unused = Window(
            screen.subwin(
                height - 13, 
                utils.partition(width, 5, length=3),
                12, 
                utils.partition(width, 5, length=2)
            ), 
            title='verylongtitlescree'
        )

        # prompt screen
        # prompt = PromptWindow(screen.subwin(3, width, height - 4, 0))

        self.window.add_windows(
            scroller,
            display,
            unused,
            # prompt
        )

    def build_application_with_properties(self, rebuild=False):
        pass

if __name__ == "__main__":
    pass
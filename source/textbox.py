import textwrap
from source.box import Box

class TextBox(Box):
    def __init__(self, p, width, height, text=None):
        super().__init__(p, width, height)
        self.text = text

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value):
        self.__text = value
        self.text_height = self.height - 2
        self.text_width = self.width - 2

    def format_text(self):
        textlist = textwrap.wrap(self.text, self.text_width)
        text = "\n".join(textlist)
        return text

    def split_text(self):
        return (
            self.text[:len(self.text) // 2],
            self.text[len(self.text) // 2 + 1:len(self.text)]
        )

    def split_x(self):
        super().split_x(cls=self.__class__)
        self.l.text, self.r.text = self.split_text()

    def split_y(self):
        super().split_y(cls=self.__class__)
        self.l.text, self.r.text = self.split_text()

    def blt_text(self):
        texts = []
        for text in (self.l, self.r):
            if text:
                texts.append(text.blt_text())
        if texts:
            return list(chain.from_iterable(texts))
        return [(self.a.x + 1, self.a.y + 1, self.format_text()),]
# Nov 1, 2023 3.50pm
# helpers
from tkinter import *
from tkinter.ttk import *

# classes
from actions import Actions
from web_classes import ImageFromHTML, ImageGetter, SVGMaker

# functions
from helpers import get_web_text


class ImageExtractor:
    def __init__(self):
        self.app = Tk()
        self.app.title("Image Extractor")
        self.app.resizable(0, 0)
        self.build_appframe()
        self.actions = Actions(self)
        self.style()
        self.get_web_text = get_web_text
        self.get_img_srcs = ImageFromHTML().feed
        self.build_svg = SVGMaker().start
        self.build_image = ImageGetter().start
        self.app.mainloop()

    def build_appframe(self):
        self.appframe = Frame(self.app, padding=(10))
        self.appframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.appframe.app = self
        self.appframe.columnconfigure(0, weight=1)

    def style(self):
        # Make it resize with the window
        self.app.columnconfigure(0, weight=1)
        self.app.rowconfigure(0, weight=1)
        self.appframe.columnconfigure(0, weight=1)

    def __getitem__(self, prop):
        return getattr(self.app, prop)


if __name__ == "__main__":
    app = ImageExtractor()

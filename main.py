"""First started Nov 1, 2023 3.50pm
"""

import sys
from tkinter import Frame, Tk, NSEW
from tkinter.ttk import Frame


class ImageExtractor:
    def __init__(self):
        self.app = Tk()
        self.app.title("Image Extractor")
        # self.app.resizable(width=0, height=0)  - looks like I'll need another typeshed PR
        self.build_appframe()
        self.style()

    def build_appframe(self):
        self.appframe = Frame(self.app, padding=(10))
        self.appframe.grid(column=0, row=0, sticky=NSEW)
        self.appframe.columnconfigure(0, weight=1)

    def style(self):
        # Make it resize with the window
        self.app.columnconfigure(0, weight=1)
        self.app.rowconfigure(0, weight=1)
        self.appframe.columnconfigure(0, weight=1)

    def __getitem__(self, prop: str):
        return getattr(self.app, prop)


if __name__ == "__main__":
    args = sys.argv
    if len(args) == 1:
        # Called without arguments
        try:
            from actions import Actions
            app = ImageExtractor()
            Actions(app)
            app.app.mainloop()
        except KeyboardInterrupt:
            pass
        finally:
            print("Exitting, thanks for using Image Extractor!")
    else:
        pass

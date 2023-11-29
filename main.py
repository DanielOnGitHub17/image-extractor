#Nov 1, 2023 3.50pm
#helpers
from tkinter import *
from tkinter.ttk import *
import os

#classes
from web_classes import get_html, ImageFromHTML, ImageGetter
from actions import Actions
from container import Container

class ImageExtractor:
    def __init__(self):
        self.app = Tk()
        self.app.title("Image Extractor")
        self.app.resizable(0, 0)
        self.build_appframe()
        self.actions = Actions(self)
        self.container = Container(self)
        self.style()
        self.get_html = get_html
        self.get_img_srcs = ImageFromHTML().feed
        self.build_image = ImageGetter().start
        self.app.mainloop()
        
    def build_appframe(self):
        self.appframe = Frame(self.app, padding=(10))
        self.appframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.appframe.app = self
        self.appframe.columnconfigure(0, weight=1)
        
    def style(self):
        #make it resize with the window
        self.app.columnconfigure(0, weight=1)
        self.app.rowconfigure(0, weight=1)
        
        self.appframe.columnconfigure(0, weight=1)
    
    def __getitem__(self, prop):
        return getattr(self.app, prop)
        
if __name__=="__main__":
    app = ImageExtractor()

# helpers
from tkinter import StringVar, Frame, Label, Entry
from tkinter.ttk import Button, Frame, Label, Entry
from tkinter.filedialog import askdirectory
import os

from main import ImageExtractor


# All the self.app stuff, maybe it should be in actions
class Actions:
    def __init__(self, app: ImageExtractor):
        self.url: str
        self.exiter: Button
        self.reseter: Button
        self.downloader: Button
        self.img_srcs: tuple[set[str], set[str]]
        self.app = app

        self.build()
        self.events()

    def build(self):
        self.frame = Frame(self.app.appframe, padding=(30, 0))
        self.frame.grid()
        column = 0

        for butn_prop in (
            ("downloader", "Download"),
            ("reseter", "Reset"),
            ("exiter", "Exit"),
        ):
            butn = Button(self.frame, text=butn_prop[1], width=15, state="disabled")
            butn.grid(row=0, column=column, padx=5, pady=5)
            column += 1
            setattr(self, butn_prop[0], butn)

        self.exiter.state(["!disabled"])
        # build status box
        self.status = StringVar(self.frame, "Input a url and click Get Images")
        self.status_display = Label(self.frame, textvariable=self.status)
        self.status_display.grid(row=1, column=0, columnspan=3, sticky="news", pady=5)
        # build search box
        self.value = StringVar(self.frame, "https://")
        self.search_box = Entry(self.frame, textvariable=self.value)
        self.search_box.grid(row=2, column=0, columnspan=3, pady=5, sticky="news")

        self.getter = Button(self.frame, text="Get Images")
        self.getter.grid(row=3, column=0, columnspan=3, pady=5, sticky="news")

    def events(self):
        def search():
            self.status.set("Searching...")
            # disable the getter
            self.getter.state(["disabled"])

            self.url = self.value.get()
            try:
                html = self.app.get_web_text(self.url)
                self.img_srcs = self.app.get_img_srcs(html, self.url)
            except Exception as error:
                print(error)
                raise error
                error = error.msg if hasattr(error, "msg") else "An error occured"
                self.status.set(error + ". click reset button to reset")
                self.reseter.state(["!disabled"])
                self.img_srcs = (set(), set())
                return

            self.reseter.state(
                ["!disabled"]
            )
            self.downloader.state(
                ["!disabled"]
            )
            self.status.set(
                "Done with searching. Click the Download button to download images"
            )

        def download():
            # self.status.set("Pick a folder")
            self.status.set("Downloading...")
            self.downloader.state(
                ["disabled"]
            )
            folder = askdirectory()
            if not folder:
                return reset()

            current = os.getcwd()
            os.chdir(folder)
            # download images
            src: str
            for src in self.img_srcs[0]:
                try:
                    self.app.build_image(self.url, src, folder)
                except Exception as error:
                    print(error, src, sep="\n")
                    self.status.set(f"couldn't download {src}")

            # download svgs
            for svg_text in self.img_srcs[1]:
                try:
                    self.app.build_svg(svg_text, folder)
                except Exception as error:
                    print(error)
                    self.status.set(str(error))

            reset()
            os.startfile(folder)
            os.chdir(current)

        def reset():
            self.img_srcs[0].clear()
            self.img_srcs[1].clear()
            self.value.set("https://")
            self.status.set("Input a url and click Get Images")
            self.downloader.state(
                ["disabled"]
            )
            self.getter.state(["!disabled"])
            self.reseter.state(["disabled"])

        self.getter["command"] = search
        self.downloader["command"] = download
        self.reseter["command"] = reset
        self.exiter["command"] = self.app.app.destroy

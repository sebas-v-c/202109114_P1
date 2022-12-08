#!/usr/bin/env python3

from tkinter import *
from tkinter import ttk
import InitialWindow


class App(Tk):
    def __init__(self) -> None:
        Tk.__init__(self)
        self._frame = None
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.title("Proyecto 1 LFP")

    def switch_frame(self, frame_class):
        new_frame = frame_class
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)


if __name__ == "__main__":
    app = App()
    controller = InitialWindow.Controller(app)
    app.mainloop()

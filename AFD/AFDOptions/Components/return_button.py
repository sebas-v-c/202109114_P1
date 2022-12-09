#!/usr/bin/env python3

from tkinter import *
from tkinter import ttk

import AFD


class ReturnButton(ttk.Button):
    def __init__(self, parent, row, column, app):
        super().__init__(parent, text="Regresar", command=self.return_to_afd_window)
        self.grid(row=row, column=column)
        self.app = app

    def return_to_afd_window(self):
        controller = AFD.Controller(self.app)

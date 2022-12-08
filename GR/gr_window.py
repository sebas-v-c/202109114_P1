#!/usr/bin/env python3

import controller
import view

from tkinter import *
from tkinter import ttk


class View(view.View):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        title_label = ttk.Label(self, text="Módulo GR", font=("Arial Bold", 20))
        title_label.grid(row=1, column=2)

        self.add_padding()


class Controller(controller.Controller):
    def __init__(self, app) -> None:
        super().__init__(app, View)

#!/usr/bin/env python3

from tkinter import *
from tkinter import ttk

import controller
import view


class View(view.View):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        parent.title("Crear AFD")

        title_label = ttk.Label(self, text="Módulo AFD", font=("Arial Bold", 20))
        title_label.grid(row=1, column=2)

        self.add_padding()


class Controller(controller.Controller):
    def __init__(self, app) -> None:
        super().__init__(app, View)

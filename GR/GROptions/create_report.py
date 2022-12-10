#!/usr/bin/env python3

from tkinter import *
from tkinter import ttk

import controller
import view

import GR


class View(view.View):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        parent.title("Módulo GR")

        title_label = ttk.Label(self, text="Generar Reporte", font=("Arial Bold", 15))
        title_label.grid(row=1, column=2)

        return_button = ttk.Button(
            self,
            text="Regresar",
            command=self.return_button_pressed,
        ).grid(column=2, row=7)

        self.add_padding()

    def return_button_pressed(self):
        if self.controller:
            self.controller.return_button()


class Controller(controller.Controller):
    def __init__(self, app) -> None:
        super().__init__(app, View)

    def return_button(self):
        controller = GR.Controller(self._app)

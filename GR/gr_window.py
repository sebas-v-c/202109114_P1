#!/usr/bin/env python3

import controller
import view

from tkinter import *
from tkinter import ttk

from GR.GROptions import create_gr, create_report, evaluate_string, help_info

import InitialWindow


class View(view.View):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        parent.title("Módulo GR")

        title_label = ttk.Label(self, text="Módulo GR", font=("Arial Bold", 20))
        title_label.grid(row=1, column=2)

        # buttons
        create_afd_button = ttk.Button(
            self, text="Crear GR", command=self.create_afd_button_pressed
        ).grid(column=2, row=4, sticky="WE")

        evaluate_string_button = ttk.Button(
            self, text="Evaluar Cadena", command=self.evaluate_string_button_pressed
        ).grid(column=2, row=5, sticky="WE")

        create_report_button = ttk.Button(
            self,
            text="Generar Reporte GR",
            command=self.create_report_button_pressed,
        ).grid(column=2, row=6, sticky="WE")

        help_button = ttk.Button(
            self,
            text="¡Ayudita!",
            command=self.help_button_pressed,
        ).grid(column=2, row=7, sticky="WE")

        return_button = ttk.Button(
            self,
            text="Regresar",
            command=self.return_button_pressed,
        ).grid(column=2, row=8)

        self.add_padding()

    # Buttons listeners
    def create_afd_button_pressed(self):
        if self.controller:
            self.controller.create_gr()

    def evaluate_string_button_pressed(self):
        if self.controller:
            self.controller.evaluate_string()

    def create_report_button_pressed(self):
        if self.controller:
            self.controller.create_report()

    def help_button_pressed(self):
        if self.controller:
            self.controller.help_button()

    def return_button_pressed(self):
        if self.controller:
            self.controller.return_button()


class Controller(controller.Controller):
    def __init__(self, app) -> None:
        super().__init__(app, View)

    def create_gr(self):
        controller = create_gr.Controller(self._app)

    def evaluate_string(self):
        controller = evaluate_string.Controller(self._app)

    def create_report(self):
        controller = create_report.Controller(self._app)

    def help_button(self):
        controller = help_info.Controller(self._app)

    def return_button(self):
        controller = InitialWindow.Controller(self._app)

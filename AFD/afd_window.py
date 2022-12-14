#!/usr/bin/env python3

from tkinter import *
from tkinter import ttk
from AFD.AFDOptions import create_afd, create_report, evaluate_string, help_info

import controller
import view
import InitialWindow


class View(view.View):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        parent.title("Módulo AFD")

        title_label = ttk.Label(self, text="Módulo AFD", font=("Arial Bold", 20))
        title_label.grid(row=1, column=2)

        # buttons
        create_afd_button = ttk.Button(
            self, text="Crear AFD", command=self.create_afd_button_pressed
        ).grid(column=2, row=4, sticky="ew")

        evaluate_string_button = ttk.Button(
            self, text="Evaluar Cadena", command=self.evaluate_string_button_pressed
        ).grid(column=2, row=5, sticky="ew")

        create_report_button = ttk.Button(
            self,
            text="Generar Reporte AFD",
            command=self.create_report_button_pressed,
        ).grid(column=2, row=6, sticky="ew")

        help_button = ttk.Button(
            self,
            text="¡Ayudita!",
            command=self.help_button_pressed,
        ).grid(column=2, row=7, sticky="ew")

        return_button = ttk.Button(
            self,
            text="Regresar",
            command=self.return_button_pressed,
        ).grid(column=2, row=8, sticky="ew")

        self.add_padding()

    # Buttons listeners
    def create_afd_button_pressed(self):
        if self.controller:
            self.controller.create_afd()

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

    def create_afd(self):
        controller = create_afd.Controller(self._app)

    def evaluate_string(self):
        controller = evaluate_string.Controller(self._app)

    def create_report(self):
        controller = create_report.Controller(self._app)

    def help_button(self):
        controller = help_info.Controller(self._app)

    def return_button(self):
        controller = InitialWindow.Controller(self._app)

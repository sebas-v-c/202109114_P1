#!/usr/bin/env python3

from tkinter import *
from tkinter import ttk

import controller
import view
import AFD
import GR
import LoadFiles


class View(view.View):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        # create widgets

        # Label
        course_label = ttk.Label(self, text="Lenguajes Formales\ny de Programación")
        course_label.grid(row=1, column=0, sticky="W")

        course_section_label = ttk.Label(self, text="Sección: N")
        course_section_label.grid(row=2, column=0, sticky="W")

        student_name_label = ttk.Label(
            self, text="Sebastian Alejandro\nVásquez Cartagena"
        )
        student_name_label.grid(row=1, column=3, sticky="E")

        student_id_label = ttk.Label(self, text="202109114")
        student_id_label.grid(row=2, column=3, sticky="E")

        title_label = ttk.Label(self, text="PROYECTO 1 LFP", font=("Arial Bold", 30))
        title_label.grid(row=4, column=2)

        afd_button = ttk.Button(self, text="AFD", command=self.afd_button_pressed).grid(
            column=2, row=5, sticky="ew"
        )

        gr_button = ttk.Button(self, text="GR", command=self.gr_button_pressed).grid(
            column=2, row=6, sticky="ew"
        )

        load_files_button = ttk.Button(
            self, text="Carga de Archivos", command=self.load_files_button_pressed
        ).grid(column=2, row=7, sticky="ew")

        quit_button = ttk.Button(
            self, text="Salir", command=self.quit_button_pressed
        ).grid(column=2, row=8, sticky="ew")

        for child in self.winfo_children():
            child.grid_configure(padx=7, pady=7)

    def afd_button_pressed(self):
        if self.controller:
            self.controller.afd_module()

    def gr_button_pressed(self):
        if self.controller:
            self.controller.gr_module()

    def load_files_button_pressed(self):
        if self.controller:
            self.controller.load_files_module()

    def quit_button_pressed(self):
        if self.controller:
            self.controller.quit_program()


class Controller(controller.Controller):
    def __init__(self, app) -> None:
        super().__init__(app, View)

    def afd_module(self):
        controller = AFD.Controller(self._app)

    def gr_module(self):
        controller = GR.Controller(self._app)

    def load_files_module(self):
        controller = LoadFiles.Controller(self._app)
        pass

    def quit_program(self):
        self._app.destroy()

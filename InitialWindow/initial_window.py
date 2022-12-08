#!/usr/bin/env python3

from tkinter import *
from tkinter import ttk


class View(ttk.Frame):
    def __init__(self, parent) -> None:
        ttk.Frame.__init__(self, parent, padding="3 3 12 12")

        self.grid(column=0, row=0, sticky="N E W S")

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

        for child in self.winfo_children():
            child.grid_configure(padx=7, pady=7)

        afd_button = ttk.Button(self, text="AFD", command=self.afd_button_pressed).grid(
            column=2, row=5
        )

        gr_button = ttk.Button(self, text="GR", command=self.gr_button_pressed).grid(
            column=2, row=6
        )

        load_files_button = ttk.Button(
            self, text="Carga de Archivos", command=self.load_files_button_pressed
        ).grid(column=2, row=7)

        quit_button = ttk.Button(
            self, text="Salir", command=self.quit_button_pressed
        ).grid(column=2, row=8)
        controller = None

        for child in self.winfo_children():
            child.grid_configure(padx=7, pady=7)

    def set_controller(self, controller):
        self.controller = controller

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


class Controller:
    def __init__(self, app) -> None:
        self._app = app
        self._view = View(app)
        app.switch_frame(self._view)

        self._view.set_controller(self)

    def afd_module(self):
        pass

    def gr_module(self):
        pass

    def load_files_module(self):
        pass

    def quit_program(self):
        self._app.destroy()

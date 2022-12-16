#!/usr/bin/env python3

from tkinter import *
from tkinter import ttk

import os

import controller
import view
import AFD.graphviz as Graphviz

import AFD

DOT_FILE_NAME = ".input.out"
PDF_FILE_NAME = "output.pdf"


class View(ttk.Frame):
    def __init__(self, parent) -> None:
        ttk.Frame.__init__(self, parent, padding="3 3 12 12")

        self.grid(column=0, row=0, sticky="N E W S")

        self.controller = None

        parent.title("Crear Reporte")

        # -----------------------------------Title-------------------------------#
        title_label = ttk.Label(self, text="Generar Reporte", font=("Arial Bold", 15))
        title_label.grid(row=1, column=2)

        # -----------------------------------AFD Combobox-------------------------------#
        self.afd_combobox = StringVar()
        self._afd_combobox = ttk.Combobox(self, textvariable=self.afd_combobox)
        self._afd_combobox.state(["readonly"])
        self._afd_combobox.grid(row=2, column=2, sticky="WE")
        self._afd_combobox.bind("<<ComboboxSelected>>", self.combobox_selected)

        # -----------------------------------create report button-------------------------------#
        self.create_button = ttk.Button(
            self, text="Generar Reporte", command=self.generate_report_button_pressed
        )
        self.create_button.state(["disabled"])
        self.create_button.grid(row=3, column=2, sticky="WE")

        # -----------------------------------return button-------------------------------#
        return_button = ttk.Button(
            self,
            text="Regresar",
            command=self.return_button_pressed,
        ).grid(column=2, row=7)

        self.add_padding()

    def generate_report_button_pressed(self):
        if self.controller:
            self.controller.generate_report()

    def combobox_selected(self, *args):
        self._afd_combobox.selection_clear()
        if self.controller:
            self.controller.combobox_selected()

    def define_combobox_values(self, values: list):
        self._afd_combobox["values"] = values

    def return_button_pressed(self):
        if self.controller:
            self.controller.return_button()

    def set_controller(self, controller):
        self.controller = controller

    def add_padding(self, x_size=7, y_size=7):
        for child in self.winfo_children():
            child.grid_configure(padx=x_size, pady=y_size)


class Controller(controller.Controller):
    def __init__(self, app) -> None:
        self._app = app
        self._view = View(app)
        app.switch_frame(self._view)

        self._view.set_controller(self)

        # get a list of names
        self._view.define_combobox_values(
            list(map(lambda afd: afd.name, app.afd_objects))
        )

    def generate_report(self):
        self._view.afd_combobox.get()
        afd_object: AFD.AFD
        for afd in self._app.afd_objects:
            if afd.name == afd_name:
                afd_object = afd
                break

        if not afd_object:
            return

        diagraph: str = "digraph G {\n" + Graphviz.create_diagraph()
        description: str = Graphviz.create_description() + "\n}"

        if os.path.exists(DOT_FILE_NAME):
            os.remove(DOT_FILE_NAME)

        cwd = os.getcwd()
        with open(DOT_FILE_NAME, mode="w") as f:
            f.write(diagraph + description)

    def combobox_selected(self):
        self._view.afd_combobox.get()

    def return_button(self):
        controller = AFD.Controller(self._app)

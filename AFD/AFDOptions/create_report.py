#!/usr/bin/env python3

from tkinter import *
from tkinter import ttk

import os

import controller
import view
import Graphviz

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

        # -----------------------------------validate label-------------------------------#
        self.generate_report = StringVar()
        self.generate_report.trace_add("write", self.on_write_changed)
        self.generate_report_label = ttk.Label(
            self,
            text="",
            foreground="red",
            font=("Arial Bold", 10),
            textvariable=self.generate_report,
        )
        self.generate_report_label.grid(row=7, column=2)

        # -----------------------------------return button-------------------------------#
        return_button = ttk.Button(
            self,
            text="Regresar",
            command=self.return_button_pressed,
        ).grid(column=2, row=5)

        self.add_padding()

    def generate_report_button_pressed(self):
        if self.controller:
            self.controller.generate_report()

    def combobox_selected(self, *args):
        self._afd_combobox.selection_clear()
        if self.controller:
            self.controller.combobox_selected()

    def on_write_changed(self, *args):
        if self.controller:
            self.controller.on_entry_changed()

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


class Controller:
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
        afd_name = self._view.afd_combobox.get()
        afd_object: AFD.AFD
        for afd in self._app.afd_objects:
            if afd.name == afd_name:
                afd_object = afd
                break

        if not afd_object:
            return

        # generate diagraph and description
        try:
            diagraph: str = "digraph G {\n" + Graphviz.create_diagraph(afd_object)
            description: str = "\n" + Graphviz.create_description(afd_object) + "\n}"
        except:
            self._view.generate_report.set(
                "Ha ocurrido un error al generar el archivo .dot"
            )
            return

        cwd = os.getcwd()

        try:
            os.remove(cwd + "/" + DOT_FILE_NAME)
        except:
            pass

        with open(DOT_FILE_NAME, mode="w") as f:
            f.write(diagraph + description)

        try:
            os.system("dot -Tpdf " + DOT_FILE_NAME + " > " + PDF_FILE_NAME)
        except:
            self._view.generate_report.set(
                "Ha ocurrido un error al generar el archivo pdf"
            )

        try:
            os.system("zathura " + cwd + "/" + PDF_FILE_NAME)
        except:
            self._view.generate_report.set(
                "Ha ocurrido un error al abrir el archivo pdf"
            )
        else:
            self._view.generate_report.set(
                "Ha ocurrido un error al abrir el archivo pdf"
            )

    def combobox_selected(self):
        self._view.create_button.state(["!disabled"])

    def on_entry_changed(self):
        self._view.generate_report.set("")

    def return_button(self):
        controller = AFD.Controller(self._app)

#!/usr/bin/env python3


from tkinter import *
from tkinter import ttk
from AFD.afd import InvalidStringException
import Graphviz

import controller
import view

import AFD
import os

DOT_FILE_NAME = ".input_route.out"
PDF_FILE_NAME = "output_route.pdf"


class View(ttk.Frame):
    def __init__(self, parent) -> None:
        ttk.Frame.__init__(self, parent, padding="3 3 12 12")

        self.grid(column=0, row=0, sticky="N E W S")

        self.controller = None

        parent.title("Módulo AFD")

        # -----------------------------------Title-------------------------------#
        title_label = ttk.Label(self, text="Evaluar Cadena", font=("Arial Bold", 15))
        title_label.grid(row=1, column=2)

        # -----------------------------------AFD Label-------------------------------#
        afd_label = ttk.Label(self, text="AFD: ")
        afd_label.grid(row=2, column=1, sticky="E")

        # -----------------------------------AFD Combobox-------------------------------#
        self.afd_combobox = StringVar()
        self._afd_combobox = ttk.Combobox(self, textvariable=self.afd_combobox)
        self._afd_combobox.state(["readonly"])
        self._afd_combobox.grid(row=2, column=2, sticky="WE")
        self._afd_combobox.bind("<<ComboboxSelected>>", self.combobox_selected)

        # -----------------------------------String-------------------------------#
        self.afd_string = StringVar()
        self.afd_string_entry = ttk.Entry(self, textvariable=self.afd_string, width=30)
        self.afd_string_entry.grid(row=3, column=2)
        self.afd_string_entry.state(["disabled"])

        # -----------------------------------validate button-------------------------------#
        self.validate_only_button = ttk.Button(
            self, text="Solo Validar", command=self.validate_only_button_pressed
        )
        self.validate_only_button.grid(row=4, column=1)
        self.validate_only_button.state(["disabled"])

        # -----------------------------------validate label-------------------------------#
        self.validate_afd = StringVar()
        self.validate_afd.trace_add("write", self.on_write_changed)
        self.validate_afd_label = ttk.Label(
            self,
            text="",
            foreground="red",
            font=("Arial Bold", 10),
            textvariable=self.validate_afd,
        )
        self.validate_afd_label.grid(row=7, column=1, columnspan=3)

        # -----------------------------------label for graphviz-------------------------------#
        self.generate_graphviz = StringVar()
        self.generate_graphviz.trace_add("write", self.on_write_changed)
        self.generate_graphviz_label = ttk.Label(
            self,
            text="",
            foreground="red",
            font=("Arial Bold", 10),
            textvariable=self.generate_graphviz,
        )
        self.generate_graphviz_label.grid(row=7, column=2)

        # -----------------------------------full route button-------------------------------#
        self.full_route_button = ttk.Button(
            self, text="Ruta", command=self.full_route_button_pressed
        )
        self.full_route_button.state(["disabled"])
        self.full_route_button.grid(row=4, column=3)
        # -----------------------------------return button-------------------------------#
        return_button = ttk.Button(
            self,
            text="Regresar",
            command=self.return_button_pressed,
        ).grid(column=3, row=7)

        self.add_padding()

    def define_combobox_values(self, values: list):
        self._afd_combobox["values"] = values

    def on_write_changed(self, *args):
        if self.controller:
            self.controller.on_entry_changed()

    def combobox_selected(self, *args):
        self._afd_combobox.selection_clear()
        if self.controller:
            self.controller.combobox_selected()

    def full_route_button_pressed(self):
        if self.controller:
            self.controller.validate_route()

    def validate_only_button_pressed(self):
        if self.controller:
            self.controller.validate_only()

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

    def validate_route(self):
        afd_name = self._view.afd_combobox.get()
        afd_object: AFD.AFD
        for afd in self._app.afd_objects:
            if afd.name == afd_name:
                afd_object = afd
                break

        if not afd_object:
            return

        string = self._view.afd_string.get()

        try:
            steps = afd_object.evaluate_string(string)
        except InvalidStringException:
            self._view.validate_afd_label.config(foreground="red")
            self._view.validate_afd.set("La Cadena Introducida No Es Válida")
        else:
            self._generate_route(steps, string)
            self._view.validate_afd_label.config(foreground="green")
            self._view.validate_afd.set("La Cadena Introducida Sí Es Válida")
            self.return_button()

    def _generate_route(self, steps: list, string: str):
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
            diagraph: str = "digraph G {\n" + Graphviz.create_route_diagraph(
                afd_object, steps
            )
            description: str = (
                "\n"
                + Graphviz.create_route_description(afd_object, steps, string)
                + "\n}"
            )
        except:
            self._view.generate_graphviz.set(
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
            self._view.generate_graphviz.set(
                "Ha ocurrido un error al generar el archivo pdf"
            )

        try:
            os.system("zathura " + cwd + "/" + PDF_FILE_NAME)
        except:
            self._view.generate_graphviz.set(
                "Ha ocurrido un error al abrir el archivo pdf"
            )
        else:
            self._view.generate_graphviz.set(
                "Ha ocurrido un error al abrir el archivo pdf"
            )

    def validate_only(self):
        afd_name = self._view.afd_combobox.get()
        afd_object: AFD.AFD
        for afd in self._app.afd_objects:
            if afd.name == afd_name:
                afd_object = afd
                break

        if not afd_object:
            return

        string = self._view.afd_string.get()

        try:
            steps = afd_object.evaluate_string(string)
        except InvalidStringException:
            self._view.validate_afd_label.config(foreground="red")
            self._view.validate_afd.set("La Cadena Introducida No Es Válida")
        else:
            self._view.validate_afd_label.config(foreground="green")
            self._view.validate_afd.set("La Cadena Introducida Sí Es Válida")

    def combobox_selected(self):
        self._view.validate_afd.set("")
        self._view.afd_string_entry.state(["!disabled"])
        self._view.validate_only_button.state(["!disabled"])
        self._view.full_route_button.state(["!disabled"])

    def on_entry_changed(self):
        self._view.validate_afd.set("")

    def return_button(self):
        controller = AFD.Controller(self._app)

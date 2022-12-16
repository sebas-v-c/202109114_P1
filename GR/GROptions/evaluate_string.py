from tkinter import *
from tkinter import ttk
from GR.gr import InvalidStringException
import Graphviz

import GR
import os

DOT_FILE_NAME = ".input_route.out"
PDF_FILE_NAME = "output_route.pdf"


class View(ttk.Frame):
    def __init__(self, parent) -> None:
        ttk.Frame.__init__(self, parent, padding="3 3 12 12")

        self.grid(column=0, row=0, sticky="N E W S")

        self.controller = None

        parent.title("Módulo GR")

        # -----------------------------------Title-------------------------------#
        title_label = ttk.Label(self, text="Evaluar Cadena", font=("Arial Bold", 15))
        title_label.grid(row=1, column=2)

        # -----------------------------------GR Label-------------------------------#
        gr_label = ttk.Label(self, text="GR: ")
        gr_label.grid(row=2, column=1, sticky="E")

        # -----------------------------------GR Combobox-------------------------------#
        self.gr_combobox = StringVar()
        self._gr_combobox = ttk.Combobox(self, textvariable=self.gr_combobox)
        self._gr_combobox.state(["readonly"])
        self._gr_combobox.grid(row=2, column=2, sticky="WE")
        self._gr_combobox.bind("<<ComboboxSelected>>", self.combobox_selected)

        # -----------------------------------String-------------------------------#
        self.gr_string = StringVar()
        self.gr_string_entry = ttk.Entry(self, textvariable=self.gr_string, width=30)
        self.gr_string_entry.grid(row=3, column=2)
        self.gr_string_entry.state(["disabled"])

        # -----------------------------------validate button-------------------------------#
        self.validate_only_button = ttk.Button(
            self, text="Solo Validar", command=self.validate_only_button_pressed
        )
        self.validate_only_button.grid(row=4, column=1)
        self.validate_only_button.state(["disabled"])

        # -----------------------------------validate label-------------------------------#
        self.validate_gr = StringVar()
        self.validate_gr.trace_add("write", self.on_write_changed)
        self.validate_gr_label = ttk.Label(
            self,
            text="",
            foreground="red",
            font=("Arial Bold", 10),
            textvariable=self.validate_gr,
        )
        self.validate_gr_label.grid(row=7, column=1, columnspan=3)

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
        self._gr_combobox["values"] = values

    def on_write_changed(self, *args):
        if self.controller:
            self.controller.on_entry_changed()

    def combobox_selected(self, *args):
        self._gr_combobox.selection_clear()
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
        self._view.define_combobox_values(list(map(lambda gr: gr.name, app.gr_objects)))

    def validate_route(self):
        gr_name = self._view.gr_combobox.get()
        gr_object: GR.GR
        for gr in self._app.gr_objects:
            if gr.name == gr_name:
                gr_object = gr
                break

        if not gr_object:
            return

        string = self._view.gr_string.get()

        try:
            steps = gr_object.evaluate_string(string)
        except InvalidStringException:
            self._view.validate_gr_label.config(foreground="red")
            self._view.validate_gr.set("La Cadena Introducida No Es Válida")
        else:
            self._generate_route(steps, string)
            self._view.validate_gr_label.config(foreground="green")
            self._view.validate_gr.set("La Cadena Introducida Sí Es Válida")
            self.return_button()

    def _generate_route(self, steps: list, string: str):
        gr_name = self._view.gr_combobox.get()
        gr_object: GR.GR
        for gr in self._app.gr_objects:
            if gr.name == gr_name:
                gr_object = gr
                break

        if not gr_object:
            return

        # generate diagraph and description
        try:
            diagraph: str = "digraph G {\n" + Graphviz.create_route_diagraph(
                gr_object, steps
            )
            description: str = (
                "\n"
                + Graphviz.create_route_description(gr_object, steps, string)
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
        gr_name = self._view.gr_combobox.get()
        gr_object: GR.GR
        for gr in self._app.gr_objects:
            if gr.name == gr_name:
                gr_object = gr
                break

        if not gr_object:
            return

        string = self._view.gr_string.get()

        try:
            steps = gr_object.evaluate_string(string)
        except InvalidStringException:
            self._view.validate_gr_label.config(foreground="red")
            self._view.validate_gr.set("La Cadena Introducida No Es Válida")
        else:
            self._view.validate_gr_label.config(foreground="green")
            self._view.validate_gr.set("La Cadena Introducida Sí Es Válida")

    def combobox_selected(self):
        self._view.validate_gr.set("")
        self._view.gr_string_entry.state(["!disabled"])
        self._view.validate_only_button.state(["!disabled"])
        self._view.full_route_button.state(["!disabled"])

    def on_entry_changed(self):
        self._view.validate_gr.set("")

    def return_button(self):
        controller = GR.Controller(self._app)

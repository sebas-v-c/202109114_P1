#!/usr/bin/env python3

from tkinter import *
from tkinter import ttk

import GR


class View(ttk.Frame):
    def __init__(self, parent, gr_example) -> None:
        ttk.Frame.__init__(self, parent, padding="3 3 12 12")

        self.grid(column=0, row=0, sticky="N E W S")

        self.controller = None

        parent.title("Crear Reporte")

        # -----------------------------------Title-------------------------------#
        title_label = ttk.Label(self, text="Ayuda", font=("Arial Bold", 15))
        title_label.grid(row=1, column=2)

        # -----------------------------------Information-------------------------------#
        # TODO descripcion gr
        info_label = ttk.Label(self, text="Descripcion chida")
        info_label.grid(row=2, column=1, columnspan=2)

        # -----------------------------------Image-------------------------------#

        canvas = Canvas(
            self,
            width=519,
            height=336,
        )
        canvas.grid(row=3, column=2)
        imgobj = PhotoImage(file="./Res/gr_help.png")
        self.imgObj = imgobj
        canvas.create_image(20, 20, anchor="nw", image=imgobj)

        # -----------------------------------return button-------------------------------#
        return_button = ttk.Button(
            self,
            text="Regresar",
            command=self.return_button_pressed,
        ).grid(column=2, row=5)

        self.add_padding()

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
        self._view = View(app, self._app.GR_EXAMPLE_IMAGE)
        app.switch_frame(self._view)

        self._view.set_controller(self)

    def return_button(self):
        controller = GR.Controller(self._app)

#!/usr/bin/env python3
from tkinter import *
from tkinter import ttk
from GR import gr_window

from GR.gr import *


class View(ttk.Frame):
    def __init__(self, parent) -> None:
        ttk.Frame.__init__(self, parent, padding="3 3 12 12")

        self.grid(column=0, row=0, sticky="N E W S")

        self.controller = None
        parent.title("Crear GR")

        # title
        title_label = ttk.Label(self, text="Crear GR", font=("Arial Bold", 15))
        title_label.grid(row=0, column=3)

        # Name entries
        gr_name_label = ttk.Label(self, text="Nombre: ")
        gr_name_label.grid(row=2, column=1, sticky="e")

        self.gr_name = StringVar()
        gr_name = ttk.Entry(self, textvariable=self.gr_name)
        gr_name.grid(row=2, column=3)

        self.gr_name_error = StringVar()
        gr_name_error = ttk.Label(
            self, text="", textvariable=self.gr_name_error, foreground="red"
        )
        gr_name_error.grid(row=2, column=4)

        # no terminals entries
        gr_no_terminals_label = ttk.Label(self, text="No Terminales: ")
        gr_no_terminals_label.grid(row=3, column=1, sticky="e")

        self.gr_no_terminals = StringVar()
        gr_no_terminals = ttk.Entry(self, textvariable=self.gr_no_terminals, width=20)
        gr_no_terminals.grid(row=3, column=3)

        self.gr_no_terminals_error = StringVar()
        gr_no_terminals_error = ttk.Label(
            self, text="", textvariable=self.gr_no_terminals_error, foreground="red"
        )
        gr_no_terminals_error.grid(row=3, column=4)

        # terminals entries
        gr_terminals_label = ttk.Label(self, text="Terminales: ")
        gr_terminals_label.grid(row=4, column=1, sticky="e")

        self.gr_terminals = StringVar()
        gr_terminals = ttk.Entry(self, textvariable=self.gr_terminals, width=20)
        gr_terminals.grid(row=4, column=3)

        self.gr_terminals_error = StringVar()
        gr_terminals_error = ttk.Label(
            self, text="", textvariable=self.gr_terminals_error, foreground="red"
        )
        gr_terminals_error.grid(row=4, column=4)

        # initial no terminal entry
        gr_initia_no_terminal_label = ttk.Label(self, text="No Terminal Inicial: ")
        gr_initia_no_terminal_label.grid(row=5, column=1, sticky="e")

        self.gr_initia_no_terminal = StringVar()
        gr_initia_no_terminal = ttk.Entry(
            self, textvariable=self.gr_initia_no_terminal, width=5
        )
        gr_initia_no_terminal.grid(row=5, column=3)

        self.gr_initia_no_terminal_error = StringVar()
        gr_initia_no_terminal_error = ttk.Label(
            self,
            text="",
            textvariable=self.gr_initia_no_terminal_error,
            foreground="red",
        )
        gr_initia_no_terminal_error.grid(row=5, column=4)

        #  productions entries
        gr_productions_label = ttk.Label(self, text="Transiciones: ")
        gr_productions_label.grid(row=7, column=1, sticky="NE")

        self.gr_productions = StringVar()
        gr_productions = ttk.Entry(self, textvariable=self.gr_productions, width=50)
        gr_productions.grid(row=7, column=3, columnspan=2)
        self.gr_productions.set("Ejemplo: A > 0; B > 1; B > $ ...")

        self.gr_productions_error = StringVar()
        gr_productions_error = ttk.Label(
            self, text="", textvariable=self.gr_productions_error, foreground="red"
        )
        gr_productions_error.grid(row=8, column=3, sticky="N")

        # succes label
        self.gr_success = StringVar()
        gr_success = ttk.Label(
            self, text="", textvariable=self.gr_success, foreground="green"
        )
        gr_success.grid(row=9, column=1, columnspan=2)

        # create button
        create_button = ttk.Button(
            self, text="Crear GR", command=self.create_gr_button_pressed
        ).grid(column=0, row=9, sticky="SW")

        # return button
        return_button = ttk.Button(
            self,
            text="Regresar",
            command=self.return_button_pressed,
        ).grid(column=4, row=9, sticky="SW")

        self.add_padding()

    def return_button_pressed(self):
        if self.controller:
            self.controller.return_button()

    def create_gr_button_pressed(self):
        if self.controller:
            self.controller.create_gr_button()

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

    def return_button(self):
        controller = gr_window.Controller(self._app)

    def reset_error_labels(self):
        self._view.gr_name_error.set("")
        self._view.gr_terminals_error.set("")
        self._view.gr_no_terminals_error.set("")
        self._view.gr_initia_no_terminal_error.set("")
        self._view.gr_productions_error.set("")
        self._view.gr_success.set("")

    def create_gr_button(self):
        self.reset_error_labels()
        try:
            new_gr = GR(self._view.gr_name.get())
            if new_gr.name in list(map(lambda x: x.name, self._app.gr_objects)):
                raise NameExistException("Name already exist in the gr_objecst")
            new_gr.no_terminals = self._view.gr_no_terminals.get()
            new_gr.terminals = self._view.gr_terminals.get()
            new_gr.initial_no_terminal = self._view.gr_initia_no_terminal.get()
            new_gr.productions = self._view.gr_productions.get()
        except NameException:
            self._view.gr_name_error.set("El nombre es invalido")
        except NameExistException:
            self._view.gr_name_error.set("El nombre ya existe en el sistema")
        except NoTerminalsException:
            self._view.gr_no_terminals_error.set(
                "Los No Terminales estań vacios\nO hay duplicados"
            )
        except TerminalsException:
            self._view.gr_terminals_error.set(
                "Hay duplicados o elementos\nson parte de los estados"
            )
        except InitialStateException:
            self._view.gr_initia_no_terminal_error.set(
                "El estado inicial no forma\nparte de los estados"
            )
        except ProductionsSyntaxException:
            self._view.gr_productions_error.set(
                "La sintaxis de la producción no es correcta"
            )
        else:
            self._app.gr_objects.append(new_gr)
            self._view.gr_success.set("GR creado con éxito")


class NameExistException(Exception):
    pass

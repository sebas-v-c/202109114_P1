#!/usr/bin/env python3

from tkinter import *
from tkinter import ttk
from AFD import AFDOptions
from AFD.afd import NameException

import controller
import view

from AFD.afd import *


class View(ttk.Frame):
    def __init__(self, parent) -> None:
        ttk.Frame.__init__(self, parent, padding="3 3 12 12")

        self.grid(column=0, row=0, sticky="N E W S")

        self.controller = None
        parent.title("Crear AFD")

        # title
        title_label = ttk.Label(self, text="Crear AFD", font=("Arial Bold", 15))
        title_label.grid(row=0, column=3)

        # Name entries
        afd_name_label = ttk.Label(self, text="Nombre: ")
        afd_name_label.grid(row=2, column=1, sticky="e")

        self.afd_name = StringVar()
        afd_name = ttk.Entry(self, textvariable=self.afd_name)
        afd_name.grid(row=2, column=3)

        self.afd_name_error = StringVar()
        afd_name_error = ttk.Label(
            self, text="", textvariable=self.afd_name_error, foreground="red"
        )
        afd_name_error.grid(row=2, column=4)

        # states entries
        afd_states_label = ttk.Label(self, text="Estados: ")
        afd_states_label.grid(row=3, column=1, sticky="e")

        self.afd_states = StringVar()
        afd_states = ttk.Entry(self, textvariable=self.afd_states, width=20)
        afd_states.grid(row=3, column=3)

        self.afd_states_error = StringVar()
        afd_states_error = ttk.Label(
            self, text="", textvariable=self.afd_states_error, foreground="red"
        )
        afd_states_error.grid(row=3, column=4)

        # alfabet entries
        afd_alfabet_label = ttk.Label(self, text="Alfabeto: ")
        afd_alfabet_label.grid(row=4, column=1, sticky="e")

        self.afd_alfabet = StringVar()
        afd_alfabet = ttk.Entry(self, textvariable=self.afd_alfabet, width=20)
        afd_alfabet.grid(row=4, column=3)

        self.afd_alfabet_error = StringVar()
        afd_alfabet_error = ttk.Label(
            self, text="", textvariable=self.afd_alfabet_error, foreground="red"
        )
        afd_alfabet_error.grid(row=4, column=4)

        # initial state entries
        afd_initial_state_label = ttk.Label(self, text="Estado Inicial: ")
        afd_initial_state_label.grid(row=5, column=1, sticky="e")

        self.afd_initial_state = StringVar()
        afd_initial_state = ttk.Entry(
            self, textvariable=self.afd_initial_state, width=5
        )
        afd_initial_state.grid(row=5, column=3)

        self.afd_initial_state_error = StringVar()
        afd_initial_state_error = ttk.Label(
            self, text="", textvariable=self.afd_initial_state_error, foreground="red"
        )
        afd_initial_state_error.grid(row=5, column=4)

        # initial state entries
        afd_acceptance_states_label = ttk.Label(self, text="Estado de Aceptación: ")
        afd_acceptance_states_label.grid(row=6, column=1, sticky="e")

        self.afd_acceptance_states = StringVar()
        afd_acceptance_states = ttk.Entry(
            self, textvariable=self.afd_acceptance_states, width=20
        )
        afd_acceptance_states.grid(row=6, column=3)

        self.afd_acceptance_states_error = StringVar()
        afd_acceptance_states_error = ttk.Label(
            self,
            text="",
            textvariable=self.afd_acceptance_states_error,
            foreground="red",
        )
        afd_acceptance_states_error.grid(row=6, column=4)

        #  transitions entries
        afd_transitions_label = ttk.Label(self, text="Transiciones: ")
        afd_transitions_label.grid(row=7, column=1, sticky="NE")

        self.afd_transitions = Text(self, width=20, height=10)
        self.afd_transitions.insert("1.0", "Ejemplo:\n\nA,1;B\nA,2;B\nB,1;C\n...")
        self.afd_transitions.grid(row=7, column=3)

        self.afd_transitions_error = StringVar()
        afd_transitions_error = ttk.Label(
            self, text="", textvariable=self.afd_transitions_error, foreground="red"
        )
        afd_transitions_error.grid(row=7, column=4, sticky="N")

        # succes label
        self.afd_success = StringVar()
        afd_success = ttk.Label(
            self, text="", textvariable=self.afd_success, foreground="green"
        )
        afd_success.grid(row=8, column=1, columnspan=2)

        # create button
        create_button = ttk.Button(
            self, text="Crear AFD", command=self.create_afd_button_pressed
        ).grid(column=0, row=8, sticky="SW")

        # return button
        return_button = ttk.Button(
            self,
            text="Regresar",
            command=self.return_button_pressed,
        ).grid(column=4, row=8, sticky="SW")

        self.add_padding()

    def return_button_pressed(self):
        if self.controller:
            self.controller.return_button()

    def create_afd_button_pressed(self):
        if self.controller:
            self.controller.create_afd_button()

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
        controller = Controller(self._app)

    def reset_error_labels(self):
        self._view.afd_name_error.set("")
        self._view.afd_states_error.set("")
        self._view.afd_alfabet_error.set("")
        self._view.afd_initial_state_error.set("")
        self._view.afd_acceptance_states_error.set("")
        self._view.afd_transitions_error.set("")

    def create_afd_button(self):
        self.reset_error_labels()
        try:
            new_afd = AFD(self._view.afd_name.get())
            new_afd.states = self._view.afd_states.get()
            new_afd.alfabet = self._view.afd_alfabet.get()
            new_afd.initial_state = self._view.afd_initial_state.get()
            new_afd.acceptance_states = self._view.afd_acceptance_states.get()
            new_afd.transitions = self._view.afd_transitions.get("1.0", END)
        except NameException:
            self._view.afd_name_error.set("El nombre es invalido")
        except StatesException:
            self._view.afd_states_error.set("Los estados estań vacios")
        except AlfabetException:
            self._view.afd_alfabet_error.set(
                "Hay duplicados o elementos\nson parte de los estados"
            )
        except InitialStateException:
            self._view.afd_initial_state_error.set(
                "El estado inicial no forma\nparte de los estados"
            )
        except AcceptanceStatesException:
            self._view.afd_acceptance_states_error.set(
                "El estado de aceptación no forma\nparte de los estados"
            )
        except TransitionsSyntaxException:
            self._view.afd_transitions_error.set(
                "La sintaxis de la transicion no es correcta"
            )
        else:
            self._app.afd_objects.append(new_afd)
            self._view.afd_success.set("AFD creado con éxito")

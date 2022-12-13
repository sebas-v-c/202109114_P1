#!/usr/bin/env python3

from tkinter import *
from tkinter import ttk

import controller
import view

import AFD


class View(view.View):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        parent.title("Crear AFD")

        # title
        title_label = ttk.Label(self, text="Crear AFD", font=("Arial Bold", 15))
        title_label.grid(row=0, column=3)

        # Name entries
        afd_name_label = ttk.Label(self, text="Nombre: ")
        afd_name_label.grid(row=2, column=1)

        self.afd_name = StringVar()
        afd_name = ttk.Entry(self, textvariable=self.afd_name, width=20)
        afd_name.grid(row=2, column=3)

        # states entries
        afd_states_label = ttk.Label(self, text="Estados: ")
        afd_states_label.grid(row=3, column=1)

        self.afd_states = StringVar()
        afd_states = ttk.Entry(self, textvariable=self.afd_states, width=20)
        afd_states.grid(row=3, column=3)

        # alfabet entries
        afd_alfabet_label = ttk.Label(self, text="Alfabeto: ")
        afd_alfabet_label.grid(row=4, column=1)

        self.afd_alfabet = StringVar()
        afd_alfabet = ttk.Entry(self, textvariable=self.afd_alfabet, width=20)
        afd_alfabet.grid(row=4, column=3)

        # initial state entries
        afd_initial_state_label = ttk.Label(self, text="Estado Inicial: ")
        afd_initial_state_label.grid(row=5, column=1)

        self.afd_initial_state = StringVar()
        afd_initial_state = ttk.Entry(
            self, textvariable=self.afd_initial_state, width=5
        )
        afd_initial_state.grid(row=5, column=3)

        # initial state entries
        afd_acceptance_states_label = ttk.Label(self, text="Estado de Aceptación: ")
        afd_acceptance_states_label.grid(row=6, column=1)

        self.afd_acceptance_states = StringVar()
        afd_acceptance_states = ttk.Entry(
            self, textvariable=self.afd_acceptance_states, width=20
        )
        afd_acceptance_states.grid(row=6, column=3)

        #  transitions entries
        afd_transitions_label = ttk.Label(self, text="Transiciones: ")
        afd_transitions_label.grid(row=7, column=1)

        self.afd_transitions = Text(self, width=20, height=10)
        self.afd_transitions.grid(row=7, column=3, sticky="N")

        return_button = ttk.Button(
            self,
            text="Regresar",
            command=self.return_button_pressed,
        ).grid(column=10, row=7, sticky="S W")

        self.add_padding()

    def return_button_pressed(self):
        if self.controller:
            self.controller.return_button()


class Controller(controller.Controller):
    def __init__(self, app) -> None:
        super().__init__(app, View)

    def return_button(self):
        controller = AFD.Controller(self._app)

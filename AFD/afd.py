#!/usr/bin/env python3

separator = ";"

# TODO create exceptions for this code


class AFD:
    def __init__(self, name: str) -> None:
        self.name = name
        self._states: list[str] = []
        self._alfabet = None
        self._initial_state = None
        self._acceptance_states = None
        self._transitions = None
        if name == "":
            raise NameException("Name is empty")

    @property
    def states(self):
        return self._states

    @states.setter
    def states(self, value: str):
        new_states: list[str] = value.split(separator)
        if len(new_states) == 0 or value == "":
            raise StatesException("The states property is Empty")
        self._states: list[str] = new_states

    @property
    def alfabet(self):
        return self._alfabet

    @alfabet.setter
    def alfabet(self, value: str):
        if len(self._states) == 0:
            raise AlfabetException("states property is empty")

        new_alfabet = value.split(separator)
        # if there are duplicate items in the alfabet we raise an error
        if len(new_alfabet) != len(set(new_alfabet)):
            raise AlfabetException("Duplicate items in alfabet list")

        for item in new_alfabet:
            if item in self._states:
                raise AlfabetException("Item of alfabet is in states list property")

        self._alfabet = new_alfabet

    @property
    def initial_state(self):
        return self._initial_state

    @initial_state.setter
    def initial_state(self, value: str):
        new_initial_state = value
        if new_initial_state not in self._states:
            raise InitialStateException(
                "Initial state item is not declared in states property"
            )
        self._initial_state = new_initial_state

    @property
    def acceptance_states(self):
        return self._acceptance_states

    @acceptance_states.setter
    def acceptance_states(self, value: str):
        new_acceptance_states = value.split(separator)
        for item in new_acceptance_states:
            if item not in self._states:
                raise AcceptanceStatesException(
                    "Acceptance state item is not declared in states property"
                )
        self._initial_state = new_acceptance_states

    @property
    def transitions(self):
        return self._transitions

    @transitions.setter
    def transitions(self, value: str):
        new_transitions = value.split("\n")
        new_transitions = filter(lambda x: not x == "", new_transitions)
        new_transitions_list = []
        try:
            for transition in new_transitions:
                # split transition
                splited_transition = transition.split(",")
                temp = splited_transition.pop(1)
                temp = temp.split(";")
                splited_transition = splited_transition + temp

                new_transitions_list.append(
                    Transition(
                        splited_transition[0],
                        splited_transition[1],
                        splited_transition[2],
                    )
                )
        except:
            raise TransitionsSyntaxException(
                "Transition syntax is not formatted correctly"
            )

        # TODO verify if this thing really is an afd
        self._transitions = new_transitions_list

    def __str__(self):
        return f"Name: {self.name}\nStates: {self._states}\nAlfabet: {self._alfabet}\nInitial State: {self._initial_state}\nAcceptance States: {self._acceptance_states}"


class Transition:
    def __init__(self, origin, entry, destination) -> None:
        self.origin = origin
        self.entry = entry
        self.destination = destination

    def __str__(self) -> str:
        return f"({self.origin}, {self.entry}; {self.destination})"


# Exception classes for error handling


class NameException(Exception):
    pass


class StatesException(Exception):
    pass


class AlfabetException(Exception):
    pass


class InitialStateException(Exception):
    pass


class AcceptanceStatesException(Exception):
    pass


class TransitionsSyntaxException(Exception):
    pass


class TransitionException(Exception):
    pass

separator = ";"

MINIMUM_STRING_LENGHT = 1


class Transition:
    def __init__(self, origin, entry, destination) -> None:
        self.origin = origin
        self.entry = entry
        self.destination = destination

    def __str__(self) -> str:
        return f"({self.origin}, {self.entry}; {self.destination})"


class GR:
    def __init__(self, name: str) -> None:
        self.name = name
        self._no_terminals: list[str] = []
        self._terminals: list[str] = []
        self._initial_no_terminal: str = ""
        self._acceptance_no_terminals: list[str] = []
        self._transitions: list[Transition]
        if name == "":
            raise NameException("Name is empty")

    @property
    def no_terminals(self):
        return self._no_terminals

    @no_terminals.setter
    def no_terminals(self, value: str):
        new_no_terminals: list[str] = value.split(separator)
        if len(new_no_terminals) == 0 or value == "":
            raise NoTerminalsException("The no terminals property is Empty")

        # there are duplicates
        if not len(new_no_terminals) == len(set(new_no_terminals)):
            raise NoTerminalsException("There is duplicates")

        self._no_terminals: list[str] = new_no_terminals

    @property
    def terminals(self):
        return self._terminals

    @terminals.setter
    def terminals(self, value: str):
        if len(self._no_terminals) == 0:
            raise TerminalsException("no_terminals property is empty")

        new_terminals = value.split(separator)
        # if there are duplicate items in the terminals we raise an error
        if len(new_terminals) != len(set(new_terminals)):
            raise TerminalsException("Duplicate items in terminals list")

        for item in new_terminals:
            if item in self._no_terminals:
                raise TerminalsException(
                    "Item of terminals is in no_terminals list property"
                )

        self._terminals = new_terminals

    @property
    def initial_no_terminal(self):
        return self._initial_no_terminal

    @initial_no_terminal.setter
    def initial_no_terminal(self, value: str):
        new_initial_no_terminal = value
        if new_initial_no_terminal not in self._no_terminals:
            raise InitialStateException(
                "Initial state item is not declared in no_terminals property"
            )
        self._initial_no_terminal = new_initial_no_terminal

    @property
    def acceptance_no_terminals(self):
        return self._acceptance_no_terminals

    @acceptance_no_terminals.setter
    def acceptance_no_terminals(self, value: str):
        new_acceptance_no_terminals = value.split(separator)
        for item in new_acceptance_no_terminals:
            if item not in self._no_terminals:
                raise AcceptanceNoTerminalsException(
                    "Acceptance state item is not declared in no_terminals property"
                )
        self._acceptance_no_terminals = new_acceptance_no_terminals

    @property
    def productions(self):
        return self._transitions

    @productions.setter
    def productions(self, value: str):
        new_transitions = value.split(";")
        # remove extra empty spaces
        new_transitions = list(
            map(lambda trans: trans.replace(" ", ""), new_transitions)
        )
        # clean empty strings
        new_transitions = filter(lambda x: not x == "", new_transitions)
        new_transitions_list = []

        def get_terminals(string: str) -> tuple[str, str]:
            no_terminal = ""
            terminal = ""

            for no_term in self.no_terminals:
                if no_term in string:
                    string = string.replace(no_term, "")
                    no_terminal = no_term
                    break

            for term in self.terminals:
                if term in string:
                    string = string.replace(term, "")
                    terminal = term
                    break

            if not string == "":
                raise Exception("There is an extra character")

            if no_terminal == "" or terminal == "":
                raise Exception("The characters dont match terminal and no terminal")

            return (terminal, no_terminal)

        try:
            for transition in new_transitions:
                splited_trans = transition.split(">")
                if len(splited_trans) == 1:
                    raise Exception("The syntax is not correct")

                # 'C' '$'
                if splited_trans[1] == "$":
                    # get first element
                    self._acceptance_no_terminals.append(splited_trans[0])
                    continue
                # 'A' '0B'
                elif len(splited_trans) == 2:
                    pass
                else:
                    raise Exception("The syntax is not correct")

                # '0'     'B'
                terminal, not_terminal = get_terminals(splited_trans[1])

                if terminal == "" or not_terminal == "":
                    raise Exception("No Terminal or terminal detected")

                new_transitions_list.append(
                    Transition(splited_trans[0], terminal, not_terminal)
                )

        except:
            raise ProductionsSyntaxException(
                "Transition syntax is not formatted correctly"
            )

        # verify if acceptance no terminals are correct
        self.acceptance_no_terminals = ";".join(self._acceptance_no_terminals)

        # TODO verify if this thing really is an afd
        self._transitions = new_transitions_list

    @property
    def valid_string(self) -> str:
        string_list: list[str] = []
        state = self.initial_no_terminal
        temp_transition_list = self.productions.copy()

        while True:
            available_transition: list[Transition] = list(
                filter(
                    lambda transition: transition.origin == state, temp_transition_list
                )
            )

            # remove one transition from the list
            temp_transition_list.remove(available_transition[0])
            # add transition entry to string list
            string_list.append(available_transition[0].entry)
            # change state to the next transition
            state = available_transition[0].destination

            # if the next state is an acceptance state break from the loop
            if state in self.acceptance_no_terminals:
                break

        return "".join(string_list)

    def evaluate_string(self, string: str) -> list[Transition]:
        transitions: list[Transition] = []
        state = self.initial_no_terminal
        # current_state = self.initial_no_terminal
        string_list = list(string)
        in_acceptance_state = False

        for char in string_list:
            # if character is not in terminals
            if char not in self.terminals:
                raise InvalidStringException(
                    "The character doesn't belong to the terminals"
                )
            # given the current state get available transitions
            available_transitions: list[Transition] = list(
                filter(lambda transition: transition.origin == state, self.productions)
            )

            # given the available transitions, get the correct one
            correct_transition: list[Transition] = list(
                filter(
                    lambda transition: transition.entry == char,
                    available_transitions,
                )
            )

            if len(correct_transition) == 0:
                raise InvalidStringException("There is no transition with this letter")

            state = correct_transition[0].destination
            transitions.append(correct_transition[0])

            if state in self._acceptance_no_terminals:
                in_acceptance_state = True
            else:
                in_acceptance_state = False

        if not in_acceptance_state:
            raise InvalidStringException("The string ended in no acceptance state")

        return transitions

    def __str__(self):
        return f"Name: {self.name}\nNo_Terminals: {self._no_terminals}\nTerminals: {self._terminals}\nInitial State: {self._initial_no_terminal}\nAcceptance No_Terminals: {self._acceptance_no_terminals}"


# Exception classes for error handling


class InvalidStringException(Exception):
    pass


class NameException(Exception):
    pass


class NoTerminalsException(Exception):
    pass


class TerminalsException(Exception):
    pass


class InitialStateException(Exception):
    pass


class AcceptanceNoTerminalsException(Exception):
    pass


class ProductionsSyntaxException(Exception):
    pass


class ProductionsException(Exception):
    pass

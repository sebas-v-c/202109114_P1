from AFD.afd import AFD
from GR.gr import GR


def create_diagraph(obj) -> str:
    if isinstance(obj, AFD):
        return create_afd_diagraph(obj)
    elif isinstance(obj, GR):
        return create_gr_diagraph(obj)
    return ""


def create_description(obj) -> str:
    if isinstance(obj, AFD):
        return create_afd_description(obj)
    elif isinstance(obj, GR):
        return create_gr_description(obj)
    return ""


def create_route_description(obj, transitions: list, string: str) -> str:
    if isinstance(obj, AFD):
        return create_afd_route_description(obj, transitions, string)
    elif isinstance(obj, GR):
        return create_gr_route_description(obj, transitions, string)
    return ""


def create_route_diagraph(obj, transitions: list) -> str:
    if isinstance(obj, AFD):
        return create_afd_route_diagraph(obj, transitions)
    elif isinstance(obj, GR):
        return create_gr_route_diagraph(obj, transitions)
    return ""


# -------------------------------------AFD-------------------------------------#
def create_afd_diagraph(afd: AFD) -> str:
    lines: list[str] = []

    lines.append("rankdir=LR;")

    transitions = ";".join(afd.states) + ";"
    lines.append(transitions)

    # add acceptance state
    for state in afd.acceptance_states:
        lines.append(state + " [peripheries=2];")

    lines.append('INICIO [shape="triangle"]')
    lines.append("INICIO -> " + afd.initial_state + ";")
    # add transitions
    for transition in afd.transitions:
        lines.append(
            " -> ".join([transition.origin, transition.destination])
            + ' [label="'
            + transition.entry
            + '"];'
        )

    return "\n".join(lines)


def create_afd_description(afd: AFD) -> str:
    lines: list[str] = []

    lines.append("node [shape=circle];")
    lines.append("fontsize=40")
    lines.append('NodeLabel [shape=none fontsize=18 fontname = "monospace" label = <')
    lines.append("Nombre: " + afd.name + "<br/>")

    align_left = '<br align="left"/>'

    lines.append("Estados: " + " ".join(afd.states) + align_left)
    lines.append("Alfabeto: " + " ".join(afd.alfabet) + align_left)
    lines.append(
        "Estados de aceptación: " + " ".join(afd.acceptance_states) + align_left
    )
    lines.append("Estado inicial: " + afd.initial_state + align_left)
    lines.append("Transiciones: " + align_left)

    for transition in afd.transitions:
        lines.append(str(transition) + align_left)

    lines.append(" " + align_left)
    lines.append("Cadena válida de ejemplo: " + afd.valid_string + align_left)
    lines.append(">];")

    return "\n".join(lines)


def create_afd_route_description(afd: AFD, transitions: list, string: str) -> str:
    """Generate a description in Graphviz Syntax for the transitions that the
    AFD took"""
    lines: list[str] = []

    lines.append("node [shape=circle];")
    lines.append("fontsize=40")
    lines.append("NodeLabel [shape=none fontsize=18 label = <")
    lines.append("Nombre: " + afd.name + "<br/>")

    align_left = '<br align="left"/>'

    lines.append("Estados: " + " ".join(afd.states) + align_left)
    lines.append("Alfabeto: " + " ".join(afd.alfabet) + align_left)
    lines.append(
        "Estados de aceptación: " + " ".join(afd.acceptance_states) + align_left
    )
    lines.append("Estado inicial: " + afd.initial_state + align_left)
    lines.append("Transiciones Realizadas: " + align_left)

    num = 1
    for transition in transitions:
        lines.append(str(num) + ". " + str(transition) + align_left)
        num += 1

    lines.append(" " + align_left)
    lines.append("Cadena ingresada: " + string + align_left)
    lines.append(">];")

    return "\n".join(lines)


def create_afd_route_diagraph(afd: AFD, transitions: list) -> str:
    lines: list[str] = []

    lines.append("rankdir=LR;")
    lines.append("")

    for i in range(len(transitions)):
        lines[1] += str(i) + ";"

    lines.append(str(len(transitions)) + " [peripheries=2];")

    lines.append('INICIO [shape="triangle"]')
    lines.append("INICIO -> 0;")

    for i in range(len(transitions)):
        lines.append(
            " -> ".join([str(i), str(i + 1)])
            + ' [label="'
            + transitions[i].entry
            + '"];'
        )

    return "\n".join(lines)


# --------------------------------------GR--------------------------------------#
def create_gr_diagraph(gr: GR) -> str:
    lines: list[str] = []

    lines.append("rankdir=LR;")

    transitions = ";".join(gr.no_terminals) + ";"
    lines.append(transitions)

    # add acceptance state
    for state in gr.acceptance_no_terminals:
        lines.append(state + " [peripheries=2];")

    lines.append('INICIO [shape="triangle"]')
    lines.append("INICIO -> " + gr.initial_no_terminal + ";")
    # add transitions
    for transition in gr.productions:
        lines.append(
            " -> ".join([transition.origin, transition.destination])
            + ' [label="'
            + transition.entry
            + '"];'
        )

    return "\n".join(lines)


def create_gr_description(gr: GR) -> str:
    lines: list[str] = []

    lines.append("node [shape=circle];")
    lines.append("fontsize=40")
    lines.append("NodeLabel [shape=none fontsize=18 label = <")
    lines.append("Nombre: " + gr.name + "<br/>")

    align_left = '<br align="left"/>'

    lines.append("No Terminales: " + " ".join(gr.no_terminals) + align_left)
    lines.append("Terminales: " + " ".join(gr.terminals) + align_left)
    lines.append("No terminal inicial: " + gr.initial_no_terminal + align_left)
    lines.append("Producciones: " + align_left)

    for no_terminal in gr.no_terminals:
        # get productions
        no_term_productions = list(
            filter(lambda prod: no_terminal == prod.origin, gr.productions)
        )

        if len(no_term_productions) == 0 and no_terminal in gr.acceptance_no_terminals:
            lines.append(" ".join([no_terminal, "&gt;", "$"]))
            continue

        lines.append(str(no_term_productions[0]) + align_left)
        for i in range(1, len(no_term_productions)):
            lines.append(
                " ".join(["" for letter in no_term_productions[i].origin])
                + "  | "
                + " ".join(
                    [no_term_productions[i].entry, no_term_productions[i].destination]
                )
                + align_left
            )

        if no_terminal in gr.acceptance_no_terminals:
            lines.append(
                " ".join(
                    [
                        ""
                        for letter in no_term_productions[
                            len(no_term_productions) - 1
                        ].origin
                    ]
                )
                + "  | "
                + "$"
                + align_left
            )

    lines.append(" " + align_left)
    lines.append("Cadena válida de ejemplo: " + gr.valid_string + align_left)
    lines.append(">];")

    return "\n".join(lines)


def create_gr_route_description(gr: GR, transitions: list, string: str) -> str:
    """Generate a description in Graphviz Syntax for the transitions that the
    GR took"""
    lines: list[str] = []

    lines.append("node [shape=circle];")
    lines.append("fontsize=40")
    lines.append("NodeLabel [shape=none fontsize=18 label = <")
    lines.append("Nombre: " + gr.name + "<br/>")

    align_left = '<br align="left"/>'

    lines.append("No Terminales: " + " ".join(gr.no_terminals) + align_left)
    lines.append("Terminales: " + " ".join(gr.terminals) + align_left)
    lines.append("Estado inicial: " + gr.initial_no_terminal + align_left)
    lines.append("Producciones: " + align_left)

    num = 1
    for transition in transitions:
        lines.append(str(num) + ". " + str(transition) + align_left)
        num += 1

    lines.append(" " + align_left)
    lines.append("Cadena ingresada: " + string + align_left)
    lines.append(">];")

    return "\n".join(lines)


def create_gr_route_diagraph(gr: GR, transitions: list) -> str:
    lines: list[str] = []

    lines.append("rankdir=LR;")
    lines.append("")

    for i in range(len(transitions)):
        lines[1] += str(i) + ";"

    lines.append(str(len(transitions)) + " [peripheries=2];")

    lines.append('INICIO [shape="triangle"]')
    lines.append("INICIO -> 0;")

    for i in range(len(transitions)):
        lines.append(
            " -> ".join([str(i), str(i + 1)])
            + ' [label="'
            + transitions[i].entry
            + '"];'
        )

    return "\n".join(lines)

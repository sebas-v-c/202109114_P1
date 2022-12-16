from AFD.afd import AFD


def create_diagraph(afd: AFD) -> str:
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


def create_description(afd: AFD) -> str:
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
    lines.append("Transiciones: " + align_left)

    for transition in afd.transitions:
        lines.append(
            transition.origin
            + ", "
            + transition.entry
            + "; "
            + transition.destination
            + align_left
        )

    lines.append(" " + align_left)
    lines.append("Cadena válida de ejemplo: " + afd.valid_string + align_left)
    lines.append(">];")

    return "\n".join(lines)


def create_route_description(afd: AFD, transitions: list, string: str) -> str:
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
        lines.append(
            str(num)
            + ". "
            + transition.origin
            + ", "
            + transition.entry
            + "; "
            + transition.destination
            + align_left
        )
        num += 1

    lines.append(" " + align_left)
    lines.append("Cadena ingresada: " + string + align_left)
    lines.append(">];")

    return "\n".join(lines)


def create_route_diagraph(afd: AFD, transitions: list) -> str:
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

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

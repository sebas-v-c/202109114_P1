#!/usr/bin/env python3


class Controller:
    def __init__(self, app, view) -> None:
        self._app = app
        self._view = view(app)
        app.switch_frame(self._view)

        self._view.set_controller(self)

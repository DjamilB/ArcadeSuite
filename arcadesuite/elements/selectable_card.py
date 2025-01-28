from nicegui import ui


UNSELECTED_CLASS = "no-shadow"
SELECTED_CLASS = ""
UNSELECTED_COLOR = "bg-grey-1"
SELECTED_COLOR = "bg-light-blue-2"


class SelectableCard(ui.card):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._classes.append(UNSELECTED_CLASS)
        self._classes.append(UNSELECTED_COLOR)

    def select(self):
        if UNSELECTED_CLASS in self._classes:
            self._classes.remove(UNSELECTED_CLASS)

        if UNSELECTED_COLOR in self._classes:
            self._classes.remove(UNSELECTED_COLOR)

        if SELECTED_CLASS not in self._classes:
            self._classes.append(SELECTED_CLASS)

        if SELECTED_COLOR not in self._classes:
            self._classes.append(SELECTED_COLOR)

        self.update()

    def unselect(self):
        if SELECTED_CLASS in self._classes:
            self._classes.remove(SELECTED_CLASS)

        if SELECTED_COLOR in self._classes:
            self._classes.remove(SELECTED_COLOR)

        if UNSELECTED_CLASS not in self._classes:
            self._classes.append(UNSELECTED_CLASS)

        if UNSELECTED_COLOR not in self._classes:
            self._classes.append(UNSELECTED_COLOR)

        self.update()

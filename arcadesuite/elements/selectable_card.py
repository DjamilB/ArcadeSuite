from nicegui import ui


UNSELECTED_CLASS = "no-shadow"
SELECTED_CLASS = ""
UNSELECTED_COLOR = "bg-grey-1"
SELECTED_COLOR = "bg-light-blue-2"

UNACTIVE_COLOR = "bg-grey-5"


class SelectableCard(ui.card):
    def __init__(self, active=True, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._active = True
        self._selected = False
        self._classes.append(UNSELECTED_CLASS)
        self._classes.append(UNSELECTED_COLOR)

    def select(self):
        self._selected = True
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
        self._selected = False
        if SELECTED_CLASS in self._classes:
            self._classes.remove(SELECTED_CLASS)

        if SELECTED_COLOR in self._classes:
            self._classes.remove(SELECTED_COLOR)

        if UNSELECTED_CLASS not in self._classes:
            self._classes.append(UNSELECTED_CLASS)

        if UNSELECTED_COLOR not in self._classes:
            self._classes.append(UNSELECTED_COLOR)

        self.update()

    def activate(self):
        if not self._active:
            self._active = True
            self._classes.remove(UNACTIVE_COLOR)
            self._classes.append(UNSELECTED_COLOR)
            self.update()
        return self

    def deactivate(self):
        if self._active:
            self._active = False

            if self._selected:
                if SELECTED_CLASS in self._classes:
                    self._classes.remove(SELECTED_CLASS)

                if SELECTED_COLOR in self._classes:
                    self._classes.remove(SELECTED_COLOR)
            else:
                if UNSELECTED_COLOR in self._classes:
                    self._classes.remove(UNSELECTED_COLOR)

            self._classes.append(UNACTIVE_COLOR)
            self.update()
        return self

from nicegui import ui
from .selectable_card import SelectableCard


class CheckboxCard(SelectableCard):
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with self:
            self._checkbox = ui.checkbox(name)

    def toggle_box(self):
        self._checkbox.set_value(not self._checkbox.value)

    def get_value(self):
        return self._checkbox.value

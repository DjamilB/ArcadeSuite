from nicegui import ui
from .selectable_card import SelectableCard


class LabelCard(SelectableCard):
    def __init__(self, text, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with self:
            self.label = ui.label(text).classes("text-2x1 text-center align-middle font-bold")

    def set_text(self, text):
        self.label.text = text

    def get_text(self):
        return self.label.text

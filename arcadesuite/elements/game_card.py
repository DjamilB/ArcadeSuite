from nicegui import ui
from .selectable_card import SelectableCard


class GameCard(SelectableCard):
    def __init__(self, name, icon_path, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with self:
            ui.label(name)
            if icon_path != "":
                ui.image(icon_path)

from nicegui import ui
from .selectable_card import SelectableCard
import os
import json


class GameCard(SelectableCard):
    def __init__(self, name, icon_path, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with self:
            self.label = ui.label(name)
            if os.path.isfile(f"../res/{name}/meta.json"):
                with open(f"../res/{name}/meta.json", "r") as file:
                    meta = json.load(file)
                    if "img_url" in meta:
                        ui.image(meta["img_url"])


    def get_text(self):
        return self.label.text

from nicegui import ui
from .selectable_card import SelectableCard
import os
import json


class GameCard(SelectableCard):
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with self:
            path = "../res/meta.json"
            if os.path.isfile(path):
                with open(path, "r") as file:
                    meta = json.load(file)
                    ui.image(meta[name]["img_url"])
                    ui.label(meta[name]["title"]).style('text-align: center; display: block; width: 100%; font-weight: bold')
            else:
                raise FileNotFoundError(f"The file {path} does not exist.")


    def get_text(self):
        return self.label.text

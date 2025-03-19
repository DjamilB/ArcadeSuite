from nicegui import ui
from .selectable_card import SelectableCard
import os
import json
import utils


class GameCard(SelectableCard):
    """
    A game card that displays the image and title of a game.

    Attributes:
        `label` is the label of the game card.
    """
    def __init__(self, name, *args, **kwargs):
        """
        Initializes the game card.
        :param name: the title of the game.
        """
        super().__init__(*args, **kwargs)

        with self:
            path = os.path.join(utils.res_path, "meta.json")
            if os.path.isfile(path):
                with open(path, "r") as file:
                    meta = json.load(file)
                    ui.image(meta[name]["img_url"])
                    ui.label(meta[name]["title"]).style('text-align: center; display: block; width: 100%; font-size: 20px;')
            else:
                raise FileNotFoundError(f"The file {path} does not exist.")


    def get_text(self):
        """
        :return: the text of the `label` attribute.
        """
        return self.label.text

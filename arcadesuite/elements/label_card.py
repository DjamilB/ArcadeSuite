from nicegui import ui
from .selectable_card import SelectableCard


class LabelCard(SelectableCard):
    """
    A label card that displays a text.
    """
    def __init__(self, text, *args, **kwargs):
        """
        Initializes the label card.
        :param text: the text to display.
        """
        super().__init__(*args, **kwargs)

        with self:
            self.label = ui.label(text).classes("text-2x1 text-center align-middle font-bold")

    def set_text(self, text):
        """
        Sets the text of the label card.
        :param text: the text to display.
        """
        self.label.text = text

    def get_text(self):
        """
        :return: the text of the *label* attribute.
        """
        return self.label.text

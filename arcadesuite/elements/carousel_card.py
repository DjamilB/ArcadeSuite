from nicegui import ui
from .selectable_card import SelectableCard

class CarouselCard(SelectableCard):
    """
    A carousel card that cycles through a list of items.

    :attr:`label` is the label of the carousel card.
    :attr:`_items` is the dictionary of items to cycle through.
    :attr:`_keys` is the list of keys of the dictionary.
    :attr:`_index` is the current index of the carousel.
    :attr:`_agents` is a boolean value that indicates if the carousel is for agents
    """

    def __init__(self, name, items, *args, **kwargs):
        """
        Initializes the carousel card.
        
        :param name: The name of the carousel card.
        :param items: A dictionary of items to cycle through.
        """
        super().__init__(*args, **kwargs)
        self._items = items
        self._keys = list(items)
        self._index = 0
        self._agents = "Agent" in self._keys or "Player" in self._keys

        with self:
            with ui.row():
                self.label = ui.label(name).style("")
                if self._agents:
                    self._key_label = ui.label(self._keys[0]).style("color: blue;")
                else: 
                    self._key_label = ui.label(self._keys[0]).style("color: red;")

    def next(self):
        """
        Advances the carousel to the next item.
        """
        self._index = (self._index + 1) % len(self._keys)
        current_key = self._keys[self._index]

        self._key_label.text = current_key
        
        if not self._agents:
            if current_key == "Default" or current_key =="Off":
                self._key_label.style("color: red;") 
            else:
                self._key_label.style("color: green;")
        self.update()

    def get_current(self):
        """
        :return: the current item.
        """
        return self._items[self._keys[self._index]]

    def get_text(self):
        """
        :return: the text of the *label* attribute.
        """
        return self.label.text

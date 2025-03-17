from nicegui import ui
from .selectable_card import SelectableCard

class CarouselCard(SelectableCard):
    def __init__(self, name, items, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._items = items
        self._keys = list(items)
        self._index = 0
        self._agents = "Agent" in self._keys or "Player" in self._keys

        with self:
            with ui.row():
                self.label = ui.label(name).style("font-weight: bold;")
                if self._agents:
                    self._key_label = ui.label(self._keys[0]).style("font-weight: bold; color: blue;")
                else: 
                    self._key_label = ui.label(self._keys[0]).style("font-weight: bold; color: red;")

    def next(self):
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
        return self._items[self._keys[self._index]]

    def get_text(self):
        return self.label.text

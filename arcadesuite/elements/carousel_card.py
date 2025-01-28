from nicegui import ui
from .selectable_card import SelectableCard


class CarouselCard(SelectableCard):
    def __init__(self, name, items, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._items = items
        self._keys = list(items)
        self._index = 0

        with self:
            with ui.row():
                ui.label(name)
                self._key_label = ui.label(self._keys[0])

    def next(self):
        self._index = (self._index + 1) % len(self._keys)
        self._key_label.text = self._keys[self._index]
        self.update()

    def get_current(self):
        return self._items[self._keys[self._index]]

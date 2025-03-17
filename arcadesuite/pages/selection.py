from nicegui import ui
from nicegui.events import KeyEventArguments
from utils import get_json, head_html
import os

import elements


class Selection:
    def __init__(self, game_page):
        self._game_page = game_page
        self._current_selection_index = 0
        self._current_agent_index = 0
        self._current_agent_path_index = 0
        self._current_modif_index = 0

        @ui.page("/selection")
        def selection():
            self._selection_cards = list()
            ui.add_head_html(head_html)
            with ui.row(align_items="center").classes("absolute-center w-full h-full items-center"):
                with ui.column(align_items="left").classes("justify-center w-[50%] q-pl-md"):
                    self._selection_cards.append(elements.LabelCard("Agents"))
                    self._selection_cards.append(elements.LabelCard("Modifiers"))
                    self._selection_cards.append(elements.LabelCard("Play"))

                ui.image(self.meta["img_url"]).props("fit='contain'").classes("absolute-right h-full w-[50%]")
            self._selection_cards[self._current_selection_index].select()

            ui.keyboard(on_key=self.handle_selection_keys)

        @ui.page("/selection/Agents")
        def agents():
            self._agent_cards = list()
            ui.add_head_html(head_html)
            with ui.row(align_items="center").classes("absolute-center w-full h-full items-center"):
                with ui.column(align_items="left").classes("justify-center w-[50%] q-pl-md"):
                    if self.meta["multiplayer"]:
                        self._agent_cards.append(elements.CarouselCard("Multiplayer", {"Off": False, "On": True}))
                    self._agent_cards.append(elements.CarouselCard("Player1", {"Player": "Player", "Agent": "Agent"}))
                    if self.p1_is_agent:
                        self._agent_cards[-1].next()
                    self._agent_cards.append(elements.LabelCard("Select Agent"))
                    if not self.p1_is_agent:
                        self._agent_cards[-1].deactivate()
                    if self.p1_agent_path != "":
                        self._agent_cards[-1].set_text(f"Agent: {self.p1_agent_path}")

                    if self.meta["multiplayer"]:
                        self._agent_cards.append(elements.CarouselCard("Player2", {"Player": "Player", "Agent": "Agent"}))
                        if not self.is_multiplayer:
                            self._agent_cards[-1].deactivate()
                        if self.p2_is_agent:
                            self._agent_cards[-1].next()
                        self._agent_cards.append(elements.LabelCard("Select Agent"))
                        if not self.p2_is_agent or not self.is_multiplayer:
                            self._agent_cards[-1].deactivate()
                        if self.p2_agent_path != "":
                            self._agent_cards[-1].set_text(f"Agent: {self.p2_agent_path}")
                    self._agent_cards.append(elements.LabelCard("Submit"))

            ui.image(self.meta["img_url"]).props("fit='contain'").classes("absolute-right h-full w-[50%]")
            self._agent_cards[self._current_agent_index].select()

            ui.keyboard(on_key=self.handle_agent_keys)

        @ui.page("/selection/Agents/path")
        def agent_path():
            self._agent_path_cards = list()
            self.agents = os.listdir(f"../models/{self.selected_game}/0")

            ui.add_head_html(head_html)
            with ui.row(align_items="center").classes("absolute-center w-full h-full items-center"):
                with ui.column(align_items="left").classes("justify-center w-[50%] q-pl-md"):
                    for agent in self.agents:
                        self._agent_path_cards.append(elements.LabelCard(agent))

            ui.image(self.meta["img_url"]).props("fit='contain'").classes("absolute-right h-full w-[50%]")
            self._agent_path_cards[self._current_agent_path_index].select()

            ui.keyboard(on_key=self.handle_agent_path_keys)

        @ui.page("/selection/Modifiers")
        def modifs():
            self._modif_cards = list()

            ui.add_head_html(head_html)
            with ui.row(align_items="center").classes("absolute-center w-full h-full items-center"):
                with ui.column(align_items="left").classes("justify-center w-[50%] q-pl-md"):
                    for modif in self.modifs:
                        if isinstance(self.meta["modifs"][modif], dict):
                            self._modif_cards.append(elements.CarouselCard(modif, self.meta["modifs"][modif]).classes("q-pr-md"))

                            n = 0
                            found = False
                            for m in self.meta["modifs"][modif]:
                                if self.meta["modifs"][modif][m] in self.selected_modifs:
                                    found = True
                                    break
                                n += 1

                            if found:
                                for i in range(n):
                                    self._modif_cards[-1].next()
                        else:
                            self._modif_cards.append(elements.CheckboxCard(modif).classes("q-pr-md"))
                            if modif in self.selected_modifs:
                                self._modif_cards[-1].toggle_box()
                    self._modif_cards.append(elements.LabelCard("Submit").classes("q-pa-sm"))

            ui.image(self.meta["img_url"]).props("fit='contain'").classes("absolute-right h-full w-[50%]")
            self._modif_cards[self._current_modif_index].select()

            ui.keyboard(on_key=self.handle_modif_keys)

    def set_selected_game(self, game):
        self.selected_game = game
        # self.meta = get_json(f"../res/{game}/meta.json")
        self.meta = get_json(f"../res/meta.json")[game]
        self.selected_modifs = []
        self.p1_is_agent = False
        self.p2_is_agent = False
        self.p1_agent_path = ""
        self.p2_agent_path = ""
        self.is_multiplayer = False

        self.modifs = list()
        for modif in self.meta["modifs"]:
            self.modifs.append(modif)

    def handle_selection_keys(self, e: KeyEventArguments):
        prev_index = self._current_selection_index
        if e.action.keydown:
            if e.key.arrow_up:
                while True:
                    if self._current_selection_index > 0:
                        self._current_selection_index -= 1
                    else:
                        self._current_selection_index = len(self._selection_cards) - 1

                    if self._selection_cards[self._current_selection_index]._active:
                        break
            elif e.key.arrow_down:
                while True:
                    self._current_selection_index = (self._current_selection_index + 1) % len(self._selection_cards)
                    if self._selection_cards[self._current_selection_index]._active:
                        break
            elif e.key == "Escape":
                ui.navigate.to("/")
            elif e.key == "Enter":
                if self._selection_cards[self._current_selection_index].get_text() == "Play":
                    self._game_page.populate(self.selected_game,
                                             self.selected_modifs,
                                             self.p1_is_agent,
                                             self.p1_agent_path,
                                             self.is_multiplayer,
                                             self.p2_is_agent if self.is_multiplayer else False,
                                             self.p2_agent_path)
                    ui.navigate.to("/game_page")
                else:
                    ui.navigate.to(f"/selection/{self._selection_cards[self._current_selection_index].get_text()}")

        self._selection_cards[prev_index].unselect()
        self._selection_cards[self._current_selection_index].select()

    def handle_agent_keys(self, e: KeyEventArguments):
        prev_index = self._current_agent_index
        if e.action.keydown:
            if e.key.arrow_up:
                while True:
                    if self._current_agent_index > 0:
                        self._current_agent_index -= 1
                    else:
                        self._current_agent_index = len(self._agent_cards) - 1

                    if self._agent_cards[self._current_agent_index]._active:
                        break
            elif e.key.arrow_down:
                while True:
                    self._current_agent_index = (self._current_agent_index + 1) % len(self._agent_cards)

                    if self._agent_cards[self._current_agent_index]._active:
                        break
            elif e.key == "Enter":
                if isinstance(self._agent_cards[self._current_agent_index], elements.CarouselCard):
                    self._agent_cards[self._current_agent_index].next()

                    if self._agent_cards[self._current_agent_index].get_text() == "Player1":
                        self.is_p1 = True
                        self.p1_is_agent = self._agent_cards[self._current_agent_index].get_current() == "Agent"
                        if self.p1_is_agent:
                            self._agent_cards[self._current_agent_index + 1].activate()
                        else:
                            self._agent_cards[self._current_agent_index + 1].deactivate()
                    elif self._agent_cards[self._current_agent_index].get_text() == "Player2":
                        self.is_p1 = False
                        self.p2_is_agent = self._agent_cards[self._current_agent_index].get_current() == "Agent"
                        if self.p2_is_agent:
                            self._agent_cards[self._current_agent_index + 1].activate()
                        else:
                            self._agent_cards[self._current_agent_index + 1].deactivate()
                    elif self._agent_cards[self._current_agent_index].get_text() == "Multiplayer":
                        self.is_multiplayer = self._agent_cards[self._current_agent_index].get_current()
                        if self._agent_cards[self._current_agent_index].get_current():
                            self._agent_cards[-3].activate()
                            if self.p2_is_agent:
                                self._agent_cards[-2].activate()
                        else:
                            self._agent_cards[-3].deactivate()
                            self._agent_cards[-2].deactivate()
                elif self._agent_cards[self._current_agent_index].get_text() == "Submit":
                    ui.navigate.to("/selection")
                elif "Agent" in self._agent_cards[self._current_agent_index].get_text():
                    ui.navigate.to("/selection/Agents/path")

        self._agent_cards[prev_index].unselect()
        self._agent_cards[self._current_agent_index].select()

    def handle_agent_path_keys(self, e: KeyEventArguments):
        prev_index = self._current_agent_path_index
        if e.action.keydown:
            if e.key.arrow_up:
                while True:
                    if self._current_agent_path_index > 0:
                        self._current_agent_path_index -= 1
                    else:
                        self._current_agent_path_index = len(self._agent_path_cards) - 1

                    if self._agent_path_cards[self._current_agent_path_index]._active:
                        break
            elif e.key.arrow_down:
                while True:
                    self._current_agent_path_index = (self._current_agent_path_index + 1) % len(self._agent_path_cards)

                    if self._agent_path_cards[self._current_agent_path_index]._active:
                        break
            elif e.key == "Enter":
                text = self._agent_path_cards[self._current_agent_path_index].get_text()
                if self.is_p1:
                    self.p1_agent_path = f"../models/{self.selected_game}/0/{text}"
                else:
                    self.p2_agent_path = f"../models/{self.selected_game}/0/{text}"
                ui.navigate.to("/selection/Agents")

        self._agent_path_cards[prev_index].unselect()
        self._agent_path_cards[self._current_agent_path_index].select()

    def handle_modif_keys(self, e: KeyEventArguments):
        prev_index = self._current_modif_index
        if e.action.keydown:
            if e.key.arrow_up:
                while True:
                    if self._current_modif_index > 0:
                        self._current_modif_index -= 1
                    else:
                        self._current_modif_index = len(self._modif_cards) - 1

                    if self._modif_cards[self._current_modif_index]._active:
                        break
            elif e.key.arrow_down:
                while True:
                    self._current_modif_index = (self._current_modif_index + 1) % len(self._modif_cards)

                    if self._modif_cards[self._current_modif_index]._active:
                        break
            elif e.key == "Enter":
                if isinstance(self._modif_cards[self._current_modif_index], elements.CarouselCard):
                    self._modif_cards[self._current_modif_index].next()
                elif isinstance(self._modif_cards[self._current_modif_index], elements.CheckboxCard):
                    self._modif_cards[self._current_modif_index].toggle_box()
                elif self._modif_cards[self._current_modif_index].get_text() == "Submit":
                    self.selected_modifs = []
                    for card in self._modif_cards:
                        if isinstance(card, elements.CarouselCard) and card.get_current() not in self.selected_modifs:
                            if card.get_current() != "":
                                self.selected_modifs.append(card.get_current())
                        elif isinstance(card, elements.CheckboxCard):
                            modifier = self.meta["modifs"][card._checkbox.text]
                            if card.get_value() and modifier not in self.selected_modifs:
                                self.selected_modifs.append(modifier)
                            elif modifier in self.selected_modifs:
                                self.selected_modifs.remove(modifier)
                    ui.navigate.to("/selection")

        self._modif_cards[prev_index].unselect()
        self._modif_cards[self._current_modif_index].select()

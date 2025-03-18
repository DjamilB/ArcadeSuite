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
        self._current_seed_index = 0
        self._current_type_index = 0
        self._current_agent_path_index = 0
        self._current_modif_index = 0

        @ui.page("/selection")
        def selection():
            self._selection_cards = list()
            ui.add_head_html(head_html)

            with ui.row(align_items="center").classes('h-screen w-full item-center'):
                with ui.column(align_items="center").classes('w-[49%]'):    
                    self._selection_cards.append(elements.LabelCard("Agents"))
                    self._selection_cards.append(elements.LabelCard("Modifiers"))
                    self._selection_cards.append(elements.LabelCard("Play"))
                self.detail_panel()
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
                        if self.is_multiplayer:
                            self._agent_cards[-1].next()
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
                self.detail_panel()
            #ui.image(self.meta["img_url"]).props("fit='contain'").classes("absolute-right h-full w-[50%]")
            self._agent_cards[self._current_agent_index].select()

            ui.keyboard(on_key=self.handle_agent_keys)

        @ui.page("/selection/Agents/seed")
        def seed_selection_page():
            self._seed_cards = list()

            seeds = os.listdir(f"../models/{self.selected_game}")
            seeds.sort()

            ui.add_head_html(head_html)
            with ui.row(align_items="center").classes("absolute-center w-full h-full items-center"):
                with ui.column(align_items="start").classes("justify-center w-[50%] q-pl-md"):
                    for seed in seeds:
                        self._seed_cards.append(elements.LabelCard(f"Seed: {seed}"))
                self.detail_panel()
            self._seed_cards[self._current_seed_index].select()

            ui.keyboard(on_key=self.handle_seed_keys)

        @ui.page("/selection/Agents/type")
        def type_selection_page():
            self._type_cards = list()

            agents = os.listdir(f"../models/{self.selected_game}/{self.seed}")

            found_dqn = False
            found_obj_ppo = False
            found_pixel_ppo = False
            found_c51 = False

            for agent in agents:
                if "dqn" in agent:
                    found_dqn = True
                if "obj_ppo" in agent:
                    found_obj_ppo = True
                if "pixel_ppo" in agent:
                    found_pixel_ppo = True
                if "c51" in agent:
                    found_c51 = True

                if found_dqn and found_obj_ppo and found_pixel_ppo and found_c51:
                    break

            ui.add_head_html(head_html)
            with ui.row(align_items="center").classes("absolute-center w-full h-full items-center"):
                with ui.column(align_items="start").classes("justify-center w-[50%] q-pl-md"):
                    if found_dqn:
                        self._type_cards.append(elements.LabelCard("DQN"))
                    if found_c51:
                        self._type_cards.append(elements.LabelCard("C51"))
                    if found_obj_ppo:
                        self._type_cards.append(elements.LabelCard("Object PPO"))
                    if found_pixel_ppo:
                        self._type_cards.append(elements.LabelCard("Pixel PPO"))
                self.detail_panel()
            self._type_cards[self._current_type_index].select()


            ui.keyboard(on_key=self.handle_type_keys)

        @ui.page("/selection/Agents/path")
        def agent_selection_page():
            all_agents = os.listdir(f"../models/{self.selected_game}/{self.seed}")
            agents = list()

            for agent in all_agents:
                if self.type in agent:
                    agents.append(agent)

            agents.sort()

            self._agent_path_cards = list()

            ui.add_head_html(head_html)
            with ui.row(align_items="center").classes("absolute-center w-full h-full items-center"):
                with ui.column(align_items="start").classes("justify-center w-[50%] q-pl-md"):
                    for agent in agents:
                        self._agent_path_cards.append(elements.LabelCard(agent))
                self.detail_panel()
            self._agent_path_cards[self._current_agent_path_index].select()

            ui.keyboard(on_key=self.handle_path_keys)

        @ui.page("/selection/Modifiers")
        def modifs():
            self._modif_cards = list()

            ui.add_head_html(head_html)
            with ui.row(align_items="center").classes("absolute-center w-full h-full items-center"):
                with ui.column(align_items="left").classes("justify-center w-[50%] q-pl-md"):
                    for modif in self.modifs:
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
                    self._modif_cards.append(elements.LabelCard("Submit").classes("q-pa-sm"))
                self.detail_panel()

            #ui.image(self.meta["img_url"]).props("fit='contain'").classes("absolute-right h-full w-[50%]")
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

    @staticmethod
    def handle_movement(index, list, e: KeyEventArguments):
        if e.key.arrow_up:
            while True:
                if index > 0:
                    index -= 1
                else:
                    index = len(list) - 1

                if list[index]._active:
                    break
        elif e.key.arrow_down:
            while True:
                index = (index + 1) % len(list)

                if list[index]._active:
                    break
        return index
    
    def detail_panel(self):
        with ui.column(align_items="center").classes('w-[49%] bg-gray-100'):
            ui.label("Details").tailwind.font_weight('bold')
            ui.label(f"Game: {self.selected_game}")
            ui.label(f"Player 1: {self.p1_agent_path if self.p1_is_agent else 'Human'}")
            ui.label(f"Player 2: {self.p2_agent_path if self.p2_is_agent else ('Human' if self.is_multiplayer else 'System')}")
            ui.label(f"Modifications: {', '.join(self.selected_modifs) if len(self.selected_modifs) > 0 else 'None'}")

    def handle_selection_keys(self, e: KeyEventArguments):
        prev_index = self._current_selection_index
        if e.action.keydown:
            self._current_selection_index = self.handle_movement(self._current_selection_index, self._selection_cards, e)

            if e.key == "Escape":
                self._current_selection_index = 0
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

                    self._current_selection_index = 0
                    ui.navigate.to("/game_page")
                else:
                    ui.navigate.to(f"/selection/{self._selection_cards[self._current_selection_index].get_text()}")

        self._selection_cards[prev_index].unselect()
        self._selection_cards[self._current_selection_index].select()

    def handle_agent_keys(self, e: KeyEventArguments):
        prev_index = self._current_agent_index
        if e.action.keydown:
            self._current_agent_index = self.handle_movement(self._current_agent_index, self._agent_cards, e)

            if e.key == "Escape":
                self._current_agent_index = 0
                ui.navigate.to("/selection")
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
                    self.is_p1 = self._agent_cards[self._current_agent_index - 1].get_text() == "Player1"
                    ui.navigate.to("/selection/Agents/seed")

        self._agent_cards[prev_index].unselect()
        self._agent_cards[self._current_agent_index].select()

    def handle_seed_keys(self, e: KeyEventArguments):
        prev_index = self._current_seed_index

        if e.action.keydown:
            self._current_seed_index = self.handle_movement(self._current_seed_index, self._seed_cards, e)

            if e.key == "Escape":
                self._current_seed_index = 0
                ui.navigate.to("/selection/Agents")
            elif e.key == "Enter":
                self.seed = self._seed_cards[self._current_seed_index].get_text().split(" ")[1]
                ui.navigate.to(f"/selection/Agents/type")

        self._seed_cards[prev_index].unselect()
        self._seed_cards[self._current_seed_index].select()

    def handle_type_keys(self, e: KeyEventArguments):
        prev_index = self._current_type_index

        if e.action.keydown:
            self._current_type_index = self.handle_movement(self._current_type_index, self._type_cards, e)

            if e.key == "Escape":
                self._current_type_index = 0
                ui.navigate.to("/selection/Agents/seed")
            elif e.key == "Enter":
                text = self._type_cards[self._current_type_index].get_text()

                self.type = text.lower().replace(" ", "_")
                if self.type == "object_ppo":
                    self.type = "obj_ppo"

                ui.navigate.to("/selection/Agents/path")

        self._type_cards[prev_index].unselect()
        self._type_cards[self._current_type_index].select()

    def handle_path_keys(self, e: KeyEventArguments):
        prev_index = self._current_agent_path_index
        if e.action.keydown:
            self._current_agent_path_index = self.handle_movement(self._current_agent_path_index, self._agent_path_cards, e)

            if e.key == "Escape":
                self._current_agent_path_index = 0
                ui.navigate.to("/selection/Agents/type")
            elif e.key == "Enter":
                text = self._agent_path_cards[self._current_agent_path_index].get_text()
                if self.is_p1:
                    self.p1_agent_path = f"../models/{self.selected_game}/{self.seed}/{text}"
                else:
                    self.p2_agent_path = f"../models/{self.selected_game}/{self.seed}/{text}"

                self._current_seed_index = 0
                self._current_type_index = 0
                self._current_agent_path_index = 0
                ui.navigate.to("/selection/Agents")

        self._agent_path_cards[prev_index].unselect()
        self._agent_path_cards[self._current_agent_path_index].select()

    def handle_modif_keys(self, e: KeyEventArguments):
        prev_index = self._current_modif_index
        if e.action.keydown:
            self._current_modif_index = self.handle_movement(self._current_modif_index, self._modif_cards, e)

            if e.key == "Escape":
                self._current_modif_index = 0
                ui.navigate.to("/selection")
            elif e.key == "Enter":
                if isinstance(self._modif_cards[self._current_modif_index], elements.CarouselCard):
                    self._modif_cards[self._current_modif_index].next()
                elif self._modif_cards[self._current_modif_index].get_text() == "Submit":
                    self.selected_modifs = []
                    for card in self._modif_cards:
                        if isinstance(card, elements.CarouselCard) and card.get_current() not in self.selected_modifs:
                            if card.get_current() != "":
                                self.selected_modifs.append(card.get_current())
                    self._current_modif_index = 0
                    ui.navigate.to("/selection")
        self._modif_cards[prev_index].unselect()
        self._modif_cards[self._current_modif_index].select()

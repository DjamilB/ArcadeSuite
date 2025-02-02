# fix issues with arch linux
import multiprocessing
multiprocessing.set_start_method("spawn", force=True)

from nicegui import ui, app
from nicegui.events import KeyEventArguments
from utils import get_games, get_json
import os

import elements
import pages


GAMES = get_games("../res/")
select_index = 0
select_class = "no-shadow"
select_color = "bg-light-blue-2"
normal_color = "bg-grey-1"

selection_index = 0

selected_game = GAMES[0]
modif_selection = list()

player_agent_selection = []

cards = dict()


# Uncomment to open Web Inspector
# app.native.start_args["debug"] = True


game_page = pages.GamePage()
select_page = pages.Selection(game_page)


@ui.page("/")
def main_page():
    global cards
    ui.add_head_html("<style>body {background-color: bisque;}</style>")
    with ui.grid(columns=6):
        for game in GAMES:
            path = ""
            if os.path.isfile(f"../res/{game}/icon.png"):
                path = f"../res/{game}/icon.png"
            cards[game] = elements.GameCard(game, path)

            if game == GAMES[select_index]:
                cards[game].select()

    def handle_key(e: KeyEventArguments):
        global select_index
        global selected_game
        prev_select = select_index
        if e.action.keydown:
            if e.key.arrow_left:
                if select_index > 0:
                    select_index -= 1
                else:
                    select_index = len(GAMES) - 1
            elif e.key.arrow_right:
                if select_index < len(GAMES) - 1:
                    select_index += 1
                else:
                    select_index = 0
            elif e.key == "Enter":
                select_page.set_selected_game(selected_game)
                ui.navigate.to("/selection")

            cards[GAMES[prev_select]].unselect()
            cards[GAMES[select_index]].select()
            selected_game = GAMES[select_index]

    ui.keyboard(on_key=handle_key)


ui.run(title="Arcade Suite", native=False, dark=False, window_size=(900, 1050))

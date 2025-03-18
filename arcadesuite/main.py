# fix issues with arch linux
import multiprocessing
multiprocessing.set_start_method("spawn", force=True)

from nicegui import ui, app
from nicegui.events import KeyEventArguments
from utils import get_games, get_json, head_html, handle_menu_movement
import os

import elements
import pages

CARD_COLUMNS = 10

# Uncomment to open Web Inspector
# app.native.start_args["debug"] = True

app.add_static_files(url_path="/static/javascript", local_directory=os.path.join(os.path.dirname(__file__), 'javascript'))

game_page = pages.GamePage()
select_page = pages.Selection(game_page)

select_index = 0

# TODO(lars): make resource/model folder locations program arguments
@ui.page("/")
def main_page():
    global select_index

    GAMES = get_games()
    selected_game = GAMES[select_index]
    cards = list()

    ui.add_head_html(head_html)

    with ui.grid(columns=CARD_COLUMNS):
        for game in GAMES:
            cards.append(elements.GameCard(game))

            if game == GAMES[select_index]:
                cards[-1].select()

    def handle_key(e: KeyEventArguments):
        global select_index
        nonlocal selected_game
        prev_select = select_index
        if e.action.keydown:
            select_index = handle_menu_movement(select_index, cards, e, CARD_COLUMNS)

            if e.key == "Enter":
                select_page.set_selected_game(selected_game)
                ui.navigate.to("/selection")

            cards[prev_select].unselect()
            cards[select_index].select()
            selected_game = GAMES[select_index]

    ui.keyboard(on_key=handle_key)


ui.run(title="Arcade Suite", native=False, dark=False, window_size=(1000, 900))

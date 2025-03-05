# fix issues with arch linux
import multiprocessing
multiprocessing.set_start_method("spawn", force=True)

from nicegui import ui, app
from nicegui.events import KeyEventArguments
from utils import get_games, get_json, head_html
import os

import elements
import pages

CARD_COLUMNS = 6

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
    cards = dict()

    ui.add_head_html(head_html)

    with ui.grid(columns=CARD_COLUMNS):
        for game in GAMES:
            cards[game] = elements.GameCard(game)

            if game == GAMES[select_index]:
                cards[game].select()

    def handle_key(e: KeyEventArguments):
        global select_index
        nonlocal selected_game
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
            elif e.key.arrow_up:
                if select_index >= CARD_COLUMNS:
                    select_index -= CARD_COLUMNS
            elif e.key.arrow_down:
                if select_index <= len(GAMES) - 1 - CARD_COLUMNS:
                    select_index += CARD_COLUMNS
            elif e.key == "Enter":
                select_page.set_selected_game(selected_game)
                ui.navigate.to("/selection")

            cards[GAMES[prev_select]].unselect()
            cards[GAMES[select_index]].select()
            selected_game = GAMES[select_index]

    ui.keyboard(on_key=handle_key)


ui.run(title="Arcade Suite", native=False, dark=False, window_size=(1000, 900))

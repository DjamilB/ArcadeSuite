# fix issues with arch linux
import multiprocessing
multiprocessing.set_start_method("spawn", force=True)

from argparse import ArgumentParser
from nicegui import ui, app
from nicegui.events import KeyEventArguments
from arcadesuite.utils import get_games, head_html, handle_menu_movement, set_models_path, set_resources_path
import os

CARD_COLUMNS = 10
NATIVE_MODE = True
FULLSCREEN = False

models_path = None
resources_path = None

# Uncomment to open Web Inspector in native mode
# app.native.start_args["debug"] = True

parser = ArgumentParser(
    prog="arcadesuite",
    description="Arcade Suite",
)
parser.add_argument(
    "--native",
    action="store_true",
    help="Run the application in native mode",
)
parser.add_argument(
    "--fullscreen",
    action="store_true",
    help="Run the application in fullscreen mode",
)
parser.add_argument("-m", "--model", type=str, help="Path of the models folder", default="../models")
parser.add_argument("-r", "--resource", type=str, help="Path of the ScoBots resources folder", default="../ScoBots/resources")

args = parser.parse_args()

if args.model is not None:
    set_models_path(args.model)

if args.resource is not None:
    set_resources_path(args.resource)

# import those here so the paths are set before they are imported
import elements
import pages

app.add_static_files(url_path="/static/javascript", local_directory=os.path.join(os.path.dirname(__file__), 'javascript'))

game_page = pages.GamePage()
select_page = pages.Selection(game_page)

select_index = 0

first_start = True

# TODO(lars): make resource/model folder locations program arguments
@ui.page("/")
def main_page():
    global select_index
    global first_start

    GAMES = get_games()
    selected_game = GAMES[select_index]
    cards = list()

    ui.add_head_html(head_html)

    with ui.grid(columns=CARD_COLUMNS):
        for game in GAMES:
            cards.append(elements.GameCard(game))

            if game == GAMES[select_index]:
                cards[-1].select()

    if not args.fullscreen and first_start and args.native:
        app.native.main_window.maximize()
        first_start = False

    def handle_key(e: KeyEventArguments):
        global select_index
        nonlocal selected_game
        prev_select = select_index
        if e.action.keydown:
            select_index = handle_menu_movement(select_index, cards, e, CARD_COLUMNS)

            if e.key == "Enter":
                select_page.set_selected_game(selected_game)
                ui.navigate.to("/selection")
            elif e.key == "Escape":
                if NATIVE_MODE:
                    app.shutdown()

            cards[prev_select].unselect()
            cards[select_index].select()
            selected_game = GAMES[select_index]

    ui.keyboard(on_key=handle_key)


ui.run(title="Arcade Suite", native=args.native, fullscreen=args.fullscreen)
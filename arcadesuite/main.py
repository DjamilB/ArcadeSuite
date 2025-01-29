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
                ui.navigate.to("/selection")

            cards[GAMES[prev_select]].unselect()
            cards[GAMES[select_index]].select()
            selected_game = GAMES[select_index]

    ui.keyboard(on_key=handle_key)


@ui.page("/selection")
def main_page():
    global selected_mode
    global selected_game
    global selection_index
    global player_agent_selection

    player_agent_selection = []
    files = []

    if not os.path.isfile(f"../res/{selected_game}/meta.json"):
        ui.navigate.to("/game_screen")
    else:
        # Button states
        playerSelection = ["Player", "Agent"]
        selection_index = 0

        # Selcted Option in GUI
        selection = []

        # Single Player vs. Multiplayer
        meta = get_json(f"../res/{selected_game}/meta.json")
        singlePlayer = not meta["multiplayer"]

        cards = dict()
        ui.add_head_html("<style>body {background-color: bisque;}</style>")

        def single_player_selection():
            with ui.row(align_items="center").classes("absolute-center w-full h-full items-center"):
                with ui.column(align_items="left").classes("justify-center w-[50%] q-pl-md"):
                    with ui.column().classes("w-full h-screen justify-center align-center items-center"):
                        ui.label(selected_game).classes("w-full text-2xl text-center align-middle font-bold")

                        cards[selection[0]] = elements.LabelCard(playerSelection[0], align_items="center").classes("w-full")
                        cards[selection[0]].select()
                        cards[selection[1]] = elements.LabelCard("Submit", align_items="center").classes("w-full")

                ui.image(f"../res/{selected_game}/icon.png").props("fit='contain' width='50%'").classes("fixed-right h-full")

        def multi_player__selection():
            with ui.row(align_items="center").classes("absolute-center w-full h-full items-center"):
                with ui.column(align_items="left").classes("justify-center w-[50%] q-pl-md"):
                    with ui.column().classes("w-full h-screen justify-center align-center items-center"):
                        ui.label(selected_game).classes("w-full text-2xl text-center align-middle font-bold")

                        with ui.row().classes("w-full gap-4 justify-center"):
                            cards[selection[0]] = elements.LabelCard(playerSelection[0], align_items="center").classes("w-1/3")
                            cards[selection[0]].select()
                            cards[selection[1]] = elements.LabelCard(playerSelection[0], align_items="center").classes("w-1/3")

                        cards[selection[2]] = elements.LabelCard("Submit", align_items="center").classes("w-2/3")
                ui.image(f"../res/{selected_game}/icon.png").props("fit='contain' width='50%'").classes("fixed-right h-full")

        def updateStatus(name):
            previous_index = playerSelection.index(cards[name].label.text)
            new_index = (previous_index + 1) % len(playerSelection)

            cards[name].label.text = playerSelection[new_index]
            cards[name].label.update()

        async def choose_file(index):
            item,  = await app.native.main_window.create_file_dialog(allow_multiple=False)
            file = item
            # print(file)
            files[index] = file

        def choose_agent(index):
            pass

        async def handle_key(e: KeyEventArguments):
            global selection_index
            global player_agent_selection
            prev_index = selection_index

            if e.action.keydown:
                if e.key == "Escape":
                    ui.navigate.to("/")

                elif e.key.arrow_up:
                    prev_index = selection_index
                    if singlePlayer:
                        if selection_index > 0:
                            selection_index -= 1
                        else:
                            selection_index = len(selection)-1
                    else:
                        if selection_index < len(selection)-1:
                            selection_index = len(selection)-1
                        else:
                            selection_index = 0
                    cards[selection[prev_index]].unselect()
                    cards[selection[selection_index]].select()

                elif e.key.arrow_down:
                    prev_index = selection_index
                    if singlePlayer:
                        if selection_index < len(selection)-1:
                            selection_index += 1
                        else:
                            selection_index = 0
                    else:
                        if selection_index < len(selection)-1:
                            selection_index = len(selection)-1
                        else:
                            selection_index = 0
                    cards[selection[prev_index]].unselect()
                    cards[selection[selection_index]].select()

                elif not singlePlayer and (e.key.arrow_right or e.key.arrow_left):
                    if selection_index < len(selection)-1:
                        cards[selection[selection_index]].unselect()
                        selection_index = (selection_index + 1) % 2
                        cards[selection[selection_index]].select()

                elif e.key == " " and selection[selection_index] != "Submit":
                    if cards[selection[selection_index]].label.text == "Agent":
                        await choose_file(selection_index)

                elif e.key == "Enter":
                    if selection_index != len(selection)-1:
                        updateStatus(selection[selection_index])
                    else:
                        temp = True
                        for i in range(0, len(selection)-1):
                            if cards[selection[selection_index]].label.text == "Agent" and files[i] == "-":
                                temp = False
                        if temp:
                            player_agent_selection = files
                            ui.navigate.to("/menu")
                        else:
                            ui.notify("No Agent selected!")
                            ui.notify("Press Whitespace to select Agent")

        if singlePlayer:
            selection.extend(["PlayerA", "Submit"])
            files = ["-"]
            single_player_selection()

        else:
            selection.extend(["PlayerA", "PlayerB", "Submit"])
            files = ["-", "-"]
            multi_player__selection()

        ui.keyboard(on_key=handle_key)


game_page = pages.GamePage()


@ui.page("/menu")
def menu_page():
    global selected_modif_index
    global selected_modif
    global modif_cards

    ui.add_head_html("<style>body {background-color: bisque;}</style>")
    meta = get_json(f"../res/{selected_game}/meta.json")

    modifs = list()
    for modif in meta["modifs"]:
        modifs.append(modif)
    modifs.append("Submit")

    selected_modif_index = 0
    selected_modif = modifs[selected_modif_index]

    modif_cards = dict()
    with ui.row(align_items="center").classes("absolute-center w-full h-full items-center"):
        with ui.column(align_items="left").classes("justify-center w-[50%] q-pl-md"):
            for modif in modifs:
                if modif == "Submit":
                    modif_cards[modif] = elements.LabelCard("Submit").classes("q-pa-sm")
                elif isinstance(meta["modifs"][modif], dict):
                    modif_cards[modif] = elements.CarouselCard(modif, meta["modifs"][modif]).classes("q-pr-md")
                else:
                    modif_cards[modif] = elements.CheckboxCard(modif).classes("q-pr-md")

                if modif == selected_modif:
                    modif_cards[modif].select()
        ui.image(f"../res/{selected_game}/icon.png").props("fit='contain'").classes("absolute-right h-full w-[50%]")

    def handle_key(e: KeyEventArguments):
        global selected_modif_index
        global selected_modif

        update = False

        prev_select = selected_modif_index
        if e.action.keydown:
            if e.key == "Escape":
                ui.navigate.to("/selection")
            elif e.key.arrow_up:
                if selected_modif_index > 0:
                    selected_modif_index -= 1
                else:
                    selected_modif_index = len(modifs) - 1
                update = True
            elif e.key.arrow_down:
                if selected_modif_index < len(modifs) - 1:
                    selected_modif_index += 1
                else:
                    selected_modif_index = 0
                update = True
            elif e.key == "Enter":
                if selected_modif == "Submit":
                    global modif_selection
                    modif_selection = list()
                    for modif in modifs:
                        if modif != "Submit":
                            if isinstance(modif_cards[modif], elements.CarouselCard):
                                modif_selection.append(modif_cards[modif].get_current())
                            elif modif_cards[modif].get_value():
                                modif_selection.append(modif)
                    ui.navigate.to("/game_page")
                    is_agent = len(player_agent_selection) > 0 and player_agent_selection[0] != "-"
                    game_page.populate(selected_game, modif_selection, is_agent, player_agent_selection[0] if is_agent else "")
                elif isinstance(modif_cards[selected_modif], elements.CarouselCard):
                    modif_cards[selected_modif].next()
                else:
                    modif_cards[selected_modif].toggle()

        if update:
            modif_cards[modifs[prev_select]].unselect()
            modif_cards[modifs[selected_modif_index]].select()
            selected_modif = modifs[selected_modif_index]

    ui.keyboard(on_key=handle_key)


ui.run(title="Arcade Suite", native=False, dark=False, window_size=(900, 1050))

from nicegui import ui, app
from nicegui.events import KeyEventArguments
from utils import get_games, get_json


GAMES = get_games('../res/')
select_index = 0
select_class = 'no-shadow'
select_color = 'bg-light-blue-2'
normal_color = 'bg-grey-1'

selected_game = GAMES[0]


cards = dict()

# app.native.start_args["debug"] = True


@ui.page("/")
def main_page():
    global cards
    ui.add_head_html('<style>body {background-color: bisque;}</style>')
    with ui.grid(columns=6):
        for game in GAMES:
            cards[game] = ui.card(align_items='center')
            with cards[game]:
                ui.label(game)
                ui.image('../res/' + game + '/icon.png')
            if game == GAMES[select_index]:
                cards[game].classes(select_color)
                continue
            else:
                cards[game].classes('no-shadow ' + normal_color)

    def handle_key(e: KeyEventArguments):
        global select_index
        global selected_game
        prev_select = select_index
        update = False
        if e.action.keydown:
            if e.key.arrow_left:
                if select_index > 0:
                    select_index -= 1
                else:
                    select_index = len(GAMES) - 1
                update = True
            elif e.key.arrow_right:
                if select_index < len(GAMES) - 1:
                    select_index += 1
                else:
                    select_index = 0
                update = True
            elif e.key == 'Enter':
                ui.navigate.to("/menu")

        if update:
            selected_game = GAMES[select_index]
            cards[GAMES[select_index]]._classes.remove(select_class)
            cards[GAMES[select_index]]._classes.remove(normal_color)
            cards[GAMES[select_index]]._classes.append(select_color)

            cards[GAMES[prev_select]]._classes.append(select_class)
            cards[GAMES[prev_select]]._classes.append(normal_color)
            cards[GAMES[prev_select]]._classes.remove(select_color)

            cards[GAMES[select_index]].update()
            cards[GAMES[prev_select]].update()

    ui.keyboard(on_key=handle_key)


@ui.page("/menu")
def menu_page():
    global selected_modif_index
    global selected_modif
    global modif_cards

    ui.add_head_html('<style>body {background-color: bisque;}</style>')
    meta = get_json(f"../res/{selected_game}/meta.json")
    modifs = list()
    for modif in meta["modifs"]:
        modifs.append(modif)
    modifs.append("Submit")

    selected_modif_index = 0
    selected_modif = modifs[selected_modif_index]

    modif_cards = dict()
    modif_checkboxes = dict()
    with ui.row(align_items="center").classes("absolute-center w-full h-full items-center"):
        with ui.column(align_items="left").classes("justify-center w-[50%] q-pl-md"):
            for modif in modifs:
                modif_cards[modif] = ui.card().tight()
                with modif_cards[modif] as card:
                    with ui.row():
                        if modif == "Submit":
                            card.classes("q-pa-sm")
                            ui.label(modif)
                        else:
                            card.classes("q-pr-md")
                            modif_checkboxes[modif] = ui.checkbox(modif)
                if modif == selected_modif:
                    modif_cards[modif].classes(f"{select_color}")
                else:
                    modif_cards[modif].classes(f"{normal_color} {select_class}")
        ui.image(f"../res/{selected_game}/icon.png").props("fit='contain' width='50%'").classes("fixed-right h-full")

    def handle_key(e: KeyEventArguments):
        global selected_modif_index
        global selected_modif

        update = False

        prev_select = selected_modif_index
        if e.action.keydown:
            if e.key == 'Escape':
                ui.navigate.to("/")
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
                    sel = list()
                    for modif in modifs:
                        if modif != "Submit" and modif_checkboxes[modif].value:
                            sel.append(modif)
                    # TODO: route to next menu page or delete objects and rebuild for other menu options?
                else:
                    modif_checkboxes[selected_modif].set_value(not modif_checkboxes[selected_modif].value)

        if update:
            selected_modif = modifs[selected_modif_index]
            modif_cards[modifs[selected_modif_index]]._classes.remove(select_class)
            modif_cards[modifs[selected_modif_index]]._classes.remove(normal_color)
            modif_cards[modifs[selected_modif_index]]._classes.append(select_color)

            modif_cards[modifs[prev_select]]._classes.append(select_class)
            modif_cards[modifs[prev_select]]._classes.append(normal_color)
            modif_cards[modifs[prev_select]]._classes.remove(select_color)

            modif_cards[modifs[selected_modif_index]].update()
            modif_cards[modifs[prev_select]].update()

    ui.keyboard(on_key=handle_key)


ui.run(title="Arcade Suite", native=True, dark=False, window_size=(900, 600))

from nicegui import ui
from nicegui.events import KeyEventArguments
from utils import get_games

GAMES = get_games('../res/')
select_index = 0
select_class = 'no-shadow'
select_color = 'bg-light-blue-2'
normal_color = 'bg-grey-1'


ui.add_head_html('<style>body {background-color: bisque;}</style>')


cards = dict()
with ui.grid(columns=6):
    first = True
    for game in GAMES:
        cards[game] = ui.card(align_items='center')
        with cards[game]:
            ui.label(game)
            ui.image('../res/' + game + '/icon.png')
        if first:
            cards[game].classes(select_color)
            first = False
            continue
        else:
            cards[game].classes('no-shadow ' + normal_color)


def handle_key(e: KeyEventArguments):
    global select_index
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
            ui.notify('Selected ' + GAMES[select_index])

    if update:
        cards[GAMES[select_index]]._classes.remove(select_class)
        cards[GAMES[select_index]]._classes.remove(normal_color)
        cards[GAMES[select_index]]._classes.append(select_color)

        cards[GAMES[prev_select]]._classes.append(select_class)
        cards[GAMES[prev_select]]._classes.append(normal_color)
        cards[GAMES[prev_select]]._classes.remove(select_color)

        cards[GAMES[select_index]].update()
        cards[GAMES[prev_select]].update()


keyboard = ui.keyboard(on_key=handle_key)

ui.run(native=True, dark=False)

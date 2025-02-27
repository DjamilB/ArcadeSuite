from nicegui import ui, app
import graphviz
import time
from .BinaryDotTree import BinaryDotTree
from .treeElements import getViper

#app.native.start_args["debug"]=True
path = True

# Modell laden
model = getViper("Boxing_seed0_reward-env_oc_pruned-extraction")
temp = BinaryDotTree(model)

# Initialen DOT-Code setzen
dot_code = str(temp.getRandomPath())

# Funktion zum Rendern von DOT als SVG
def render_dot(dot_text):
    dot_graph = graphviz.Source(dot_text)
    return dot_graph.pipe(format="svg").decode("utf-8")

# UI-Komponente für die Grafik
svg_container = ui.html(render_dot(dot_code))

# FPS-Anzeige
fps_label = ui.label("FPS: 0")

# Variablen für FPS-Messung
frame_count = 0
start_time = time.perf_counter()

# Funktion zur automatischen Aktualisierung
def update_graph():
    global frame_count, start_time

    # Neuen Graph generieren
    if path:
        dot_code = str(temp.getRandomPath())
    else: 
        dot_code = str(temp.getRandomTree())
    svg_container.set_content(render_dot(dot_code))

    # FPS berechnen
    frame_count += 1
    elapsed_time = time.perf_counter() - start_time
    if elapsed_time > 1.0:  # Alle 1 Sekunde FPS aktualisieren
        fps = frame_count / elapsed_time
        fps_label.set_text(f"FPS: {fps:.2f}")
        frame_count = 0
        start_time = time.perf_counter()

# Automatische Aktualisierung starten
def start_auto_update():
    while True:
        update_graph()

def changeRender():
    global path
    path = not path
    update_graph()


ui.button("Update Graph", on_click=update_graph)
ui.button("Change Render", on_click=changeRender)
ui.button("Start Auto Update", on_click=lambda: ui.timer(0.01, update_graph))  # 100 FPS Ziel
#ui.run(title="Arcade Suite",native=False,window_size=(900,1050))
ui.run(title="Arcade Suite",native=True)


from nicegui import ui
from nicegui.events import KeyEventArguments
from hackatari import HackAtari
from ocatari.utils import load_agent
import torch
import numpy as np
from base64 import b64encode
from utils import map_to_pygame_key_codes


class GamePage:
    def __init__(self):
        @ui.page("/game_page")
        def page():
            self.timer = ui.timer(1/30, self.step_game)

            # TODO(Lars): put in different file
            canvas_script = '''
            const canvas = document.getElementById("gameCanvas");
            const ctx = canvas.getContext("2d");
            const imageData = ctx.createImageData(800, 1050);

            function updateCanvas(base64Data) {
                const binaryData = atob(base64Data);  // Decode Base64 string to binary
                var pixelData = new Uint8ClampedArray(binaryData.length);
                for (let i = 0; i < binaryData.length; i++) {
                    pixelData[i] = binaryData.charCodeAt(i);  // Convert binary string to byte array
                }
                imageData.data.set(pixelData);  // Set pixel data on canvas
                ctx.putImageData(imageData, 0, 0);  // Render to canvas
            };
            '''

            ui.add_head_html("<style>body {background-color: black;}</style>")
            ui.add_body_html(f"<canvas id='gameCanvas' style='border: 1px solid black;' width=800px height=1050px/><script>{canvas_script}</script>")
            ui.keyboard(on_key=self.handle_key)

    def populate(self, game, modifs, is_agent, agent_path):
        self.is_agent = is_agent

        # create HackAtari environment
        obs_mode = "obj"
        if is_agent:
            if agent_path.find("dqn", 0, len(agent_path)) != -1:
                obs_mode = "dqn"
            elif agent_path.find("c51", 0, len(agent_path)) != -1:
                obs_mode = "dqn"

        self.env = HackAtari(game,
            modifs=modifs,
            render_mode="rgb_array",
            dopamine_pooling=False,
            full_action_space=False,
            obs_mode=obs_mode)

        if is_agent:
            _, self.policy = load_agent(agent_path, self.env, "cpu")
        self.obs, _ = self.env.reset()
        self.nstep = 1
        self.tr = 0

        self.env.render_oc_overlay = True
        self.env.render()
        self.env.render_oc_overlay = False

        self.keys2action = self.env.unwrapped.get_keys_to_action()
        self.current_keys_down = set()

    def handle_key(self, e: KeyEventArguments):
        if e.action.keydown:
            if e.key == "q":
                self.timer.cancel()
                ui.navigate.to("/")
            elif (map_to_pygame_key_codes(e.key),) in self.keys2action.keys():
                self.current_keys_down.add(map_to_pygame_key_codes(e.key))
        if e.action.keyup:
            if (map_to_pygame_key_codes(e.key),) in self.keys2action.keys():
                self.current_keys_down.remove(map_to_pygame_key_codes(e.key))

    async def step_game(self):
        self.pressed_keys = list(self.current_keys_down)
        self.pressed_keys.sort()
        self.pressed_keys = tuple(self.pressed_keys)
        if not self.is_agent:
            if self.pressed_keys in self.keys2action.keys():
                action = self.keys2action[self.pressed_keys]
            else:
                action = 0
        else:
            action = self.policy(torch.Tensor(self.obs).unsqueeze(0))[0]
        self.obs, reward, terminated, truncated, info = self.env.step(action)
        self.tr += reward
        if terminated or truncated:
            print(info)
            print(self.tr)
            self.tr = 0
            self.env.reset()
            # Navigate to some game over screen?
        self.nstep += 1

        rgb_data = self.env.render().transpose((1, 0, 2))
        rgba_data = np.concatenate([rgb_data, 255 * np.ones((1050, 800, 1), dtype=np.uint8)], axis=-1)  # Add alpha channel
        pixel_data = rgba_data.tobytes()  # Convert to raw bytes

        # Encode the data as Base64
        base64_pixel_data = b64encode(pixel_data).decode("utf-8")  # Convert to string for JavaScript

        # Debug: Print a snippet of the Base64 string
        # print("Sending Base64 data (truncated):", base64_pixel_data[:32])

        # Call the JavaScript update function
        ui.run_javascript(f"updateCanvas('{base64_pixel_data}')")

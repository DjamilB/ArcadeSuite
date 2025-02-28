from nicegui import ui
from nicegui.events import KeyEventArguments
from hackatari import HackAtari
from pettingzoo.atari.base_atari_env import BaseAtariEnv
from ocatari.utils import load_agent
import torch
import numpy as np
from base64 import b64encode
from utils import map_to_pygame_key_codes, head_html, get_keys_to_action_p1, get_keys_to_action_p2, load_multiplayer_agent
from supersuit import color_reduction_v0, resize_v1, frame_stack_v1, reshape_v0


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

            ui.add_head_html(head_html)
            ui.add_body_html(f"<canvas id='gameCanvas' style='border: 1px solid black;' width=800px height=1050px/><script>{canvas_script}</script>")
            ui.keyboard(on_key=self.handle_key)

    def populate(self, game, modifs, p1_is_agent, p1_agent_path, is_multiplayer=False, p2_is_agent=False, p2_agent_path=""):
        self.p1_is_agent = p1_is_agent
        self.p2_is_agent = p2_is_agent
        self.is_multiplayer = is_multiplayer

        # create HackAtari environment
        obs_mode = "obj"
        obs_type = "ram"
        if p1_is_agent:
            if p1_agent_path.find("dqn", 0, len(p1_agent_path)) != -1:
                obs_mode = "dqn"
                obs_type = "rgb_image"
            elif p1_agent_path.find("c51", 0, len(p1_agent_path)) != -1:
                obs_mode = "dqn"
                obs_type = "rgb_image"

        if is_multiplayer:
            self.env = BaseAtariEnv(game=game.lower(),
                                    num_players=2,
                                    mode_num=None,
                                    env_name=game.lower(),
                                    obs_type=obs_type,
                                    render_mode="rgb_array")
            self.env = reshape_v0(frame_stack_v1(resize_v1(color_reduction_v0(self.env, 'full'), x_size=84, y_size=84), 4), (4, 84, 84))
        else:
            self.env = HackAtari(game,
                                 modifs=modifs,
                                 render_mode="rgb_array",
                                 dopamine_pooling=False,
                                 full_action_space=not p1_is_agent,
                                 obs_mode=obs_mode)

        self.policies = dict()

        if p1_is_agent and not is_multiplayer:
            _, self.policies['first_0'] = load_agent(p1_agent_path, self.env, "cpu")
        elif p1_is_agent and p2_is_agent:
            _, self.policies['first_0'] = load_multiplayer_agent(p1_agent_path, self.env.unwrapped.possible_agents[0], self.env.unwrapped, "cpu")
            _, self.policies['second_0'] = load_multiplayer_agent(p2_agent_path, self.env.unwrapped.possible_agents[1], self.env.unwrapped, "cpu")

        if not is_multiplayer:
            self.obs, _ = self.env.reset()
        else:
            self.env.reset()
        self.nstep = 1
        self.tr = 0

        self.env.render_oc_overlay = True
        self.env.render()
        self.env.render_oc_overlay = False

        self.keys2action_p1 = get_keys_to_action_p1()
        self.keys2action_p2 = get_keys_to_action_p2()
        self.current_keys_down_p1 = set()
        self.current_keys_down_p2 = set()

    def handle_key(self, e: KeyEventArguments):
        if e.action.keydown:
            if e.key == "q":
                self.timer.cancel()
                ui.navigate.to("/")
            elif (str(e.key),) in self.keys2action_p1.keys():
                self.current_keys_down_p1.add(str(e.key))
            elif (str(e.key),) in self.keys2action_p2.keys():
                self.current_keys_down_p2.add(str(e.key))
        if e.action.keyup:
            if (str(e.key),) in self.keys2action_p1.keys():
                self.current_keys_down_p1.remove(str(e.key))
            if (str(e.key),) in self.keys2action_p2.keys():
                self.current_keys_down_p2.remove(str(e.key))

    # TODO(lars): finish multiplayer support
    async def step_game(self):
        self.pressed_keys_p1 = list(self.current_keys_down_p1)
        self.pressed_keys_p1.sort()
        self.pressed_keys_p1 = tuple(self.pressed_keys_p1)

        self.pressed_keys_p2 = list(self.current_keys_down_p2)
        self.pressed_keys_p2.sort()
        self.pressed_keys_p2 = tuple(self.pressed_keys_p2)

        if self.is_multiplayer:
            if self.p1_is_agent:
                observation, reward, termination, truncation, info = self.env.last()
                if termination or truncation:
                    action = None
                else:
                    action = self.policies['first_0'](torch.Tensor(observation).unsqueeze(0))[0]
            else:
                if self.pressed_keys_p1 in self.keys2action_p1.keys():
                    action = self.keys2action_p1[self.pressed_keys_p1]
                else:
                    action = 0

            self.env.step(action)

            if self.p2_is_agent:
                observation, reward, termination, truncation, info = self.env.last()
                if termination or truncation:
                    action = None
                else:
                    action = self.policies['second_0'](torch.Tensor(observation).unsqueeze(0))[0]
            else:
                if self.pressed_keys_p2 in self.keys2action_p2.keys():
                    action = self.keys2action_p2[self.pressed_keys_p2]
                else:
                    action = 0

            self.env.step(action)
        else:
            if not self.p1_is_agent:
                if self.pressed_keys_p1 in self.keys2action_p1.keys():
                    action = self.keys2action_p1[self.pressed_keys_p1]
                else:
                    action = 0
                self.obs, self.reward, self.terminated, self.truncated, self.info = self.env.step(action)
            else:
                action = self.policies['first_0'](torch.Tensor(self.obs).unsqueeze(0))[0]
                self.obs, self.reward, self.terminated, self.truncated, self.info = self.env.step(action)

        if self.is_multiplayer:
            _, self.reward, self.terminated, self.truncated, self.info = self.env.last()

        self.tr += self.reward
        if self.terminated or self.truncated:
            # print(info)
            # print(self.tr)
            self.tr = 0
            self.env.reset()
            # Navigate to some game over screen?
        self.nstep += 1

        if self.is_multiplayer:
            rgb_data = self.env.render().repeat(5, axis=0).repeat(5, axis=1)
        else:
            rgb_data = self.env.render().transpose((1, 0, 2))
        rgba_data = np.concatenate([rgb_data, 255 * np.ones((1050, 800, 1), dtype=np.uint8)], axis=-1)  # Add alpha channel
        pixel_data = rgba_data.tobytes()  # Convert to raw bytes

        # Encode the data as Base64
        base64_pixel_data = b64encode(pixel_data).decode("utf-8")  # Convert to string for JavaScript

        # Debug: Print a snippet of the Base64 string
        # print("Sending Base64 data (truncated):", base64_pixel_data[:32])

        # Call the JavaScript update function
        ui.run_javascript(f"updateCanvas('{base64_pixel_data}')")

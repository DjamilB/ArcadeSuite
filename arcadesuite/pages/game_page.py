from nicegui import ui
from nicegui.events import KeyEventArguments
from hackatari import HackAtari
from pettingzoo.atari.base_atari_env import BaseAtariEnv
import ocatari
import torch
import numpy as np
from DecisionTree.utils import get_Decisiontree_data   
from arcadesuite import DecisionTree
from base64 import b64encode
from utils import head_html, get_keys_to_action_p1, get_keys_to_action_p2, custom_load_agent
from supersuit import resize_v1, frame_stack_v1


class GamePage:
    def __init__(self):
        @ui.page("/game_page")
        def page():
            """
            Creates the game page with the game canvas and the decision tree visualization
            """
            # TODO(lars): rework game loop
            self.timer = ui.timer(1/30, self.step_game)

            ui.add_head_html(head_html)
            # Debug canvas for grayscale observation data
            # ui.add_body_html("<canvas id='grayCanvas' style='border: 1px solid black;' width=84px height=84px></canvas>")
            with ui.row():
                with ui.column():
                    ui.html("<canvas id='gameCanvas' onload='onCanvasLoad()' style='border: 1px solid black;' width=640px height=840px></canvas>")
                with ui.column():
                    self.tree_vis = ui.html("")
            ui.add_body_html("<script type='text/javascript' src='static/javascript/canvas.js'></script>")
            ui.keyboard(on_key=self.handle_key)

    def populate(self, game, modifs, p1_is_agent,_current_seed_index,  p1_agent_path, is_multiplayer=False, p2_is_agent=False, p2_agent_path=""):
        """
        Populates the game page with the given game, modifs and agents
        :param game: the game to be played
        :param modifs: the modifications to the game
        :param p1_is_agent: if player 1 is an agent
        :param p1_agent_path: path to the agent of player 1
        :param is_multiplayer: if the game is multiplayer
        :param p2_is_agent: if player 2 is an agent
        :param p2_agent_path: path to the agent of player 2
        """

        ocatari.core.UPSCALE_FACTOR = 4
        self.p1_is_agent = p1_is_agent
        self.p2_is_agent = p2_is_agent
        self.is_multiplayer = is_multiplayer
        self._current_seed_index = _current_seed_index

        # create HackAtari environment
        obs_mode = "obj"
        obs_type = "ram"
        if p1_is_agent:
            if "dqn" in p1_agent_path:
                obs_mode = "dqn"
                obs_type = "grayscale_image"
            elif "c51" in p1_agent_path:
                obs_mode = "dqn"
                obs_type = "grayscale_image"
            elif "obj" in p1_agent_path:
                model, features = get_Decisiontree_data(game, "env", self._current_seed_index)   # TODO (Djamil): Rewardtype (human, env)
                if model:
                    self.tree = DecisionTree.Decisiontree(model, features)
                else:
                    self.tree = None

        elif p2_is_agent:
            if "dqn" in p2_agent_path:
                obs_type = "grayscale_image"
            elif "c51" in p2_agent_path:
                obs_type = "grayscale_image"

        if is_multiplayer:
            self.env = BaseAtariEnv(game=game.lower(),
                                    num_players=2,
                                    mode_num=None,
                                    env_name=game.lower(),
                                    obs_type=obs_type,
                                    render_mode="rgb_array")

            # TODO(lars): Do reshape for ram observation?
            if obs_type == "grayscale_image":
                self.env = frame_stack_v1(resize_v1(self.env, x_size=84, y_size=84), 4)
        else:
            self.env = HackAtari(game,
                                 modifs=modifs,
                                 render_mode="rgb_array",
                                 dopamine_pooling=False,
                                 full_action_space=not p1_is_agent,
                                 obs_mode=obs_mode)

        self.policies = dict()

        if p1_is_agent:
            _, self.policies['first_0'] = custom_load_agent(p1_agent_path, 'first_0', self.env, is_multiplayer, "cpu")
        if p2_is_agent:
            _, self.policies['second_0'] = custom_load_agent(p2_agent_path, 'second_0', self.env, is_multiplayer, "cpu")

        if not is_multiplayer:
            self.obs, _ = self.env.reset()
        else:
            self.env.reset()
        self.nstep = 1
        self.tr = 0

        if not self.is_multiplayer:
            self.env.render_oc_overlay = True
            self.env.render()
            self.env.render_oc_overlay = False

        self.paused = False

        self.keys2action_p1 = get_keys_to_action_p1()
        self.keys2action_p2 = get_keys_to_action_p2()
        self.current_keys_down_p1 = set()
        self.current_keys_down_p2 = set()

    def handle_key(self, e: KeyEventArguments):
        if e.action.keydown:
            if e.key == "q":
                self.timer.cancel()
                ui.navigate.to("/")
            elif e.key == "p":
                self.paused = not self.paused
                if self.paused:
                    self.timer.deactivate()
                else:
                    self.timer.activate()
            elif e.key == "n":
                if self.paused:
                    self.step_game()
            elif e.key == "r":
                self.env.reset()
            elif e.key == "o":
                if not self.is_multiplayer:
                    self.env.render_oc_overlay = not self.env.render_oc_overlay
            elif (str(e.key),) in self.keys2action_p1.keys():
                self.current_keys_down_p1.add(str(e.key))
            elif (str(e.key),) in self.keys2action_p2.keys():
                self.current_keys_down_p2.add(str(e.key))
        if e.action.keyup:
            if (str(e.key),) in self.keys2action_p1.keys():
                self.current_keys_down_p1.remove(str(e.key))
            if (str(e.key),) in self.keys2action_p2.keys():
                self.current_keys_down_p2.remove(str(e.key))

    def step_game(self):
        """
        Steps the game by one frame
        """
        self.pressed_keys_p1 = list(self.current_keys_down_p1)
        self.pressed_keys_p1.sort()
        self.pressed_keys_p1 = tuple(self.pressed_keys_p1)

        self.pressed_keys_p2 = list(self.current_keys_down_p2)
        self.pressed_keys_p2.sort()
        self.pressed_keys_p2 = tuple(self.pressed_keys_p2)

        if self.is_multiplayer:
            if self.p1_is_agent:
                obs, reward, termination, truncation, info = self.env.last()
                if termination or truncation:
                    action = None
                else:
                    action = self.policies['first_0'](torch.Tensor(np.transpose(obs, (2, 0, 1))).unsqueeze(0))[0]
            else:
                if self.pressed_keys_p1 in self.keys2action_p1.keys():
                    action = self.keys2action_p1[self.pressed_keys_p1]
                else:
                    action = 0

            self.env.step(action)

            if self.p2_is_agent:
                obs, reward, termination, truncation, info = self.env.last()
                if termination or truncation:
                    action = None
                else:
                    action = self.policies['second_0'](torch.Tensor(np.transpose(obs, (2, 0, 1))).unsqueeze(0))[0]
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
                if self.tree:
                    temp = self.tree.get_path(self.obs.flatten())
                    self.tree_vis.set_content(temp)


        if self.is_multiplayer:
            _, self.reward, self.terminated, self.truncated, self.info = self.env.last()

        self.tr += self.reward
        if self.terminated or self.truncated:
            self.tr = 0
            self.env.reset()
            # Navigate to some game over screen?
        self.nstep += 1

        if self.is_multiplayer:
            rgb_data = self.env.render().repeat(4, axis=0).repeat(4, axis=1)
        else:
            rgb_data = self.env.render().transpose((1, 0, 2))
        rgba_data = np.concatenate([rgb_data, 255 * np.ones((840, 640, 1), dtype=np.uint8)], axis=-1)  # Add alpha channel
        pixel_data = rgba_data.tobytes()  # Convert to raw bytes

        # Encode the data as Base64
        base64_pixel_data = b64encode(pixel_data).decode("utf-8")  # Convert to string for JavaScript

        # Debug: Print a snippet of the Base64 string
        # print("Sending Base64 data (truncated):", base64_pixel_data[:32])

        # Call the JavaScript update function
        ui.run_javascript(f"updateCanvas('{base64_pixel_data}')")

        # if self.is_multiplayer:
        #     obs, _, _, _, _ = self.env.last()
        #     grayscale_image = np.delete(obs, [1, 2, 3], 2)
        #     grayscale_image = np.concatenate([grayscale_image, 255 * np.zeros((84, 84, 1), dtype=np.uint8)], axis=-1)
        #     grayscale_image = np.concatenate([grayscale_image, 255 * np.zeros((84, 84, 1), dtype=np.uint8)], axis=-1)
        #     grayscale_image = np.concatenate([grayscale_image, 255 * np.ones((84, 84, 1), dtype=np.uint8)], axis=-1)
        #     pixel_data = grayscale_image.tobytes()
        #
        #     base64_pixel_data = b64encode(pixel_data).decode("utf-8")
        #
        #     ui.run_javascript(f"updateGrayCanvas('{base64_pixel_data}')")

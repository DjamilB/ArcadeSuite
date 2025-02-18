# Arcade Suite
This is the repo for our Bachelors project.
The goal of this project is to let agents play the modified [HackAtari](https://github.com/k4ntz/HackAtari) versions of Atari2600 
Games with the help of [OC_Atari](https://github.com/k4ntz/OC_Atari). We are going to implement PvP, PvE and EvE modes and visualize the decision making of Agents when they are playing using [ScoBots](https://github.com/k4ntz/SCoBots).

## Run Instructions
**WARNING only tested on Ubuntu for now.** <br>
To run the app you will first have to clone at least the HackAtari submodule.
Then go into the HackAtari folder and run ```pip install -e .```. <br>
You will also have to install some dependencies with: <br>
```sudo apt install pkg-config libcairo2-dev gcc python3-dev libgirepository1.0-dev```. <br>
Then you can install the requirments with: <br>
```pip install -r requirements.txt``` <br>

## Supported Games
| Game | Singleplayer | Multiplayer |
| :--: | :----------: | :---------: |
| Chopper Command | :x: | :x: |
| Name This Game | :x: | :x: |
| Ms. Pacman | :heavy_check_mark: | :x: |
| Bank Heist | :heavy_check_mark: | :x: |
| Asterix | :heavy_check_mark: | :x: |
| Fishing Derby | :heavy_check_mark: | :x: |
| Demon Attack | :x: | :x: |
| Riverraid | :x: | :x: |
| Yars Revenge | :x: | :x: |
| Carnival | :x: | :x: |
| Freeway | :heavy_check_mark: | :x: |
| Skiing | :heavy_check_mark: | :x: |
| Breakout | :heavy_check_mark: | :x: |
| Amidar | :heavy_check_mark: | :x: | 
| Tennis | :heavy_check_mark: | :x: |
| Pong | :heavy_check_mark: | :x: |
| Venture | :x: | :x: |
| Seaquest | :heavy_check_mark: | :x: |
| Frostbite | :heavy_check_mark: | :x: |
| Boxing | :heavy_check_mark: | :x: |
| Space Invaders | :heavy_check_mark: | :x: |
| Galaxian | :x: | :x: |
| Atlantis | :heavy_check_mark: | :x: |
| Donkey Kong | :heavy_check_mark: | :x: |
| Double Dunk | :heavy_check_mark: | :x: |
| Montezuma Revenge | :heavy_check_mark: | :x: |
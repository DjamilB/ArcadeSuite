# Arcade Suite
This is the repo for our Bachelors project.
The goal of this project is to let agents play the modified [HackAtari](https://github.com/k4ntz/HackAtari)
versions of Atari2600 Games with the help of [OC_Atari](https://github.com/k4ntz/OC_Atari).
We are going to implement PvP, PvE and EvE modes and visualize
the decision-making of Agents when they are playing using [ScoBots](https://github.com/k4ntz/SCoBots).

## Installation Instructions
**WARNING: only works on Ubuntu for now.**

To run the app you will first have to install the HackAtari submodule as well
as install requirement for this project.

First, install some dependencies:
````bash
sudo apt install pkg-config libcairo2-dev;
sudo apt install gcc python3-dev libgirepository1.0-dev
````

Second, create and activate the virtual environment:
````bash
python3.9 -m venv .venv;
source .venv/bin/activate;
````

Third, clone HackAtari and install it:
````bash
git clone https://github.com/k4ntz/HackAtari/ HackAtari;
cd HackAtari;
pip install -e .;
pip install "gymnasium[atari, accept-rom-license]";
````

Fourth, install requirements for current project:
````bash
pip install -r requirements.txt;
````

### Setting up SCoBots
To install SCoBots:
````bash
git clone https://github.com/k4ntz/SCoBots/ SCoBots;
git checkout cleanup;
source .venv/bin/activate;
cd SCoBots;
pip install -e .;
pip install stable-baselines3[extras]==2.0.0;
````

#### Get agents for SCoBots
Add agents (only with seed 0) to the agents folder in SCoBots:
````bash
cd SCoBots;
wget https://hessenbox.tu-darmstadt.de/dl/fi47F21YBzVZBRfGPKswumb7/resources_seed0.zip;
unzip resources.zip;
rm resources.zip;
````
OR download agents (all seeds) for SCoBots:
````bash
cd SCoBots;
wget https://hessenbox.tu-darmstadt.de/dl/fiPLH36Zwi8EVv8JaLU4HpE2/resources_all.zip;
unzip resources.zip;
rm resources.zip;
````


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
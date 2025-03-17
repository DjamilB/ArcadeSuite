# Arcade Suite
This is the repo for our Bachelors project.
The goal of this project is to let agents play the modified [HackAtari](https://github.com/k4ntz/HackAtari)
versions of Atari2600 Games with the help of [OC_Atari](https://github.com/k4ntz/OC_Atari).
We are going to implement PvP, PvE and EvE modes and visualize
the decision-making of Agents when they are playing using [ScoBots](https://github.com/k4ntz/SCoBots).

## Installation Instructions
**WARNING: only tested on Ubuntu for now.**

This project uses Python 3.9

To run the app you will first have to install some dependencies.

For Ubuntu:
````bash
sudo apt install pkg-config libcairo2-dev gcc python3.9-dev libgirepository1.0-dev
````

For Arch:
```bash
sudo pacman -S pkgconf cairo libgirepository
```

Then init and update the submodules
````bash
git submodule init
git submodule update
````

To install HackAtari just go into the "HackAtari" directory with ```cd HackAtari``` and run
````bash
pip install -e .
````

After that go back to the directory of this repository with ```cd ..``` and run
````bash
pip install -r requirements.txt
pip install "gymnasium[atari, accept-rom-license]"
````

### Setting up SCoBots
To install SCoBots:
````bash
cd SCoBots
pip install -e .
pip install stable-baselines3[extras]==2.0.0
````

#### Get agents for SCoBots
Add agents (only with seed 0) to the agents folder in SCoBots:
````bash
cd SCoBots
wget https://hessenbox.tu-darmstadt.de/dl/fi47F21YBzVZBRfGPKswumb7/resources_seed0.zip
unzip resources.zip
rm resources.zip
````
OR download agents (all seeds) for SCoBots:
````bash
cd SCoBots
wget https://hessenbox.tu-darmstadt.de/dl/fiPLH36Zwi8EVv8JaLU4HpE2/resources_all.zip
unzip resources.zip
rm resources.zip
````

## Running this app
To run this app you just have to go to the 'arcadesuite' directory and run the 'main.py' from there.


## Supported Games
| Game | Singleplayer |    Multiplayer     |
| :--: | :----------: |:------------------:|
| Chopper Command | :x: |        :x:         |
| Name This Game | :x: |        :x:         |
| Ms. Pacman | :heavy_check_mark: |        :x:         |
| Bank Heist | :heavy_check_mark: |        :x:         |
| Asterix | :heavy_check_mark: |        :x:         |
| Fishing Derby | :heavy_check_mark: |        :x:         |
| Demon Attack | :x: |        :x:         |
| Riverraid | :x: |        :x:         |
| Yars Revenge | :x: |        :x:         |
| Carnival | :x: |        :x:         |
| Freeway | :heavy_check_mark: |        :x:         |
| Skiing | :heavy_check_mark: |        :x:         |
| Breakout | :heavy_check_mark: |        :x:         |
| Amidar | :heavy_check_mark: |        :x:         | 
| Tennis | :heavy_check_mark: |        :x:         |
| Pong | :heavy_check_mark: |        :x:         |
| Venture | :x: |        :x:         |
| Seaquest | :heavy_check_mark: |        :x:         |
| Frostbite | :heavy_check_mark: |        :x:         |
| Boxing | :heavy_check_mark: | :heavy_check_mark: |
| Space Invaders | :heavy_check_mark: |        :x:         |
| Galaxian | :x: |        :x:         |
| Atlantis | :heavy_check_mark: |        :x:         |
| Donkey Kong | :heavy_check_mark: |        :x:         |
| Double Dunk | :heavy_check_mark: |        :x:         |
| Montezuma Revenge | :heavy_check_mark: |        :x:         |

# Arcade Suite
This is the repo for our Bachelors project.
The goal of this project is to let agents play the modified [HackAtari](https://github.com/k4ntz/HackAtari) versions of Atari2600 
Games with the help of [OC_Atari](https://github.com/k4ntz/OC_Atari). We are going to implement PvP, PvE and EvE modes and visualize the decision making of Agents when they are playing using [ScoBots](https://github.com/k4ntz/SCoBots).

## Run Instructions
**WARNING only tested on Ubuntu for now. The "res" Directory will have to be created manually for now.** <br>
To run the app you will first have to clone at least the HackAtari submodule.
Then go into the HackAtari folder and run ```pip install -e .```. <br>
You will also have to install some dependencies with: <br>
```sudo apt install pkg-config libcairo2-dev gcc python3-dev libgirepository1.0-dev```. <br>
Then you can install the requirments with: <br>
```pip install -r requirments.txt``` <br>

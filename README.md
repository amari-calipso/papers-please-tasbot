# "Papers, Please" TASbot
A "Papers, Please" TASbot that offers a programmable interface with the game.

Huge thanks to HowToCantaloupe for helping throughout the development process, giving ideas, as well as offering information about the how the game is actually built, and, in general, providing a lot of knowledge about the game!

# Usage
Requires Python 3.11+ and the dependencies listed in `requirements.txt`. Run `main.py` to start the bot.

Run `build.py` to build an optimized version of the text recognition system, written in Cython. 

To build releases, pass the `--release` argument to `build.py`.

Note that using `build.py` requires the dependencies listed in `build_requirements.txt`

NOTE: this bot is currently only tested for Papers Please v1.1.67-S. it will NOT work for the latest version of the game.

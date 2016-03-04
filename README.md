# Tymeventure
A small adventure game I'm working on. Currently it's nothing big, but it will be. Eventually.

## How to install
You will need:
 - Python 3.4
 - Curses for Python 3.4
 - (Windows only) A terminal such as CygWin

Download the .zip of the game. In the future you really should go to the Releases tab, but there's not much here right now so you can go ahead and just download the latest commit.

Exctract it into a folder. Enter that folder, then run `python setup.py build`.<br>
After that, run `python setup.py install`. (On Linux/UNIX, you have to run with `sudo`.)<br>
Run `tymeventure` to play the game.

## Command-line Arguments

- `-h, --help`: Show help
- `-n, --name NAME`: Set your name
- `--nocolor`: Don't use colors
- `--nointro`: Skip the intro

## What's with the savegames?
The save automatically loads from the current directory - so wherever you launch Tymeventure from is your save directory.
To remove a save, delete the file labeled `YOURNAME_tymeventuresave`.
I reccomend making a save directory called `TymeventureSaves` and `cd`ing into that when you play.

## Where's the Wiki?
You can find the Tymeventure Wikia [here](https://tymeventure.wikia.com).
Currently there is no dev wiki - just the Wikia for gameplay.

## I have an old version installed. Do I need to uninstall it to update?
Nope! Just go through the installation instructions again and it'll automatically update.

## Uh, there's a problem!
Simply report an issue and I'll get to it.

## There was a problem but I fixed it now!
Make a pull request and I'll check it over. If it's good (as in it doesn't introduce more bugs or go against the goal of the project), then I'll add it in.

## I have an idea!
Suggest ideas on [the Scratch topic](https://scratch.mit.edu/discuss/topic/185267/).<br>
Alternatively, you can make a pull request and add your idea to IDEAS.md.

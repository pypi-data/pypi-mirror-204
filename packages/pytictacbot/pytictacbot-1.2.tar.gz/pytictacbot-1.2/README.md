# Tictacbot

A program that makes you unbeatable at [BombParty](https://jklm.fun/) (in french).

## Installation

⚠️ This program requires a version of **Python** >= 3 installed on your machine.

Install the [pytictacbot](https://pypi.org/project/pytictacbot/) module using *pip*:
```zsh
pip install pytictacbot
```

## Usage

*Note: this program will only work on MacOS since it uses "Command + V" keys to paste. You can edit the code yourself if you want to adapt it to your environment.*

In order for this program to work, you must allow "Accessibility" settings to the application that will run the script. Indeed, you need access to the input monitorig to listen to the keys you type.

- On your Mac, open *System settings*,
- Open the *Privacy & Security* section,
- Open the *Accessibility* section,
- Allow the application in which you will run the script (ex: iTerm).

Once this is done, it is ready to use !

In your terminal, run:
```zsh
tictacbot
```

An interface will be displayed. It will listen to the keys you type. A history of these keys will be displayed in the interface.

- To launch the search, **press the space bar**.
- To cancel the keys you typed, **press the escape key**. 

After a successful search, the found word will be automatically pasted. The "remaining letters" list will be updated accordingly.

## Rules

Before understanding how does it work, let's remember the rules of the bomb party :
- The player will be given a series of letters. He will then have to find (as quickly as possible) a word that contains this series of letters *(ex: "iso" -> "ma**iso**n")*
- The player starts with a list of all the letters in the alphabet. If, with the words he/she types during the game, the player manages to use all these letters at least once, then the player will gain an extra life.

Finally, the goal in each round would be to find a word containing the sequence of letters, but also the one that will unlock the most letters at once!

## How does it work ?

Once the script is launched, it will run in the background, listening to the keys that are typed on the keyboard.

It will display everything on the interface to make it easier for the user to understand what is happening in the background.

When the user will press escape to search the best word including the sequence of letters he/she typed, the *Tictacbot* will crawl a file containing all the words of the French language.

It will first determine a list of all words containing the given sequence of letters.
Then, it will crawl this list and, for each word, calculate a score using the letters to discover (cf. 2nd rule). It will finally return the word with the highest possible score.

Finally, it will erase the sequence of letters that has ben typed by the user and paste the word instead.
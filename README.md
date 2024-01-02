# operant-bot

a silly bot.

## Running the bot

1) Download the repository.
2) In the repository, open .env file and copy paste the following:
```
TOKEN = ''
```
3) In between the quotation marks, add the bot token.

## Current features
#### General
1) Use !hello to test that the bot is responding to commands.

#### Tort
1) Use the !tort command to open a game of tort. Users will be able to join the lobby by using !join and !leave to leave it. Use !restart to reset the lobby.
2) Use the !start command to begin a game of tort.
3) There are currently three levels, and three rounds of Tort. 
4) Users will be asked one question corresponding to each level, once per round. Each user will be asked one question. 
5) By default, questions cannot be repeated.
6) The question can be chosen, at which point the user has a maximum of 100 seconds to respond, or reshuffled an infinite number of times.

#### Changelog
1) Added basic functionality for the Tort game, including
    1. The game.py file, which currently contains the gameflow.
    2. The tort.py file, which currently allows the game to be opened and started using commands.
2) Deleted the original tort.py file and its test commands, which are now implemented in the game.py file
3) Games cannot be started if another game is already in progress.
4) Lobbies cannot be opened if another lobby is already open.

## Features to add
#### Tort
1) Command to exit the gameflow at any point.
2) Server is able to create custom question lists. 
    1. Question lists can be created for each game. This will also require automatically configuring the maximum number of rounds/levels to ensure that there will be enough questions for the entire game.
    2. Question lists can be saved for that server.
3) More customizability
    1. Ability to add a maximum number of reshuffles for the entire game
    2. Ability to vary timeout durations.
    3. Ability to create a larger number of levels or rounds.
    4. Ability to allow repeat questions.

#### General
1) Help command with list of commands.
2) Convert commands to embed message format (prettier).

#### For fun
1) Habit tracker with leaderboard functionality.

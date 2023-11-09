from discord.ext import commands
import json
import random

'''
Actions that have to do with manipulating questions in the questionbank. With attributes to keep
track of which questions have been chosen. A separate questionbank is used for every level of the
game. Mostly in case we want to add option to create custom levels and questionbanks in the future.
'''
class Questionbank():
    def __init__(self, file):
        self.questions = set(self.load_questions(file)) # Attribute for all questions
        self.used = set() # Attribute for used questions

    def load_questions(self, file, level: str): # Generate a list of questions corresponding to the level (preferably this 
        # would be integers but idk how to do that with json)
        with open(file, 'r') as f:
            data = json.load(f)
            level_questions = [str(item) for item in data['Levels'][level]['Questions']]

        return level_questions

    # Method to pick a question from the questionbank
    def pick_question(self):
        # Pick question from the set, but excluding the used questions
        q = random.choice(set(self.questions).difference(self.used))
        self.used.add(q)
        return q


'''
Wrapper to execute the logic flow of an entire game. 
'''
class Game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Number of players

        # Number of choices to give person (TBA)

        # Minimum level to start

        # Maximum level 

        # Number of questions per person per round

        # Number of rounds per level

        # Reshuffles allowed per player

    # Command to start the game
    @commands.command(name='start')
    async def start(self, ctx):
        pass
        # Display the current settings
        # Ask if any of the settings should be changed
        # Run the lobby until someone marks it as ready

        # In the future, add an option to have default server settings lmao

        # Play as many rounds as are specified

            # After round is played, send message

            # Update the number of rounds that have been played

        # End game and display message

    # Change settings

        # Specify the number of choices to give a person

        # Specify the minimum level to start at (default value = 1)

        # Specify the maximum level to reach (default value = 3)

        # Specify the number of questions per person per round (default value = 3)

            # Also display a maximum beyond which there wouldn't be enough questions

        # Specify the number of rounds per level
            
            # Also display a maximum beyond which there wouldn't be enough questions

        # Specify the number of reshuffles allowed per player

    # Play one level

        # Check level, generate question list from the unused questions of that level

        # While the number of rounds has not exceeded the number of rounds per level

            # For each player in the lobby

                # Play per player
                
        # Mark the level as over and update the level

    # Logic flow for a single person's turn
    async def play(self, ctx, questionbank, player):
        # Ask them a question and prompt them to respond (give list of commands)
        while turn_over != True:
            chosen_q = questionbank.pick_question()
            reshuffles = player.reshuffles() #TBA lol add under lobby class ....??? how to keep track of reshuffles for each player efficiently
            turn_over = False 
            await ctx.send(
                            f'''
                            Here's your question, {ctx.author.mention}: {chosen_q}
                            Reply with "accept" to accept the question, or "reshuffle" to pick a new one.
                            You have {reshuffles} left.
                            '''
                            )

            def check(msg, user):
                pass # TBA deal with user input in case user mistypes or smthing ALSO the message needs to time out 
                    # eventually and default to accept so use ayncio sleep at some point here
            
            # If reshuffle
                # Then we take the chosen question and we put that bad boy back in the unused questions list
                # Continue with the loop 
            # If accept then we don't do shit
                # Mark their turn as over to exit the loop
                turn_over == True
    
    # Check maximum number of questions based on current parameters assuming constant number of players, levels, and rounds or something like that idk
    def max_questions():
        pass
        

    # Command to end a game early
    @commands.command('end')
    async def end(self, ctx):
        pass

'''
A class to keep track of who is playing - ensures that each game is run for a group of players.
'''
class Lobby(commands.Cog):
    def __init__():
        pass
        # Add player attributes here

    # Add player to lobby
    @commands.command(name='join')
    async def join(self, ctx):
        pass

    # Delete player from lobby
    @commands.command(name='leave')
    async def leave(self, ctx):
        pass

    # Shuffle list of players (to change order)

    # Mark lobby as ready

    # Attempt to play (if there's error, won't start game)
    
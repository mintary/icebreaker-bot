import json
import random
import asyncio

'''
Actions that have to do with manipulating questions in the questionbank. With attributes to keep
track of which questions have been chosen. A separate questionbank is used for every level of the
game. Mostly in case we want to add option to create custom levels and questionbanks in the future.
'''
class Questionbank():
    def __init__(self, file, level:str):
        self.level = "Level " + level
        self.questions = set(self.load_questions(file)) # Attribute for all questions
        self.used = set() # Attribute for used questions
        self.ended = False

    def load_questions(self, file): # Generate a list of questions corresponding to the level, which is currently expressed in the format ('Level n')
        # TBA: method of storing the level data as an integer, not a string
        with open(file, 'r') as f:
            data = json.load(f)
            level_questions = [str(item) for item in data['Levels'][self.level]]

        return level_questions

    # Method to pick a question from the questionbank
    def pick_question(self):
        # Pick question from the set, but excluding the used questions
        unused_questions = list(set(self.questions).difference(self.used))
        q = random.choice(unused_questions)
        self.used.add(q)
        return q 
    
    # Method to add back a question that was picked, but now should be returned to the questionbank
    def add_back(self, question):
        try:
            self.used.remove(question)
            self.questions.add(question)
        except KeyError:
            print('Error: attempted to add back question that did not exist.')

'''
Wrapper to execute the logic flow of an entire game. 
'''
class Game():
    def __init__(self, bot, ctx, players, channel_id):
        # TBA Ability to update the number of levels, rounds, and set a timer via a command
        self.bot = bot
        self.ctx = ctx
        self.levels = 3
        self.rounds = 3
        self.players = players
        self.channel = self.bot.get_channel(channel_id)

    async def game(self):
        '''
        There are three levels in a Tort game, as well as three rounds. 

        Every player will be asked a question corresponding to the current level of the game.

        '''
        for level in range(1, self.levels + 1):
            questionbank = Questionbank("resources/questions.json", str(level))
            await self.ctx.send(f"Starting level {level} of {self.levels}.")

            for round in range(1, self.rounds + 1):
                await self.ctx.send(f"Round {round} of {self.rounds} has begun.")
                for player in self.players:
                    await self.play(questionbank, player)


    async def play(self, questionbank, player_id): # TBA: Functionality related to player argument. Allows for checking for player ID and number of reshuffles associated with them
        '''
        For a single person's turn. The player will be given a question picked from the
        questionbank. They will have the chance to accept or reshuffle it within 10 seconds. 
        If they choose to reshuffle, they will be asked a new question. If they choose the question,
        their turn is over. If they do not make a choice in time, their turn is skipped.
        '''
        # Ask them a question and prompt them to respond (give list of commands)
        turn_over = False
        while turn_over != True:
            chosen_q = questionbank.pick_question()
            # TBA: Ability to get the number of reshuffles associated with the player
            player_name = await self.bot.fetch_user(player_id)
            message = await self.ctx.send(f"Here's your question, {player_name}: {chosen_q} You can either accept, or reshuffle the question.") 
                 
            await message.add_reaction('✅')
            await message.add_reaction('❌')

            def check(reaction, user):
                return user.id == player_id and str(reaction.emoji) in ['✅', '❌']
            
            def check2(reaction, user):
                return user.id == player_id and str(reaction.emoji) == "👍"

            reaction, user = await self.bot.wait_for('reaction_add', check=check)  # Fixed the check condition
            if str(reaction.emoji) == '✅':  # Accept question. Mark turn as over and exit loop
                await message.edit(content = f"{player_name} accepted the question: {chosen_q} React with 👍 once you are done answering. ") 
                
                # Clean this code
                await message.add_reaction('👍')
                reaction_2, user_2 = await self.bot.wait_for('reaction_add', check=check2)
                if str(reaction_2.emoji) == '👍':
                    turn_over = True

                turn_over = True  
            elif str(reaction.emoji) == '❌':  # Reshuffle question. Continue with loop
                questionbank.add_back(chosen_q)
                await message.edit(content = f"{player_name} chose to reshuffle the question: {chosen_q}")



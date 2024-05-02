import asyncio
import sqlite3
from discord.ext import commands
from utils.questionbank import Questionbank

'''
Wrapper to execute the logic flow of an entire game. 
'''
class Game(commands.Cog):
    def __init__(self, bot, ctx, players, guild_id):
        # TBA Ability to update the number of levels, rounds, and set a timer via a command
        self.bot = bot
        self.ctx = ctx
        self.playing = True
        self.guild_id = guild_id
        self.levels = 3
        self.rounds = 3
        self.players = players

    async def game(self):
        '''
        There are three levels in a Tort game, as well as three rounds. 

        Every player will be asked a question corresponding to the current level of the game.

        '''
        db = sqlite3.connect('icebreaker.db')
        cur = db.cursor()

        query = "SELECT custom_q FROM settings WHERE guild_id = ?"
        cur.execute(query, (self.guild_id,))

        setting = cur.fetchone()[0]

        level = 1
        while (level <= self.levels and self.playing):
            questionbank = Questionbank(level, setting, self.guild_id)
            await self.ctx.send(f"Starting level {level} of {self.levels}.")

            for round in range(1, self.rounds + 1):
                if self.playing: await self.ctx.send(f"Round {round} of {self.rounds} has begun.")
                for player in self.players:
                    status = await self.play(questionbank, player)
                    if status == False: return
            level+=1

    async def play(self, questionbank, player_id): # TBA: Functionality related to player argument. Allows for checking for player ID and number of reshuffles associated with them
        '''
        For a single person's turn. The player will be given a question picked from the
        questionbank. They will have the chance to accept or reshuffle it within 10 seconds. 
        If they choose to reshuffle, they will be asked a new question. If they choose the question,
        their turn is over. If they do not make a choice in time, their turn is skipped.
        '''
        # Ask them a question and prompt them to respond (give list of commands)
        turn_over = False
        while turn_over != True and self.playing:
            chosen_q = questionbank.pick_question()
            if chosen_q == None:
                await self.ctx.send("No more unused questions. Ending turn early.")
                return True

            # TBA: Ability to get the number of reshuffles associated with the player
            player_name = await self.bot.fetch_user(player_id)
            message = await self.ctx.send(f"Here's your question, {player_name}: {chosen_q} You can either accept, or reshuffle the question, or end the game.") 
                 
            await message.add_reaction('✅')
            await message.add_reaction('❌')
            await message.add_reaction('🛑')

            def check(reaction, user):
                return user.id == player_id and str(reaction.emoji) in ['✅', '❌', '🛑'] # Provide option to end game early
            
            def check2(reaction, user):
                return user.id == player_id and str(reaction.emoji) in ['👍', '🛑']

            try: 
                reaction, user = await self.bot.wait_for('reaction_add', timeout=300.0, check=check)  # Fixed the check condition
                
                if str(reaction.emoji) == '✅':  
                    await message.edit(content = f"{player_name} accepted the question: {chosen_q} React with 👍 once you are done answering. ") 
                    
                    await message.add_reaction('👍')
                    await message.add_reaction('🛑')

                    try: 
                        reaction_2, user_2 = await self.bot.wait_for('reaction_add', timeout=300.0, check=check2)
                        if str(reaction_2.emoji) == '👍':
                            turn_over = True
                        elif str(reaction_2.emoji) == '🛑':
                            turn_over = True
                            self.playing = False
                            await message.channel.send("Game ended.")
                        
                    except asyncio.TimeoutError:
                        await message.channel.send("Timed out.")
                        turn_over = True
                    
                elif str(reaction.emoji) == '❌':  # Reshuffle question. Continue with loop
                    questionbank.add_back(chosen_q)
                    await message.edit(content = f"{player_name} chose to reshuffle the question: {chosen_q}")
                elif str(reaction.emoji) == '🛑':
                    turn_over = True
                    self.playing = False
                    await message.channel.send("Game ended.")
            except asyncio.TimeoutError:
                await message.channel.send("Timed out.")

            return self.playing
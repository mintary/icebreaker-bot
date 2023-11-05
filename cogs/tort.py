from discord.ext import commands
import json
import random

class Tort(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.questions = self.load_questions()
        self.used_questions = set()

    def load_questions(self):
        with open('questions.json', 'r') as f:
            data = json.load(f)
            list = [str(item) for item in data]
        return list

    @commands.command(name='tort_start')
    async def tort_start(self, ctx):
        await ctx.send('Started new tort game!')

    @commands.command(name='tort_end')
    async def tort_end(self, ctx):
        self.used_questions.clear()
        await ctx.send('Ended tort game.')
    
    @commands.command(name='tort_ask')
    async def tort_ask(self, ctx):
        if len(self.questions) == len(self.used_questions):
            await ctx.send('No more questions available!')
            return
        
        unused_questions = list(set(self.questions).difference(self.used_questions))
        selected_q = random.choice(unused_questions)
        self.used_questions.add(selected_q)

        await ctx.send(f'Question: {selected_q}')
    
async def setup(bot):
    await bot.add_cog(Tort(bot))

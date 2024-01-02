from discord.ext import commands
from game import Game

class Tort(commands.Cog):
    '''
    Tort class will contain commands that enable the user to open a game (allowing players to join the lobby) and
    also start a game. Contains four different commands: !join !leave !start !restart

    Will keep track of if the lobby is open and if there is currently a game in progress.
    '''
    def __init__(self, bot):
        self.bot = bot
        self.players = set() # Keep track of players who are playing
        self.open_lobby = False # Switch to true when a game begins
        self.playing = False # Switch to true when players are ready to play

    # Add player to lobby
    @commands.command(name='join')
    async def join(self, ctx):
        '''
        Command that allows players to join an existing game.
        '''
        if self.open_lobby:
            try:
                self.players.add(ctx.message.author.id)
                await ctx.send(f"{ctx.author.name} joined the lobby.")
            except ValueError:
                await ctx.send('You were unable to join the lobby.')
        else:
            await ctx.send("There is no game in progress.")

    # Delete player from lobby
    @commands.command(name='leave')
    async def leave(self, ctx):
        if self.open_lobby:
            try:
                self.players.remove(ctx.message.author.id)
                await ctx.send(f"{ctx.author.name} left the lobby.")
            except ValueError: # There are no people in the lobby.
                await ctx.send('You are not in the lobby, the game has already started, or there is no game in progress.')
        else:
            await ctx.send("There is no game in progress.")

    @commands.command(name='start')
    async def start(self, ctx):
        '''
        This command will be used to start the game.
        '''
        # Check that lobby is open and game is not already in progress.
        if self.open_lobby and self.playing == False:
            # Set attributes to playing state to prevent new game from being started.
            self.playing == True
            self.open_lobby == False

            # TBA: Ability to track multiple channels playing at once.
            channel_id = ctx.channel.id
            print(f"channel_id: {channel_id} now playing")

            # Create a new game with the added players
            new_game = Game(self.bot, ctx, self.players, channel_id)

            # Gameflow initiated
            await new_game.game()

            await ctx.send("Game over. Thanks for playing!")

            # Set playing status to false and close the lobby.
            self.playing = False
            self.open_lobby = False 

        elif self.playing:
            await ctx.send("Game is already in progress.")
        else:
            await ctx.send("Use !tort to start a new game.")

    # Open the lobby
    @commands.command(name='tort')
    async def tort(self, ctx):
        if self.open_lobby == False and self.playing == False:
            self.open_lobby = True
            self.players.add(ctx.message.author.id) 
            await ctx.send("Lobby is now open. Use !join to join or !leave to leave. Use !start to start the game.")
        else:
            await ctx.send("Game is already in progress.")
    
    # Reset the lobby. Should pay attention to how this command might interact with a command to stop the game while it is in progress.
    @commands.command(name="reset")
    async def reset(self, ctx):
        self.open_lobby = False
        self.playing = False
        self.players = set()
        await ctx.send("Lobby closed and game status set to not playing.")

async def setup(bot):
    await bot.add_cog(Tort(bot))
import discord
from discord.ext import commands
from discord import app_commands
import sqlite3

db = sqlite3.connect('icebreaker.db')
cur = db.cursor()
db.execute('''CREATE TABLE IF NOT EXISTS questions(
           interaction_id integer PRIMARY KEY, 
           level integer, 
           guild_id integer, 
           question_text text NOT NULL,
           FOREIGN KEY (guild_id) REFERENCES settings(guild_id))
           ''')

db.execute('''CREATE TABLE IF NOT EXISTS settings(
           guild_id integer PRIMARY KEY,
           custom_q text NOT NULL,
           FOREIGN KEY (guild_id) REFERENCES questions(guild_id)
           )
            ''')

db.commit()

class SettingsDropdown(discord.ui.Select):
    def __init__(self):
        options=[
            discord.SelectOption(label="custom", description="Custom questionbank for TorT. Associated commands: /add_q, /delete_q, /custom_q"),
            discord.SelectOption(label="default", description="Default questionbank for TorT."),
            discord.SelectOption(label="mixed", description="Mixes the custom and default questionbank. ")
        ]

        super().__init__(placeholder="TorT questionbank", options=options, min_values=1, max_values=1)

    def update_settings(self, guild_id: int, setting: str):
        query_check = "SELECT 1 FROM settings WHERE guild_id = ? LIMIT 1"
        cur.execute(query_check, (guild_id,))
        guild_exists = cur.fetchone()
        if guild_exists:
            query = "UPDATE settings SET custom_q = ? WHERE guild_id = ?"
            cur.execute(query, (setting, guild_id))
        else:
            query = "INSERT INTO settings VALUES (?, ?)"
            cur.execute(query, (guild_id, setting))
        db.commit()

    async def callback(self, interaction: discord.Interaction):
        self.update_settings(interaction.guild_id, self.values[0])
        await interaction.response.send_message(f"You chose the `{self.values[0]}` TorT questionbank.")
                                                
class SettingsView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(SettingsDropdown())

class Custom(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def q_exists(self, question): 
        query_check = "SELECT 1 FROM questions WHERE question_text = ? LIMIT 1"
        cur.execute(query_check, (question,))
        record_exists = cur.fetchone()
        return record_exists

    @app_commands.command(name='add_q', description="Adds a new question to the custom questionbank, or updates level.")
    async def add_q(self, interaction: discord.Interaction, question : str, level : int):
        if level > 3 or level < 1:
            await interaction.response.send_message(content="Only levels between 1 - 3 are currently supported.")
        elif self.q_exists(question):
            query = "UPDATE questions SET level = ? WHERE question_text = ?"
            cur.execute(query, (level, question))
            db.commit()
            await interaction.response.send_message(content="Question already exists, only level was updated.")
        else:
            query = "INSERT INTO questions VALUES (?, ?, ?, ?)"
            cur.execute(query, (interaction.id, level, interaction.guild_id, question))
            db.commit()
            await interaction.response.send_message(content="Question written into database.")

    @app_commands.command(name='delete_q', description="Deletes question from questionbank.")
    async def delete_q(self, interaction: discord.Interaction, question : str):
        if self.q_exists(question):
            query_del = "DELETE FROM questions WHERE question_text = ?"
            cur.execute(query_del, (question,))
            db.commit()
            await interaction.response.send_message(content="Question deleted from database.")
        else:
            await interaction.response.send_message(content="Question not found in database.")

    @app_commands.command(name='view_custom', description="Show custom questionbank for this guild.")
    async def view_custom(self, interaction: discord.Interaction):
        cur_guild_id = interaction.guild_id
        query = "SELECT * FROM questions WHERE guild_id = ?"
        data = cur.execute(query, (cur_guild_id,)).fetchall()

        questions_by_level = {
            1: [],
            2: [],
            3: []
        }

        for row in data:
            level = row[1]
            question = row[3]
            questions_by_level[level].append(question)

        message = ""
        for level, questions in questions_by_level.items():
            message += f"Level {level} questions:\n"
            for question in questions:
                message += f"✰ {question}\n"
            message += "\n"
        
        await interaction.response.send_message(content=message)
    
    @app_commands.command(name='settings', description="Update server settings.")
    async def settings(self, interaction: discord.Interaction):
        await interaction.response.send_message("Use the dropdown menu to change guild settings.", view=SettingsView())

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Custom(bot))
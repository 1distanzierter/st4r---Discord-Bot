import discord
import random
import json
import asyncio

from datetime import datetime
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice

with open('./config.json') as cjson:
    config = json.load(cjson)


class clear(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="clear",
        description="Delete Messages")
    
    @app_commands.describe(
        amount="How much messages you want to delete",
    )

    async def clear(self, interaction: discord.Interaction, amount: int) -> None:
       
       with open("permissions/moderationperms.txt", "r") as f:
        permslist = f.read().split("\n")

        if interaction.user.name in permslist:
           
           await interaction.response.send_message(f'> **Deleted __{amount}__ messages**', ephemeral=True)
           await interaction.channel.purge(limit=amount)
           

        else:
            embed = discord.Embed(title="",
                                  description="You dont have permissions to use this command!",
                                  color=0xfffb00)
            embed.set_author(name="No Permissions", icon_url=f'{config["IconURL"]}')
            embed.set_footer(text=interaction.user.name, icon_url=interaction.user.avatar.url)
            embed.timestamp = datetime.utcnow()
            await interaction.response.send_message(embed=embed)
            


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        clear(bot),
        guilds=[discord.Object(config["GuildID"])]
    )
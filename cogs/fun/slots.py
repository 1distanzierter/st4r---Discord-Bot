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


class slots(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="slots",
        description="Delete Messages")
    
    @app_commands.describe(
        amount="How much messages you want to delete",
    )

    async def slot(self, interaction: discord.Interaction, ) -> None:

        print("Test")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        slots(bot),
        guilds=[discord.Object(config["GuildID"])]
    )
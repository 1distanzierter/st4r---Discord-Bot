import discord
import random
import json
import asyncio
import uuid

from datetime import datetime
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice

with open('./config.json') as cjson:
    config = json.load(cjson)


class avatar(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="avatar",
        description="Change your Bots Avatar (Owner Only)")
    
    @app_commands.describe(
        image="Select or Avatar (PNG,JPG, GIF)",
    )
    
    async def avatard(self, interaction: discord.Interaction, image: discord.Attachment) -> None:


        if interaction.user.id == config["BotOwner"]:
           
           await self.bot.user.edit(avatar=await image.read())

           await interaction.response.send_message("Avatar changed!", file=image.to_file())

        else:
            #The Error Message
            errorembed = discord.Embed(title="",
                                   description="You dont have enough permissions to run this command!",
                                   color=0xfffb00)
            errorembed.set_author(name="Error", icon_url=config["IconURL"])
            errorembed.set_footer(text=interaction.user.name, icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(interaction.user.mention, embed=errorembed)

        


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        avatar(bot),
        guilds=[discord.Object(config["GuildID"])]
    )
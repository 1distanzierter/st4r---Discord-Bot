import discord
import random
import json
import time as pyTime

from datetime import datetime
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice

with open('./config.json') as cjson:
    config = json.load(cjson)


class gtn(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="guessthenumbers",
        description="An Minigame who the members have to guess a random number maybe to win a prize")
    
    @app_commands.describe(
        number="which number should the members guess?",
        time="Time to guess the number (in seconds)",
        price="name a price that the right guesser will get"
    )
    async def gtn(self, interaction: discord.Interaction, number: int, time: int, price: str) -> None:

        NoPerm = discord.Embed(title="",
                       description="you dont have enought permissions to use this command!",
                       color=0xfffb00)
        NoPerm.set_author(name="❌ No Permissions ❌", icon_url=config["IconURL"])
        NoPerm.set_footer(text=interaction.user.name, icon_url=interaction.user.avatar.url)
        NoPerm.timestamp = datetime.utcnow()
        BotPermsRole = interaction.guild.get_role(config["BotPermsRoleID"])

        timeleft = pyTime.time() + time

        if BotPermsRole in interaction.user.roles:
            gtnembed = discord.Embed(title="",
                                     description=f"> **You have __{time}__ seconds time to guess a number.**\n> **The person who guess the number get a prize!**\n\n> **The number has __{len(str(number))}__ digit(s).**\n> **Prize: __{price}__!**\n> **Guessing ends:** <t:{int(timeleft)}:R>",
                                     color=0xfffb00)
            gtnembed.set_author(name="Guess the Number 💭", icon_url=config["IconURL"])
            gtnembed.set_footer(text=interaction.user.name, icon_url=interaction.user.avatar.url)
            gtnembed.timestamp = datetime.utcnow()
            await interaction.response.send_message(f"The number is ||{number}|| btw 😉", ephemeral=True)
            await interaction.channel.send(embed=gtnembed)
            msgs = 0
            while True:
                msg = await self.bot.wait_for("message")
                msgs + 1
                if int(msg.content) == number:
                    await interaction.channel.send(embed=discord.Embed(title="",
                                                                    description=f"> **%user% guessed the right number! 🎉**\n> **The number was: __%number%__**".replace("%user%", msg.author.mention).replace("%number%", str(number)),
                                                                    color=0xfffb00))
                    await msg.author.send(embed=discord.Embed(title="",
                                                                    description=f"> **You guessed the right number! 🎉**\n> **Please open a <#1094379285583761448> to claim your prize!**",
                                                                    color=0xfffb00))
                    break
                if pyTime.time() >= timeleft:
                    await interaction.channel.send(embed=discord.Embed(title="",
                                                                       description=f"> **The time is over!** **\n> Nobody guesses the right number 😐**\n\n **> The number was: __{number}__**",
                                                                       color=0xfffb00))
                    break
        
        else:
            await interaction.response.send_message(interaction.user.mention, embed=NoPerm)

        


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        gtn(bot),
        guilds=[discord.Object(config["GuildID"])]
    )
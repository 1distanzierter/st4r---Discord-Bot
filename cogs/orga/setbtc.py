import discord
import random
import json

from datetime import datetime
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice

with open('./config.json') as cjson:
    config = json.load(cjson)


class setbtcchannel(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="setbitcoinchannel",
        description="Set the channel where the Bitcoin price will be send all 15 minutes")
    
    @app_commands.describe(
        channel="select your channel"
    )

    async def setbitcoinchannel(self, interaction: discord.Interaction, channel: discord.TextChannel) -> None:

        NoPerm = discord.Embed(title="",
                       description="you dont have enought permissions to use this command!",
                       color=0xfffb00)
        NoPerm.set_author(name="❌ No Permissions ❌", icon_url=config["IconURL"])
        NoPerm.set_footer(text=interaction.user.name, icon_url=interaction.user.avatar.url)
        NoPerm.timestamp = datetime.utcnow()
        

        if interaction.user.id == config["BotOwner"]:

            embed = discord.Embed(
                title="",
                description=f"The Bitcoin price message will now send to {channel.mention}",
                color=0xfffb00
            )
            embed.set_author(name="Bitcoin Channel changed", icon_url=f'{config["IconURL"]}')
            embed.set_footer(text="coded by artur454", icon_url=f'{config["IconURL"]}')
            embed.timestamp = datetime.utcnow()

            await interaction.response.send_message(embed=embed)

            embed2 = discord.Embed(
                title="",
                description=f"{interaction.user.mention} ({interaction.user.id}) changed the Bitcoin Channel to {channel.mention}({channel.id})",
                color=0xfffb00
            )
            embed2.set_author(name="st4r Bitcoin Logs", icon_url=f'{config["IconURL"]}')
            embed2.set_footer(text=interaction.user.name, icon_url=interaction.user.avatar.url)
            embed2.timestamp = datetime.utcnow()
            LogChannel = self.bot.get_channel(config["Log Channel"])
            await LogChannel.send(embed=embed2)

            config["BTC Channel"] = channel.id       
            with open("./config.json", "w") as gaylord:
                json.dump(config, gaylord, indent=4)
        else:
            await interaction.response.send_message(interaction.user.mention, embed=NoPerm
                                                    )

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        setbtcchannel(bot),
        guilds=[discord.Object(config["GuildID"])]
    )
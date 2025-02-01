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


class userinfo(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="userinfo",
        description="get info about a user or about yourself")
    
    @app_commands.describe(
        user="The Member you want informations about"
    )
    async def userinfo(self, interaction: discord.Interaction, user: discord.Member = None) -> None:

        if user == None:
            user = interaction.user
        
        if user.bot == False:
            bot_status = "`❌`"
        else:
            bot_status = "`✔`"

        if user.nick == None:
            user_nick = user.name
        else:
            user_nick = user.nick

        embed = discord.Embed(title="",
                            description=f"• **User:** {user.mention}\n"+
                                        f"• **Username:** `{user.name}`\n" + 
                                        f"• **UserID:** `{user.id}`\n" + 
                                        f"• **Nickname: ** `{user_nick}`\n" +
                                        f"• **Bot:** {bot_status}\n" +
                                        "• **Account createt at: ** `" + user.created_at.strftime("%d %B %Y") + "`\n" +
                                        f"• **Joined at: ** `" + user.joined_at.strftime("%d %B %Y") + "`\n",
                            color=0xfffb00)
            

        
        embed.add_field(name=f"Roles", value=f"{', '.join([role.mention for role in user.roles])}", inline=True)
        embed.set_author(name=f"Userinfo about {user.name}", icon_url=user.avatar.url)
        embed.set_footer(text=interaction.user.name, icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)

        


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        userinfo(bot),
        guilds=[discord.Object(config["GuildID"])]
    )
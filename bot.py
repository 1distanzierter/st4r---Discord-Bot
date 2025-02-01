from typing import Optional
import discord
from discord import *
from pystyle import Colors, Colorate, Center
from discord.ext import commands
from colorama import *
import aiohttp
import json
import time
import requests
import datetime
import asyncio
import random
import io
import os


with open('./config.json') as cjson:
    config = json.load(cjson)

logo =(
    """
    
  .-')   .-') _          _  .-')   
 ( OO ).(  OO) )        ( \( -O )  
(_)---\_/     '._  .---. ,------.  
/    _ ||'--...__)/ .  | |   /`. ' 
\  :` `.'--.  .--/ /|  | |  /  | | 
 '..`''.)  |  | / / |  |_|  |_.' | 
.-._)   \  |  |/  '-'    |  .  '.' 
\       /  |  |`----|  |-|  |\  \  
 `-----'   `--'     `--' `--' '--' 

    """)

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=config["Prefix"],
            intents=discord.Intents.all(),
            application_id=config["Bot_Application_ID"]
        )


        self.initial_extensions = [
            "cogs.orga.setbtc",
            "cogs.moderation.clear",
            "cogs.fun.gtn",
            "cogs.admin.gen_key",
            "cogs.everyone.userinfo",
            "cogs.admin.avatar",
        ]

    async def setup_hook(self):
        self.session = aiohttp.ClientSession()
        for ext in self.initial_extensions:
            await self.load_extension(ext)

    async def close(self):
        await super().close()
        await self.session.close()

    async def on_ready(self):
        print(Colorate.Horizontal(Colors.yellow_to_red, logo, 1))
        
        print(Fore.LIGHTGREEN_EX + f"Bot{Fore.LIGHTWHITE_EX}({self.user}) {Fore.LIGHTGREEN_EX} has connected to Discord!")
        await bot.change_presence(activity=discord.CustomActivity(name="⭐"), status=discord.Status.idle)
        try:
            await self.tree.sync(guild=discord.Object(config["GuildID"]))

            print(f'{Fore.LIGHTGREEN_EX}Synced Slash Commands')
        except Exception as e:
            print(e)
        
        await ticketmessage()
        await verifymessage()
        await bitcoin()

    async def on_member_join(self, member: discord.Member):
        WelcomeChannel = bot.get_channel(config["WelcomeChannel"])
        guildd = bot.get_guild(config["GuildID"])
        MemberChannel = bot.get_channel(1152705852193636483)
        ROLE = guildd.get_role(1151973062166720613)

        embed= discord.Embed(title="",
                             description=f'Welcome, {member.mention}! You can verify in <#{config["VerifyChannel"]}>',
                             color=0xfffb00)
        embed.set_author(name="Welcome 👋🏻", icon_url=f'{config["IconURL"]}')
        embed.set_footer(text="coded by artur454", icon_url=f'{config["IconURL"]}')
        embed.timestamp = datetime.datetime.utcnow()
        await WelcomeChannel.send(embed=embed)
        await member.add_roles(ROLE)
        await MemberChannel.edit(name=f"👥・Members: {guildd.member_count}")

    async def on_member_leave(self, member: discord.Member):
        WelcomeChannel = bot.get_channel(config["WelcomeChannel"])
        guildd = bot.get_guild(config["GuildID"])
        MemberChannel = bot.get_channel(1152705852193636483)
        ROLE = guildd.get_role(1151973062166720613)

        embed= discord.Embed(title="",
                             description=f'Bye Bye, {member.mention}! We wish you a good time ',
                             color=0xfffb00)
        embed.set_author(name="Bye Bye 👋🏻", icon_url=f'{config["IconURL"]}')
        embed.set_footer(text="coded by artur454", icon_url=f'{config["IconURL"]}')
        embed.timestamp = datetime.datetime.utcnow()
        await WelcomeChannel.send(embed=embed)
        await MemberChannel.edit(name=f"👥・Members: {guildd.member_count}")

class Dropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label='General question ticket', description='Open a General question ticket', emoji='🎫'),
            discord.SelectOption(label='Shop ticket', description='Open a Shop ticket', emoji='💸'),
            discord.SelectOption(label='Team apply ticket', description='Open a ticket for a team apply', emoji='👷🏻‍♂️')
        ]

        super().__init__(placeholder='Which ticket do you want to open?', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        guild = bot.get_guild(interaction.guild.id)
        creator = interaction.user
        if self.values[0] == "Shop ticket":
            checkchannel = discord.utils.get(guild.channels, name=f"shop-{interaction.user.name}")
            if not checkchannel:
                await interaction.response.send_message(f'Your {self.values[0]} will be open soon', ephemeral=True)

            else:
                await interaction.response.send_message(f'You already have a open {self.values[0]}!', ephemeral=True)
        elif self.values[0] == "General question ticket":
            checkchannel = discord.utils.get(guild.channels, name=f"questions-{interaction.user.name}")
            if not checkchannel:
                await interaction.response.send_message(f'Your {self.values[0]} will be open soon', ephemeral=True)

            else:
                await interaction.response.send_message(f'You already have a open {self.values[0]}!', ephemeral=True)
        elif self.values[0] == "Team apply ticket":
            checkchannel = discord.utils.get(guild.channels, name=f"teamapply-{interaction.user.name}")
            if not checkchannel:
                await interaction.response.send_message(f'Your {self.values[0]} will be open soon', ephemeral=True)

            else:
                await interaction.response.send_message(f'You already have a open {self.values[0]}!', ephemeral=True)



        class CloseDropdown(discord.ui.Select):
            def __init__(self):
                options = [
                    discord.SelectOption(label='Close ticket', description='Close the ticket',
                                         emoji='🔒'),
                    discord.SelectOption(label="Reopen ticket", description='Reopen the ticket', emoji="🔓"),

                    discord.SelectOption(label="Delete ticket", description='Delete the ticket', emoji="❌")


                ]

                super().__init__(placeholder='Here you can close the ticket', min_values=1, max_values=1,
                                 options=options)

            async def callback(self, interaction: discord.Interaction):

                if self.values[0] == "Close ticket":

                    if channel.category.id == 1175832487964979270:
                        await interaction.response.send_message('The ticket is already closed', ephemeral=True)
                    else:
                        await interaction.response.send_message(f'The ticket will be closed soon', ephemeral=True)
                        await asyncio.sleep(5)
                        await channel.set_permissions(creator, send_messages=False, read_messages=False, add_reactions=True,
                                                embed_links=True, attach_files=True, read_message_history=True,
                                                external_emojis=True, manage_channels=True)
                        await channel.edit(category=bot.get_channel(1175832487964979270))

                if self.values[0] == "Close ticket":

                    if channel.category.id != 1175832487964979270:
                        await interaction.response.send_message('The ticket is already open', ephemeral=True)
                    else:
                        await interaction.response.send_message(f'Reopening the ticket...', ephemeral=True)
                        await asyncio.sleep(5)
                        await channel.set_permissions(creator, send_messages=True, read_messages=True, add_reactions=True,
                                                embed_links=True, attach_files=True, read_message_history=True,
                                                external_emojis=True, manage_channels=True)
                        await channel.edit(category=bot.get_channel(1175832487964979270))


                if self.values[0] == "Delete ticket":
                    role = guild.get_role(1175827550677774408)
                    if role in interaction.user.roles:
                        await interaction.response.send_message("Ticket will be deleted")
                        transcriptchannel = bot.get_channel(1113042008643215382)

                        transcript = await chat_exporter.export(
                            channel,
                            limit=None,
                            bot=bot,
                            tz_info="Europe/Berlin"
                            )

                        file = discord.File(
                            io.BytesIO(transcript.encode()),
                            filename=f"{channel}-transcript.html"
                        )
                        file1 = discord.File(
                            io.BytesIO(transcript.encode()),
                            filename=f"{channel}-transcript.html"
                        )

                        await transcriptchannel.send(file=file)
                        await creator.send(file=file1)
                        await asyncio.sleep(5)
                        await channel.delete()
                    else:
                        await interaction.response.send_message('You dont have permissions to delete a ticket', ephemeral=True)

        class CloseDropdownView(discord.ui.View):
            def __init__(self):
                super().__init__()

                self.add_item(CloseDropdown())

        view = CloseDropdownView()

        if self.values[0] == "General question ticket":
            checkchannel = discord.utils.get(guild.channels, name=f"questions-{interaction.user.name}")
            if not checkchannel:

                channel = await guild.create_text_channel(name=f"questions-{interaction.user.name}",
                                                        category=bot.get_channel(1175827355583926352))

                rolesearch = discord.utils.get(guild.roles, id=1175827550677774408)

                await channel.set_permissions(interaction.user, send_messages=True, read_messages=True, add_reactions=True,
                                            embed_links=True, attach_files=True, read_message_history=True,
                                            external_emojis=True, manage_channels=True)

                await channel.set_permissions(rolesearch, send_messages=True, read_messages=True, add_reactions=True,
                                            embed_links=True, attach_files=True, read_message_history=True,
                                            external_emojis=True, manage_channels=True)

                await channel.set_permissions(guild.default_role, send_messages=False, read_messages=False)

                embed = discord.Embed(title='',
                                    description=f'Hello, {interaction.user.mention}!' + '\n'
                                    + '\n' + 'tell us your question and one of the *st4r team* will be answer your question!',
                                    color=0xfffb00)
                embed.set_author(name='st4r ・ Ticket System',
                                icon_url=f'{config["IconURL"]}')
                embed.set_thumbnail(url=f'{config["IconURL"]}')
                embed.set_footer(text=interaction.user.name, icon_url=interaction.user.avatar.url)
                embed.timestamp = datetime.datetime.utcnow()

                await channel.send('<@&1175827550677774408>', embed=embed, view=view)

        elif self.values[0] == "Shop ticket":
            checkchannel = discord.utils.get(guild.channels, name=f"shop-{interaction.user.name}")
            if not checkchannel:
                channel = await guild.create_text_channel(name=f"shop-{interaction.user.name}",
                                                        category=bot.get_channel(1175827417550553188))

                rolesearch = discord.utils.get(guild.roles, id=1175827550677774408)

                await channel.set_permissions(interaction.user, send_messages=True, read_messages=True, add_reactions=True,
                                            embed_links=True, attach_files=True, read_message_history=True,
                                            external_emojis=True, manage_channels=True)

                await channel.set_permissions(rolesearch, send_messages=True, read_messages=True, add_reactions=True,
                                            embed_links=True, attach_files=True, read_message_history=True,
                                            external_emojis=True, manage_channels=True)

                await channel.set_permissions(guild.default_role, send_messages=False, read_messages=False)

                embed = discord.Embed(title='',
                                    description=f'Hello, {interaction.user.mention}!' + '\n'
                                                + '\n' + 'Please answer the questions' + '\n' + '\n' + '1. What do you want to buy?' + '\n' + '2. How much do you want to buy?' + '\n' + '3. Which payment method do you want to pay with?',
                                    color=0xfffb00)
                embed.set_author(name='st4r ・ Ticket System',
                                icon_url=f'{config["IconURL"]}')
                embed.set_thumbnail(
                    url=f'{config["IconURL"]}')
                embed.set_footer(text=interaction.user.name, icon_url=interaction.user.avatar.url)
                embed.timestamp = datetime.datetime.utcnow()

                await channel.send('<@&1175827550677774408>', embed=embed, view=view)

        elif self.values[0] == "Team apply ticket":
            checkchannel = discord.utils.get(guild.channels, name=f"teamapply-{interaction.user.name}")
            if not checkchannel:
                channel = await guild.create_text_channel(name=f"teamapply-{interaction.user.name}",
                                                        category=bot.get_channel(1175827470377828432))

                rolesearch = discord.utils.get(guild.roles, id=1175827550677774408)

                await channel.set_permissions(interaction.user, send_messages=True, read_messages=True, add_reactions=True,
                                            embed_links=True, attach_files=True, read_message_history=True,
                                            external_emojis=True, manage_channels=True)

                await channel.set_permissions(rolesearch, send_messages=True, read_messages=True, add_reactions=True,
                                            embed_links=True, attach_files=True, read_message_history=True,
                                            external_emojis=True, manage_channels=True)

                await channel.set_permissions(guild.default_role, send_messages=False, read_messages=False)

                embed = discord.Embed(title='',
                                    description=f'Hello, {interaction.user.mention}!' + '\n'
                                                + '\n' + 'Please send your apply in this channel',
                                    color=0xfffb00)
                embed.set_author(name='st4r ・ Ticket System',
                                icon_url=f'{config["IconURL"]}')
                embed.set_thumbnail(
                    url=f'{config["IconURL"]}')
                embed.set_footer(text=interaction.user.name, icon_url=interaction.user.avatar.url)
                embed.timestamp = datetime.datetime.utcnow()

                await channel.send('<@&1175827550677774408>', embed=embed, view=view)

class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(Dropdown())


async def ticketmessage():

    embed = discord.Embed(title="",
                        description="Open a ticket with the Menu :)",
                        color=0xfffb00)
    embed.set_author(name="Ticket Support", icon_url=f'{config["IconURL"]}')
    embed.set_footer(text="coded by artur454", icon_url=f'{config["IconURL"]}')
    embed.timestamp = datetime.datetime.utcnow()
    view = DropdownView()
    TicketChannel = bot.get_channel(1094379285583761448)
    await TicketChannel.purge(limit=2)
    await TicketChannel.send(embed=embed, view=view)


class VerifyButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Verify!", style=discord.ButtonStyle.green, emoji="✅")
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        VerifyRole = discord.utils.get(interaction.guild.roles, id=config["VerifyRoleID"])
        embed = discord.Embed(title="",
                              description=f"The role <@&{VerifyRole.id}> was added successfully!",
                              color=0xfffb00)
        await interaction.user.add_roles(VerifyRole)
        await asyncio.sleep(0.5)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        


async def verifymessage():

    embed = discord.Embed(title="",
                        description="Click on the Button to see the whole Discord",
                        color=0xfffb00)
    embed.set_author(name="Verify", icon_url=f'{config["IconURL"]}')
    embed.set_footer(text="coded by artur454", icon_url=f'{config["IconURL"]}')
    embed.timestamp = datetime.datetime.utcnow()

    VerifyChannel = bot.get_channel(config["VerifyChannel"])
    await VerifyChannel.purge(limit=2)
    await VerifyChannel.send(embed=embed, view=VerifyButton())



async def bitcoin():
        while True:

            with open("./config.json", "r") as gay:
                btc = json.load(gay)

            bitcoin = requests.get('https://blockchain.info/ticker').json()
            channel = bot.get_channel(btc["BTC Channel"])

            embed = discord.Embed(title="",
                                description="These are the Bitcoin prices at the moment",
                                color=0xfffb00)
            embed.set_footer(text="coded by artur454", icon_url=f'{config["IconURL"]}')
            embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Bitcoin.svg/800px-Bitcoin.svg.png")
            embed.set_author(name="Bitcoin Price", icon_url=f'{config["IconURL"]}')
            embed.timestamp = datetime.datetime.utcnow()
            embed.add_field(name="EUR (€)", value=f'{bitcoin["EUR"]["last"]}€')
            embed.add_field(name="USD ($)", value=f'{bitcoin["USD"]["last"]}$')

            await channel.send(embed=embed)
            await asyncio.sleep(15*60)

bot = Bot()
bot.run(config["Token"])

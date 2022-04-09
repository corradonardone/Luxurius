import discord
import os
import json
from discord.ext import commands
from discord.ui import *

from cogs.Information import Information

print("======================")
print("Il bot si sta avviando...")

def get_prefix(bot, message):
    with open('json/prefixes.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

token = "OTU4ODIzMDcxNzAyMTg4MDQy.YkS7kg.95XHEPMBV4YruJxxQrCXj44QnF0"
intents = discord.Intents().all()
bot = commands.Bot(command_prefix=get_prefix, intents=intents)
bot.remove_command('help')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

@bot.event
async def on_ready():
    await bot.change_presence(status = discord.Status.online, activity=discord.Game("Use help command to view all list of my commands"))
    print(bot.user, "si è appena avviato!")
    print('=========================')

@bot.event
async def on_guild_join(guild):
    with open('json/prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = '.'
    with open('json/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@bot.event
async def on_guild_remove(guild):
    with open('json/prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes.pop(str(guild.id))
    with open('json/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@bot.slash_command(name='changeprefix', description='Change my command prefix', pass_context=True)
@commands.has_permissions(administrator=True)
async def changeprefix(ctx, prefix):
    with open('json/prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(ctx.guild.id)] = prefix
    with open('json/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    embed1=discord.Embed(title="New Prefix", color=0x14f910)
    embed1.add_field(name="My new prefix is:", value=f"{prefix}", inline=True)
    await ctx.send(embed=embed1)
    name=f'{prefix}BotBot'
    
class DropDownMenu(discord.ui.View):
    @discord.ui.select(placeholder="Choose a category", min_values=1, max_values=1, options=[
        discord.SelectOption(label="Information", description="View information commands", emoji="🔍"),
        discord.SelectOption(label="Moderation", description="View moderation commands", emoji="🤖"),
        discord.SelectOption(label="Levelling", description="View levelling command", emoji="💹"),
    ])
    async def callback(self, select, interaction: discord.Interaction):
        if select.values[0] == "Information":
            infoembedmess = """
```profileinfo```: View the member information
```serverinfo```: View the server information
```avatar```: View the avatar of a user
            """
            infoembed = discord.Embed(
                title="Information",
                description="Information commands list:",
                color=0x21f312
            )
            infoembed.add_field(name=infoembedmess, value="\u200b")
            await interaction.response.send_message(embed=infoembed, ephemeral=True)
        if select.values[0] == "Moderation":
            await interaction.response.send_message("Coming soon...", ephemeral=True)
        if select.values[0] == "Levelling":
            levellingembedmess = """
```rank```: View user rank
```leaderboard```: View the server leaderboard
```card```: Select your card background (use number from 1 to 6)
```color```: Select your rank card text color
            """
            levellingembed = discord.Embed(
                title="Levelling",
                description="Levelling commands list:",
                color=0x21f312
            )
            levellingembed.add_field(name=levellingembedmess, value="\u200b")
            await interaction.response.send_message(embed=levellingembed, ephemeral=True)

@bot.command(name="help")
async def help(ctx):
    embed = discord.Embed(
        title="Choose an option!",
        colour=0x21f312
    )
    dropdowns=DropDownMenu()
    await ctx.send(embed=embed, view=dropdowns)

bot.run(token)


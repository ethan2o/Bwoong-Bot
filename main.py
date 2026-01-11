import discord
import os
from dotenv import load_dotenv
import random
from discord import app_commands
from discord.ext import commands

import patch
import bot_commands

last_roll = set()
    
if __name__ == "__main__":
    bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
    
    load_dotenv()
    BOT_TOKEN = os.getenv("DISCORD_API_KEY")
    data = patch.Patch_Data()

@bot.event
async def on_ready():
    
    print(f"{bot.user} is now running")
    
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


@bot.tree.command(name="roll_champs", description="Create a grid of n champions")
@app_commands.describe(n="number of champions", ignore_previous="Allow previous champions to be rerolled")
async def roll_champs(interaction: discord.Interaction, n: int=1, ignore_previous: bool=False):
    global last_roll
    
    if ignore_previous:
        last_roll = set()
            
    champions = bot_commands.random_champions(data.CHAMPIONS, n, last_roll)
    last_roll.update(champions)
    
    # WUKONG Exception (listed as MonkeyKing in game files)
    if "MonkeyKing" in champions:
        champions.remove("MonkeyKing")
        champions.add("Wukong")
    
        # sort champion list before making grid
        champions = sorted(list(champions))
        
        # WUKONG Exception replace Wukong back with MonkeyKing
        champions = ["MonkeyKing" if champion == "Wukong" else champion for champion in champions]
    else:
        champions = sorted(list(champions))
    
    await interaction.response.defer(thinking=True)
    
    result = bot_commands.create_grid(champions)
    
    if not result:
        await interaction.followup.send("Error")
    else:
        await interaction.followup.send(file=discord.File("grid.png"))
        
        
@bot.tree.command(name="random_user", description="Get random user(s) in the voice channel you are connected to")
@app_commands.describe(n="Number of users to select")
async def random_user(interaction: discord.Interaction, n: int = 1):
    # check if user is connected to a voice channel
    if not interaction.user.voice or not interaction.user.voice.channel:
        await interaction.response.send_message("You are not connected to a voice channel.", ephemeral=True)
        return

    members = [member for member in interaction.user.voice.channel.members if not member.bot]

    if not members:
        await interaction.response.send_message("No users found in the voice channel.", ephemeral=True)
        return

    # clamp n so it doesn't exceed number of members
    n = min(n, len(members))

    selected = random.sample(members, n)
    mentions = " ".join(member.mention for member in selected)

    await interaction.response.send_message(f"{mentions}")
    
bot.run(BOT_TOKEN)
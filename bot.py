import discord
import asyncio
import os
from dotenv import load_dotenv
from discord.ext import commands
from logger import Logger
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='$', intents=intents)
logger = Logger();

@bot.event
async def on_ready():
    logger.log(f'Logged in as {bot.user.name} ({bot.user.id})')
    logger.log('------')
    for guild in bot.guilds:
        role = discord.utils.get(guild.roles, name='notifications')
        if role:
            logger.log(f'Role "notifications" found in guild {guild.name}')
        else:
            logger.error(f'Role "notifications" not found in guild {guild.name}')

        channel = discord.utils.get(guild.text_channels, name='notifications')
        if channel:
            logger.log(f'Text channel "notifications" found in guild {guild.name}')
        else:
            logger.error(f'Text channel "notifications" not found in guild {guild.name}')

@bot.event 
async def on_message(message):
    logger.log(message.author.name + '@' + message.guild.name + ": " + message.content)

    if message.author == bot.user: 
        return
    
@bot.event
async def on_voice_state_update(member, before, after):
    # Check if the user joined a voice channel
    if before.channel is None and after.channel is not None:
        # Check if the voice channel is empty before the user joins
        if len(after.channel.members) == 1:
            # Get the 'notifications' role
            role = discord.utils.get(member.guild.roles, name='notifications')
            if role:
                # Send a message in the default text channel (or any specific channel)
                channel = discord.utils.get(member.guild.text_channels, name='notifications')  # Replace 'general' with your channel name
                if channel:
                    await channel.send(f'{role.mention}, {member.mention} has joined the voice channel {after.channel.mention}.')
                    logger.log(f'{member.name} started a voice channel in {after.channel.name}.')
                else:
                    logger.error('Text channel "notifications" not found.')
            else:
                logger.error('Role "notifications" not found.')
        else:
            logger.log(f'{member.name} joined the voice channel {after.channel.name}.  Members: {[m.name for m in after.channel.members]}')
    elif before.channel is None and after.channel is None:
        logger.log(f'{member.name} left voice channel {before.channel.name}. Members: {[m.name for m in after.channel.members]}')
    elif before.channel is not None and after.channel is not None and before.channel is not after.channel:
        logger.log(f'{member.name} switched from {before.channel.name} to {after.channel.name}. Members: {[m.name for m in after.channel.members]}')

bot.run(os.getenv('DISCORD_TOKEN'))
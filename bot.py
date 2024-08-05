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

@bot.event 
async def on_message(message):
    logger.log(message.author.name + '@' + message.guild.name + ": " + message.content)

    if message.author == bot.user: 
        return 

    if message.content.startswith('$hello'): 
        await message.channel.send('Hallo! ' + message.author.mention)

    if message.content.startswith('$timeout'):
        args = message.content.split(' ')
        if len(args) == 3:
            try:
                user = int(args[1].replace('<@!', '').replace('>', ''))
                timeout = int(args[2])
                member = message.guild.get_member(user)
                member.timeout(datetime.now() + timeout, reason=args[3])
            except ValueError:
                await message.channel.send('Invalid parameter.')
        else:
            await message.channel.send('Invalid number of arguments.')
    
@bot.event
async def on_voice_state_update(member, before, after):
    # Check if the user joined a voice channel
    if before.channel is None and after.channel is not None:
        # Debugging output to verify event trigger
        logger.log(f'{member.name} joined {after.channel.name}. Members: {[m.name for m in after.channel.members]}')
        
        # Check if the voice channel is empty before the user joins
        if len(after.channel.members) == 1:
            # Get the 'notifications' role
            role = discord.utils.get(member.guild.roles, name='notifications')
            if role:
                # Send a message in the default text channel (or any specific channel)
                channel = discord.utils.get(member.guild.text_channels, name='notifications')  # Replace 'general' with your channel name
                if channel:
                    await channel.send(f'{role.mention}, {member.mention} has joined the voice channel {after.channel.mention}.')
                    logger.log(f'{member.name} started a voice chat in {after.channel.name}.')
                else:
                    logger.error('Text channel "notifications" not found.')
            else:
                logger.error('Role "notifications" not found.')
        else:
            logger.log(f'{member.name} joined a voice chat.')
    else:
        logger.log(f'{member.name} left a voice channel.')

bot.run(os.getenv('DISCORD_TOKEN'))
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
    guildLength = 20
    channelLength = 20
    userLength = 20

    logger.log("   ", f'Logged in as {bot.user.name} ({bot.user.id})', '','')
    for guild in bot.guilds:
        role = discord.utils.get(guild.roles, name='notifications')
        if role:
            logger.log("   ", f'Role "notifications" found in guild {guild.name}', '','')
        else:
            logger.error("   ", f'Role "notifications" not found in guild {guild.name}', '','')

        channel = discord.utils.get(guild.text_channels, name='notifications')
        if channel:
            logger.log("   ", f'Text channel "notifications" found in guild {guild.name}', '','')
        else:
            logger.error("   ", f'Text channel "notifications" not found in guild {guild.name}', '','')

        if guildLength < len(guild.name):
            logger.setGuildLength(len(guild.name))
            guildLength = len(guild.name)
        
        for channel in guild.text_channels:
            if channelLength < len(channel.name):
                channelLength = len(channel.name)
        
        for channel in guild.voice_channels:
            if channelLength < len(channel.name):
                channelLength = len(channel.name)

        for member in guild.members:
            if userLength < len(member.name):
                userLength = len(member.name)

    logger.setChannelLength(channelLength)
    logger.setUserLength(userLength)
    logger.setGuildLength(guildLength)

    logger.log('', '', '','')
    logger.log("Guild", "Channel", "User", "Message/Action")
    logger.log("-"*(guildLength + 1), "-"*(channelLength + 1), "-"*(userLength + 1),"--------------------")

@bot.event 
async def on_message(message):
    logger.log(message.guild.name, message.channel.name, message.author.name, message.content)

    if message.author == bot.user: 
        return

@bot.event
async def on_message_delete(message):
    logger.log(message.guild.name, message.channel.name, message.author.name, "deleted message: " + message.content)

@bot.event
async def on_message_edit(before, after):
    logger.log(before.guild.name, before.channel.name, before.author.name, f"edited message: {before.content} -> {after.content}")

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
                    logger.log(member.guild.name, after.channel.name, member.name, f'started')
                else:
                    logger.error(member.guild.name,'', '', 'Text channel "notifications" not found.')
            else:
                logger.error(member.guild.name,'','', 'Role "notifications" not found.')
        else:
            logger.log(member.guild.name, after.channel.name, member.name, f'joined. Members: {[m.name for m in after.channel.members]}')
    elif before.channel is not None and after.channel is None:
        logger.log(member.guild.name, before.channel.name, member.name, f'left')
    elif before.channel is not None and after.channel is not None and before.channel is not after.channel:
        logger.log(member.guild.name, after.channel.name, member.name, f'switched from {before.channel.name}. Members: {[m.name for m in after.channel.members]}')

bot.run(os.getenv('DISCORD_TOKEN'))
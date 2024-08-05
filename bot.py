import discord
import asyncio
from discord.ext import commands
from logger import Logger

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
        await message.channel.send('Hallo!')
    
@bot.event
async def on_voice_state_update(member, before, after):
    # Check if the user joined a voice channel
    if before.channel is None and after.channel is not None:
        # Debugging output to verify event trigger
        logger.log(f'{member.name} joined {after.channel.name}. Members: {[m.name for m in after.channel.members]}')
        
        # Check if the voice channel is empty before the user joins
        if len(after.channel.members) == 1:
            logger.log(f'Channel {after.channel.name} was empty before {member.name} joined.')
            
            # Get the 'notifications' role
            role = discord.utils.get(member.guild.roles, name='notifications')
            if role:
                # Send a message in the default text channel (or any specific channel)
                channel = discord.utils.get(member.guild.text_channels, name='general')  # Replace 'general' with your channel name
                if channel:
                    await channel.send(f'{role.mention}, {member.mention} has joined the voice channel {after.channel.mention}.')
                    logger.log(f'Sent message about {member.name} joining {after.channel.name}.')
                else:
                    logger.log('Text channel not found.')
            else:
                logger.log('Role "notifications" not found.')
        else:
            logger.log(f'Channel {after.channel.name} was not empty before {member.name} joined.')
    else:
        logger.log(f'{member.name} did not join a new voice channel.')

bot.run('ODA0MDk0NTYxOTA2NDU4Njk1.GkELDM.dFe8eU-6_aE78GBuxqLbDG5sXyEF5ru2kzuFdU')
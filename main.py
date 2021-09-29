import os
import discord
from discord.utils import get
import asyncio

from video_queries import yt_query

client = discord.Client()

#bot = Bot(command_prefix="!")

@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  user_guild = message.guild
  msg = message.content
  if message.author == client.user:
    return
  
  if msg.startswith('$'):
    msg = msg[1:].lower()
    if msg.startswith('hello'):
      await message.channel.send('Hello ' + message.author + '!')
    elif msg.startswith('play ') or msg.startswith('p '):
      user = message.author
      voice_channel=user.voice
      if voice_channel.channel:
        voice_channel=user.voice.channel
        # Get url
        if msg.startswith('play '):query = message.content[5:]
        else: query = message.content[2:]
        sound = yt_query(query)
        source = discord.FFmpegPCMAudio(sound.url)
        # Check voice channel
        if (not get(client.voice_clients)) or voice_channel != get(client.voice_clients, guild=user_guild).channel:
          await voice_channel.connect()
        voice = get(client.voice_clients, guild=user_guild)
        if voice and voice.is_playing(): 
          voice.stop() 
        voice.play(source)
        await message.channel.send('Playing ' + sound.title)
        while voice.is_playing():
            await asyncio.sleep(1)
        voice.stop()
      else:
          await message.channel.send('User is not in a channel.')
    elif msg.startswith('stop') or msg.startswith('s'):
      voice = get(client.voice_clients, guild=user_guild)
      if voice and voice.is_connected() and voice.is_playing():
        await message.channel.send('Music stopped')
        voice.stop()
      else:
        await message.channel.send('No music was playing')

client.run('')
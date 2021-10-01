import asyncio
import discord
import os
import youtube_dl
from discord.ext import commands#, tasks
from video_queries import YTDLSource

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='-',intents=intents)
tok = open("../tok.txt", "r")

@bot.event
async def on_ready():
  print('Logged in as {0.user}'.format(bot))

@bot.command(name='play', help='To play song')
async def play(ctx, *url):
   url = ' '.join(url)
   server = ctx.message.guild
   voice_channel = server.voice_client

   if not voice_channel:
      if not ctx.message.author.voice:
          await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
          return
      else:
          channel = ctx.message.author.voice.channel
      await channel.connect()
      voice_channel = server.voice_client

   if voice_channel:
      async with ctx.typing():
          filename = await YTDLSource.from_url(url)
          if voice_channel.is_playing(): voice_channel.stop()
          voice_channel.play(discord.FFmpegPCMAudio(filename.url))
      await ctx.send('**Now playing:** {}'.format(filename.title))
   else: print('No conectado al canal de voz')

@bot.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment.")

@bot.command(name='resume', help='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        voice_client.resume()
    else:
        await ctx.send("The bot was not playing anything before this. Use play_song command")

@bot.command(name='stop', help='Stops the song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")

@bot.command(name='disconnect', help='To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@bot.event
async def on_message(message):
    await bot.process_commands(message) 
    if str(message.content).lower() == "hello cloud":
        await message.channel.send('Hi!')

bot.run(tok.read())
#bot.run(os.environ['token'])
tok.close()

print('Bye!')

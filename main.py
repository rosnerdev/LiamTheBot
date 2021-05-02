import os
import json
import random
import requests
import discord
from discord.ext import commands
import googlesearch
import sqlite3
from replit import db
from discord.ext import tasks
from discord.utils import get

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='$', intents=intents)
db = sqlite3.connect('main.db')
main = db.cursor()

q = " "

@bot.event
async def on_ready():
    print("Bot Online.")



@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount : int):
    await ctx.channel.purge(limit=amount+1)
    await ctx.send('Done!')

@purge.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify the amount of messages you want to clear. Usage: //clear <number>')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You do not have manage_messages permssion')

api_weather = os.environ['api_weather']


@bot.command()
async def temp(ctx, *args):
  argument = (' ').join(list(args))
  temp = 'https://api.openweathermap.org/data/2.5/weather?q='+argument+'&units=metric&appid='+api_weather
  get = requests.get(temp)
  json = get.json()["main"]["temp"]
  await ctx.send("The temperature in the selected city is: " + str(json))

@bot.command()
async def wiki(ctx, *args):
  argument = (' ').join(list(args))
  term = argument + " wikipedia"
  searcher = googlesearch.search(term)
  await ctx.send("Result from Wikipedia:")
  await ctx.send(searcher[0])

@bot.command()
async def youtube(ctx, *args):
  argument = (' ').join(list(args))
  term = argument + " youtube"
  searcher = googlesearch.search(term, num_results=5)
  await ctx.send("Results from Youtube:")
  for s in searcher:
    await ctx.send(s)

@bot.command()
async def google(ctx, *args):
  argument = (' ').join(list(args))
  term = argument
  searcher = googlesearch.search(term, num_results=3)
  await ctx.send("Results from Google:")
  for s in searcher:
    await ctx.send(s)

@bot.command()
async def welcome_channel(ctx, channel:discord.TextChannel):
  if channel is not None:
    db = sqlite3.connect('main.db')
    cursor = db.cursor()
    cursor.execute(f"SELECT channel_id FROM wel_c WHERE guild_id = '{ctx.guild.id}'")
    channel_id = cursor.fetchone()
    if channel_id is None:
      sql = ("INSERT INTO wel_c(guild_id, channel_id) VALUES(?,?)")
      val = (ctx.guild.id, channel.id)
      cursor.execute(sql, val)
      db.commit()
      await ctx.send(f"The channel '{channel.name}' has been set.")
    else:
      sql = ("UPDATE wel_c SET channel_id = ? WHERE guild_id = ?")
      val = (channel.id, ctx.guild.id)
      cursor.execute(sql, val)
      db.commit()
      await ctx.send(f"The channel '{channel.name}' has been update.")

  else:
    await ctx.send("Pls send the channel that u want.")

my_secret = os.environ['TOKEN']
bot.run(my_secret)

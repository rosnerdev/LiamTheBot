import os
import random
import requests
import discord
from discord.ext import commands
import googlesearch

client = discord.Client()
bot = commands.Bot(command_prefix='$')

q = " "

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

api_gif = 'your-token'

@bot.command()
async def gif(ctx, *args):
    q = (' ').join(list(args))
    link = 'https://api.giphy.com/v1/gifs/search?api_key='+api_gif+'&q='+q+'&limit=25&offset=0&rating=r&lang=en'
    get = requests.get(link)
    json = get.json()["data"][random.randint(0,9)]["embed_url"]
    await ctx.send(json)


api_weather = 'your-token'


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

my_secret = 'your-token'
bot.run(my_secret)

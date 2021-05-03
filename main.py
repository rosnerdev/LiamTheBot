import os
import json
import random
import requests
import discord
from discord.ext import commands
import googlesearch
from replit import db

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} Ready.')



@bot.command(pass_context=True)
@bot.event
async def on_member_join(member):
    print(f'{member} has joined a server.')
    await member.send(f"Hello {member}!")
    await member.send(f"Welcome to the server!")
    async def member_join_channel(ctx, member=member):
      await ctx.send(f"Hello and Welcome, {member}!")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send('Done!')


@purge.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            'Please specify the amount of messages you want to clear. Usage: //clear <number>'
        )
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You do not have manage_messages permssion')


api_weather = os.environ['api_weather']


@bot.command()
async def temp(ctx, *args):
    argument = (' ').join(list(args))
    temp = 'https://api.openweathermap.org/data/2.5/weather?q=' + argument + '&units=metric&appid=' + api_weather
    get = requests.get(temp)
    json = get.json()["main"]["temp"]
    lists = ["\"If you want to see the sunshine, you have to weather the storm.\" - Frank Lane", "\"We could all take a lesson from the weather, It pays no attention to criticism.\"", "\"Wherever you go, no matter what the weather, always bring your own sunshine.\" - Anthony J. D'Angelo", "\"There is no such thing as bad weather, Only inappropriate clothing.\""]
    await ctx.send("The temperature in the selected city is: " + str(json))
    await ctx.send(lists[random.randint(0,3)])

@bot.command()
async def youtube(ctx, *args):
    argument = (' ').join(list(args))
    term = argument, "liam neeson", "youtube"
    searcher = googlesearch.search(term, num_results=4)
    await ctx.send(searcher[random.randint(0,3)])


@bot.command()
async def google(ctx, *args):
    argument = (' ').join(list(args))
    term = argument, "liam neeson"
    searcher = googlesearch.search(term, num_results=1)
    await ctx.send("Result from Google:")
    for s in searcher:
        await ctx.send(s)

my_secret = os.environ['TOKEN']
bot.run(my_secret)

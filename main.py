import os
import discord
import random
import requests
import json
import asyncio
from discord.ext import commands
#fhgf
intents = discord.Intents.all()

helpCommand=commands.DefaultHelpCommand(no_category='Commands')

bot = commands.Bot(command_prefix = "!amelia", intents = intents, helpCommand=helpCommand)

@bot.event

async def on_connect():
  print("bot is online")

@bot.command(brief="the bot will say hi")
async def hi(ctx):
  await ctx.reply("hello from amelia's bot")

@bot.command(brief="enter a name to greet")
async def name(ctx, name):
  await ctx.reply("hello " + name + "!")

@bot.command(brief = "add two numbers separated by a space")
async def add(ctx, num1, num2):
  num3 = int(num1) + int(num2)
  await ctx.reply(str(num1) + "+" + str(num2) + "=" + str(num3))

@bot.command(brief="enter the hour and am/pm")
async def time(ctx, hour, ampm):
  if(ampm == "am"):
    await ctx.reply("good morning")
  else:
    hour2 = int(hour)
    if(hour2 >= 6):
      await ctx.reply("good evening")
    else:
      await ctx.reply("good afternoon")

@bot.command(brief="receive a picture of a dumpster fire")
async def dumpsterfire(ctx):
  await ctx.reply("https://bloximages.chicago2.vip.townnews.com/sharonherald.com/content/tncms/assets/v3/editorial/b/f8/bf8fd690-dc26-58bc-bd9b-0c62436c437a/5aa22d7456db5.image.jpg?resize=400%2C281")

birdList = ["https://www.allaboutbirds.org/guide/assets/photo/308074031-480px.jpg", "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/362635561/900", "https://www.activewild.com/wp-content/uploads/2017/10/animals-that-start-with-p-parrot.jpg", "https://qph.cf2.quoracdn.net/main-qimg-fbd27abdbbd663ef42937998ab71d782-lq"]

@bot.command(brief="receive a random bird picture")
async def birds(ctx):
  pic = random.choice(birdList)
  await ctx.send(pic)

eightballList = ["certainly", "no lol", "without a doubt", "over my dead body"]

@bot.command(brief="ask a question you want to answer")
async def eightball(ctx, *, phrase: str):
  reply = random.choice(eightballList)
  await ctx.send("**" + phrase + "** " + reply)

rpsList = ["rock", "paper", "scissors"]

@bot.command(brief="enter your choice in rock paper scissors and play against the bot")
async def rps(ctx, choice):
  botChoice = random.choice(rpsList)
  choice = choice.lower()
  print(botChoice)
  if botChoice == "rock":
    if choice == "rock":
      await ctx.reply("Tie! You chose " + choice + ", and the bot chose " + botChoice + ".")
    elif choice == "paper":
      await ctx.reply("You won! You chose " + choice + ", and the bot chose " + botChoice + ".")
    elif choice == "scissors":
      await ctx.reply("You lose. You chose " + choice + ", and the bot chose " + botChoice + ".")
      
  if botChoice == "paper":
    if choice == "rock":
      await ctx.reply("You lose. You chose " + choice + ", and the bot chose " + botChoice + ".")
    elif choice == "paper":
      await ctx.reply("Tie! You chose " + choice + ", and the bot chose " + botChoice + ".")
    elif choice == "scissors":
      await ctx.reply("You won! You chose " + choice + ", and the bot chose " + botChoice + ".")

  if botChoice == "scissors":
    if choice == "rock":
      await ctx.reply("You won! You chose " + choice + ", and the bot chose " + botChoice + ".")
    elif choice == "paper":
      await ctx.reply("You lose. You chose " + choice + ", and the bot chose " + botChoice + ".")
    elif choice == "scissors":
      await ctx.reply("Tie! You chose " + choice + ", and the bot chose " + botChoice + ".")

@bot.command(brief="receive a random joke")
async def joke(ctx):
  url="https://official-joke-api.appspot.com/random_joke"
  req = requests.get(url)
  #get data from url
  data=req.json()
  setup=data["setup"]
  punchline=data["punchline"]
  await ctx.send(setup)
  await asyncio.sleep(3)
  await ctx.send(punchline)

@bot.command(brief="enter your zip code")
async def weather(ctx, zip):
  my_secret_weather = os.environ['weatherAPIkey']
  
  url="https://api.openweathermap.org/data/2.5/weather?zip=" + zip + ",US&appid=" + my_secret_weather
  
  req = requests.get(url)
  data=req.json()
  weather=data["weather"][0]["description"]

  temp = data["main"]["temp"]
  temp = (temp - 273.15) * 9/5 + 32
  temp = round(temp, 2)
  
  await ctx.send(weather + " " + str(temp) + " degrees F")

@bot.command(brief="enter two names separated by a space to see how compatible they are")
async def love(ctx, name1, name2):
  url = "https://love-calculator.p.rapidapi.com/getPercentage"

  querystring = {"sname":name1,"fname":name2}
  
  love_API = os.environ['loveAPIkey']
  headers = {
	  "X-RapidAPI-Key": love_API,
	  "X-RapidAPI-Host": "love-calculator.p.rapidapi.com"
  }

  response = requests.request("GET", url, headers=headers, params=querystring)

  data = response.json()
  percentage = data["percentage"]
  result = data["result"]

  print(response.text)
  await ctx.send("you're " + percentage + "% compatible. " + result)

@bot.command(brief="enter a word to see it's urban dictionary definition")
async def urban(ctx, word):
  urban_API = os.environ['urbanAPIkey']
  url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"

  querystring = {"term": word}

  headers = {
	  "X-RapidAPI-Key": urban_API,
	  "X-RapidAPI-Host": "mashape-community-urban-dictionary.p.rapidapi.com"
  }

  response = requests.request("GET", url, headers=headers, params=querystring)

  print(response.text[0:2000])
  
  data = response.json()
  definition = data["list"][0]["definition"]

  await ctx.send(definition)

my_secret = os.environ['token']
bot.run(my_secret)
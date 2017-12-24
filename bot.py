import discord
from discord.ext import commands
import random

bot = commands.Bot(command_prefix = '%', description = "ion's secs bot")

@bot.event
async def on_ready():
    print("on_ready fired. You are in debug mode.")
    print("Bot initialized. Logging in...")
    print('Logged in as ' + bot.user.name + ' with ID [' + bot.user.id + '] on:')
    for sv in bot.servers:
        print('\t[' + str(sv.id) + '] ' + str(sv.name))
        print('\n')

@bot.command(pass_context=True)
async def dai(ctx, id, msj):
    await bot.send_message(await bot.get_user_info(id), msj)

rezultat = 0
nextOper =""
splituit = []

@bot.event
async def on_message(message):
    '''if "+" in message.content:
        msj = message.content.split()
        rezultat = int(msj[0]) + int(msj[2])
        await bot.send_message(message.channel, str(rezultat))
    elif "-" in message.content:
        msj = message.content.split()
        rezultat = int(msj[0]) - int(msj[2])
        await bot.send_message(message.channel, str(rezultat))
    elif "*" in message.content:
        msj = message.content.split()
        rezultat = int(msj[0]) * int(msj[2])
        await bot.send_message(message.channel, str(rezultat))
    elif "/" in message.content or ":" in message.content:
        msj = message.content.split()
        rezultat = int(msj[0]) / int(msj[2])
        await bot.send_message(message.channel, str(rezultat))
    elif "^" in message.content:
        msj = message.content.split()
        rezultat = int(msj[0]) ** int(msj[2])
        await bot.send_message(message.channel, str(rezultat))'''
    global splituit
    global rezultat
    splituit = message.content.split()
    rezultat = int(splituit[0])
    splituit.remove(splituit[0])
    if message.author.id != bot.user.id:
        for elem in splituit:
            global nextOper
            if (not any(char.isdigit() for char in elem)) and ("+-/*^:".find(elem)!=-1):
                nextOper = elem
            elif any(char.isdigit() for char in elem) and nextOper=="+":
                rezultat = rezultat + int(elem)
            elif any(char.isdigit() for char in elem) and nextOper=="-":
                rezultat = rezultat - int(elem)
            elif any(char.isdigit() for char in elem) and nextOper=="*":
                rezultat = rezultat * int(elem)
            elif any(char.isdigit() for char in elem) and (nextOper=="/" or nextOper==":"):
                rezultat = rezultat / int(elem)
            elif any(char.isdigit() for char in elem) and nextOper=="^":
                rezultat = rezultat ** int(elem)


        await bot.send_message(message.channel, str(rezultat))



bot.run("Mzk0NTU0MzA3ODQxNjIyMDI2.DSGA2Q.zWEtGR_ORdLsELiNp60p94GCJQk")

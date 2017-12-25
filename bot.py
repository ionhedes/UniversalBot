import discord
from discord.ext import commands
import google
import random
import re

bot = commands.Bot(command_prefix = '%', description = "Bot for everything!")

@bot.event
async def on_ready():
    print("on_ready fired. You are in debug mode.")
    print("Bot initialized. Logging in...")
    print('Logged in as ' + bot.user.name + ' with ID [' + bot.user.id + '] on:')
    for sv in bot.servers:
        print('\t[' + str(sv.id) + '] ' + str(sv.name))
        print('\n')



@bot.command(pass_context=True)
async def mseg(ctx, id, msj):
    if ctx.message.channel.id == '190836493399359488' or ctx.message.channel.id == '394560963510140939':
        await bot.send_message(await bot.get_user_info(id), msj)

rezultat = 0
nextOper =""
splituit = []

@bot.command(pass_context=True)
async def join(ctx):
    if ctx.message.channel.id == '190836493399359488' or ctx.message.channel.id == '394560963510140939':
        for ch in bot.get_all_channels():
            for usr in ch.voice_members:
                if usr.id == ctx.message.author.id:
                    await bot.join_voice_channel(ch)

@bot.command(pass_context=True)
async def disc(ctx):
    if ctx.message.channel.id == '190836493399359488' or ctx.message.channel.id == '394560963510140939':
        for cl in bot.voice_clients:
            if (cl.server == ctx.message.server):
                await cl.disconnect()

@bot.event
async def on_message(message):
    global splituit
    global rezultat
    global expresie

    if message.content[0] != "%" and message.author.id != bot.user.id and (message.channel.id == '190836493399359488' or message.channel.id == '394560963510140939'):
        expresie = message.content
        index = re.search("\d", expresie)
        expresie = expresie [index.start(): len(expresie)]
        splituit = expresie.split()
        rezultat = int(splituit[0])
        splituit.remove(splituit[0])
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
    await bot.process_commands(message)

@bot.command(pass_context=True)
async def search(ctx, *, text):
    if ctx.message.channel.id == '190836493399359488' or ctx.message.channel.id == '394560963510140939':
        src = google.search(text)
        i=0
        for url in src:
            i+=1
            if i>4:
                break
            await bot.send_message(ctx.message.channel, url)

bot.run("Mzk0NTU0MzA3ODQxNjIyMDI2.DSGA2Q.zWEtGR_ORdLsELiNp60p94GCJQk")




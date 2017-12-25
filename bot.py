import discord
from discord.ext import commands
import google
import re
from ctypes.util import find_library
import configparser
import os.path
from shutil import copyfile
import time
import sys
import validators
import urllib.request
import urllib.parse

config = configparser.ConfigParser()
if os.path.isfile("config.ini"):
    config.read("config.ini")
else:
    try:
        copyfile("default_config.ini", "config.ini")
        print("Config file config.ini not found, generating a new one from default_config.ini", flush=True)
        time.sleep(1)
        config.read("config.ini")
    except:
        print("FATAL: Neither config.ini , nor default_config.ini do not exist, cannot create bot. Exiting in 5 seconds.", flush=True)
        time.sleep(5)
        sys.exit(1)
try:
    token = config["Login"]["token"]
    cmdPref = config["Options"]["command_prefix"]
    bindToTxt = config["Options"]["bind_to_channels"].split()
    bindToMusic = config["Music"]["music_text_channels"].split()
except:
    cmdPref = "%"
    print("Something wrong with the config. If you crash, delete it so we can regenerate it.", flush=True)

bot = commands.Bot(command_prefix = cmdPref, description = "Bot for everything!")
opus = discord.opus.load_opus(find_library("opus"))
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
    if ctx.message.channel.id in bindToTxt:
        await bot.send_message(await bot.get_user_info(id), msj)

rezultat = 0
nextOper =""
splituit = []

@bot.command(pass_context=True)
async def join(ctx):
    if ctx.message.channel.id in bindToTxt:
        global voice
        for ch in bot.get_all_channels():
            for usr in ch.voice_members:
                if usr.id == ctx.message.author.id:
                    voice = await bot.join_voice_channel(ch)

@bot.command(pass_context=True)
async def play(ctx, link):
    if ctx.message.channel.id in bindToMusic:
        global player
        if validators.url(link):
            player = await voice.create_ytdl_player(link)
            player.start()
        elif not validators.url(link):
            cautare = urllib.parse.urlencode({"search_query" : link})
            rezultate_cautare = urllib.request.urlopen("http://www.youtube.com/results?" + cautare)
            nume_videouri = re.findall(r'href=\"\/watch\?v=(.{11})', rezultate_cautare.read().decode())
            link = nume_videouri[0]
            player = await voice.create_ytdl_player(link)
            player.start()


@bot.command(pass_context=True)
async def pause(ctx):
    if ctx.message.channel.id in bindToMusic:
        player.pause()

@bot.command(pass_context=True)
async def resume(ctx):
    if ctx.message.channel.id in bindToMusic:
        player.resume()

@bot.command(pass_context=True)
async def stop(ctx):
    if ctx.message.channel.id in bindToMusic:
        player.stop()

@bot.command(pass_context=True)
async def disc(ctx):
    if ctx.message.channel.id in bindToMusic:
        for cl in bot.voice_clients:
            if (cl.server == ctx.message.server):
                await cl.disconnect()

@bot.event
async def on_message(message):
    global splituit
    global rezultat
    global expresie
    if message.content[0] != cmdPref and message.author.id != bot.user.id and (message.channel.id in bindToTxt):
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
    if ctx.message.channel.id in bindToTxt:
        src = google.search(text)
        i=0
        for url in src:
            i+=1
            if i>4:
                break
            await bot.send_message(ctx.message.channel, url)

@bot.command(pass_context=True)
async def shutdown(ctx):
    if ctx.message.channel.id in bindToTxt:
        await bot.close()


if token == "YourToken":
    print("Bot login token is invalid. You need to go into config.ini and change the token under Login to your bot's token. Exiting in 5 seconds.")
    time.sleep(5)
    sys.exit(1)
else:
    try:
        bot.run(token)
    except:
        print("There was an error while connecting the bot to Discord.\nEither your login token is invalid, or idk. Exiting in 5 seconds.")
        time.sleep(5)
        sys.exit(1)

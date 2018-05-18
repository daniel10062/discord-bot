"""Discord bot source code!"""
import discord
from random import randint, randrange
from discord.ext import commands
import asyncio
import os, json

bot = commands.Bot(command_prefix='!')

client = discord.Client()

GuessGameList = ['hejsan']

@bot.command()
async def test():
    await bot.say('testing testing')

# @bot.command()
# async def mute(member : discord.Member):
#     if member.id == '225606372849352705':
#         await bot.say('You cant mute the creater :knife:')
#         return
#     else:
#         await bot.add_roles(member,member.role)
#         await bot.say('{} has been muted and got added to {}.'.format(member.mention, role))
#
#
# @bot.command()
# async def unmute(member: discord.Member):
#     await bot.server_voice_state(member,mute=False)
#     await bot.say('{} has been unmuted.'.format(member.mention))

def check_muted(member):
    with open('discord_mute.mt1', 'r') as ss:
        mute_list = json.load(ss)
        if member in mute_list:
            return True
    return False

@bot.command(pass_context = True)
async def mute(ctx, *, member : discord.Member):
    if not os.path.isfile('discord_mute.mt1'):
        discord_mute_id = []
    else:
        with open('discord_mute.mt1', 'r') as dm:
            discord_mute_id = json.load(dm)
    if not member.id in discord_mute_id:
        discord_mute_id.append(member.id)
        await bot.say('Muted {}'.format(member))
    with open('discord_mute.mt1', 'w') as ds:
        json.dump(discord_mute_id, ds)

@bot.command(pass_context = True)
async def unmute(ctx, *, member: discord.Member):
    with open('discord_mute.mt1', 'r') as qs:
        a = json.load(qs)
        if member.id in a:
            a.remove(member.id)
            with open('discord_mute.mt1', 'w') as qr:
                json.dump(a, qr)
                await bot.say("Took away {}'s mute".format(member))
        else:
            await bot.say("{} is not a muted member".format(member))


    #write code that looks into the list in the file
    #write code to delete every message the memer id in the list writes
    #write code to update the lsit in the file


@bot.command(pass_context = True)
async def echo(ctx, *,echo: str):
    if not check_muted(ctx.message.author.id):
        await bot.delete_message(ctx.message)
        await bot.say(":smile: " + echo + ":smile:")
    else:
        await bot.say('You are muted')
        await bot.delete_message(ctx.message)

@bot.command(pass_context = True)
async def kill(ctx, *,member : discord.Member = None):
    if member is None:
        await bot.say(ctx.message.author.mention + "Sorry, you need to tell me who to kill!")
        return

    if member.id == '435698986834198529':
        await bot.say(ctx.message.author.mention + 'Ha! You think you can kill me? :devil:')
        return
    elif member.id == '225606372849352705':
        await bot.say(ctx.message.author.mention + "Don't you dare kill my creater! :knife:")
        return
    await bot.say("I poisoned {} food.. This will be fun to watch :smiling_imp:".format(member.name))

@bot.command(pass_context = True)
async def choose(ctx, *, choices: str):
    choicesArray = choices.split(",")
    chosen = choicesArray[randrange(len(choicesArray))]
    await bot.say(ctx.message.author.mention + 'I will choose: ```{}```'.format(chosen))

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------------')
    print('Bot is ready to do work!')
    print('------------')

@bot.listen()
async def on_message(msg):
    if check_muted(msg.author.id):
        await bot.delete_message(msg)


bot.run('NDM1Njk4OTg2ODM0MTk4NTI5.Dbcwaw.NWfE_wzRS1fBmzMD8NIHkKPNjwQ')

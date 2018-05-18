"""Discord bot source code!"""
import discord
from random import randint
from discord.ext import commands
import asyncio
import os
import json

client = discord.Client()

GuessGameList = ['hejsan', 'tjenare', 'traveler', 'sir', 'pirate']
quotemachineVAR = '!addquote'

#roles = client.get_server("235834703935045632").roles

##how to call it



# @client.event
# async def on_message(message):
#     # we do not want the bot to reply to itself
#     if message.author == client.user:
#         return
#
#     if message.content.startswith('!hello'):
#         msg = 'Hello {0.author.mention}'.format(message)
#         await client.send_message(message.channel, msg)


def get_role(server_roles, target_name):
   for each in server_roles:
      if each.name == target_name:
         return each
   return None


@client.event
async def on_message(message):
    await bot.server_voice_state(member,mute=False)
    await bot.say('{} has been unmuted.'.format(member.mention))


@client.event
async def on_message(message):
# we do not want the bot to reply to itself
    if message.author == client.user:
        return

    #HANGMAN GAME
    if message.content.startswith('!hangman'):
        word_G = GuessGameList[randint(0,(len(GuessGameList)-1))]
        finish_word = word_G
        first = True
        life = 3
        #await client.send_message(message.channel, '``` {} ```'.format())
        while life > 0:
            if len(word_G) < 1:
                return await client.send_message(message.channel, 'Good job you won, word finished {}'.format(finish_word))

            if first == True:
                await client.send_message(message.channel, "I have chosen a word, please start guessing for one letter. The word is {} long".format(len(word_G)))
                word_I = await client.wait_for_message(timeout = 10.0, author=message.author)
                first = False
            else:
                await client.send_message(message.channel, 'Please choose another letter now!')
                word_I = await client.wait_for_message(timeout = 10.0, author=message.author)

            if word_I == None or word_I.content not in word_G:
                back_msg = 'Sorry, your took to long or didnt answer with the right letter. Your current lives: {}. '
                life -= 1
                await client.send_message(message.channel, back_msg.format(life))
                continue

            if word_I.content in word_G:
                word_G = word_G.replace(word_I.content, '')
                await client.send_message(message.channel, 'Good, you were right. Your guess {}. Amount of letter left in the word: {}'.format(word_I.content, len(word_G)))
                continue
        else:
            await client.send_message(message.channel, 'You lost! The word was {}'.format(finish_word))

    #Quote machine
    if message.content.startswith(quotemachineVAR):
        if not os.path.isfile('quote_file_for_discord.pk1'):
            quote_list = []
        else:
            with open('quote_file_for_discord.pk1', 'r') as ql:
                quote_list = json.load(ql)
        quote_list.append(message.content[len(quotemachineVAR):])
        with open('quote_file_for_discord.pk1', 'w') as ff:
            json.dump(quote_list, ff)
            await client.send_message(message.channel, 'Just added a quote')

    if message.content.startswith('!Rquote'):
        with open('quote_file_for_discord.pk1', 'r') as quote_list:
            quote_list = json.load(quote_list)
        await client.send_message(message.channel, '```' + quote_list[randint(0,len(quote_list) -1)] + '```')

    if message.content.startswith('!deletequote'):
        with open('quote_file_for_discord.pk1', 'r') as qs:
            quote_list = json.load(qs)
            if message.content[12:] in quote_list and len(message.content) > 12:
                quote_list.remove(message.content[12:])
                with open('quote_file_for_discord.pk1', 'w') as dd:
                    json.dump(quote_list, dd)
                    await client.send_message(message.channel, 'Deleted {} from quote list'.format(message.content[13:]))
            else:
                await client.send_message(message.channel, 'There is no such word, you delete arg was {}'.format(message.content[13:]))

    #HELLO TO USER
    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    #GUESS THE NUMBER GAME
    if message.content.startswith('!guess'):
        await client.send_message(message.channel, 'Guess a number between 1 to 19')

        def guess_check(m):
            return m.content.isdigit()

        guess = await client.wait_for_message(timeout=5.0, author=message.author, check=guess_check)
        answer = randint(1, 19)
        if guess is None:
            fmt = 'Sorry, you took too long. It was {}.'
            await client.send_message(message.channel, fmt.format(answer))
            return
        if int(guess.content) == answer:
            await client.send_message(message.channel, 'You are right!')
            return
        else:
            await client.send_message(message.channel, 'Sorry. It is actually {}.'.format(answer))
            return

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------------')
    print('Bot is ready to do work!')
    print('------------')

client.run('NDM1MzQzMTc1NjYyNjk4NDk2.DbedAw.q3AxmD2voK0jquuCtzyxHtdVFys')

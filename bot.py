import random

import discord
import os

from dotenv import load_dotenv

load_dotenv(dotenv_path="config")

env = "TEST"

if env == "PROD":
    TOKEN = os.getenv("TOKEN")
    CHANNEL_DJ_101_150 = int(os.getenv("CHANNEL_DJ_101_150"))
    CHANNEL_DJ_151_190 = int(os.getenv("CHANNEL_DJ_151_190"))
    CHANNEL_DJ_191_200 = int(os.getenv("CHANNEL_DJ_191_200"))
    CHANNEL_EXPE = int(os.getenv("CHANNEL_EXPE"))
else:
    TOKEN = os.getenv("TOKEN_TEST")
    CHANNEL_DJ_101_150 = int(os.getenv("CHANNEL_DJ_101_150_TEST"))
    CHANNEL_DJ_151_190 = int(os.getenv("CHANNEL_DJ_151_190_TEST"))
    CHANNEL_DJ_191_200 = int(os.getenv("CHANNEL_DJ_191_200_TEST"))
    CHANNEL_EXPE = int(os.getenv("CHANNEL_EXPE_TEST"))

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


def lire_fichier(chemin):
    f = open(chemin, 'r')
    message = f.read()
    f.close()
    return message


async def reinit_donjon(channel_id, chemin):
    salon = client.get_channel(channel_id)
    await salon.purge()
    text_dj = lire_fichier(chemin)
    liste_dj = text_dj.split('-')
    for dj in liste_dj:
        djsend = await salon.send(dj)
        await djsend.add_reaction("0⃣")
        await djsend.add_reaction("1⃣")
        await djsend.add_reaction("2⃣")
        await djsend.add_reaction("3⃣")
        await djsend.add_reaction("4⃣")

async def reinit_expe(channel_id, chemin):
    salon = client.get_channel(channel_id)
    await salon.purge()
    text_dj = lire_fichier(chemin)
    liste_dj = text_dj.split('-')
    for dj in liste_dj:
        djsend = await salon.send(dj)
        await djsend.add_reaction(u"\U0001F170")
        await djsend.add_reaction(u"\U0001F171")


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    # await reinit_expe(CHANNEL_EXPE, s'Expeditions.txt')
    # await reinit_donjon(CHANNEL_DJ_101_150, 'Succes_101_150.txt')
    # await reinit_donjon(CHANNEL_DJ_151_190, 'Succes_151_190.txt')
    # await reinit_donjon(CHANNEL_DJ_191_200, 'Succes_191_200.txt')


@client.event
async def on_message(message):
    if message.content == "!purge":
        await message.channel.purge()

    if message.content == "!reinit":
        if message.channel.id == CHANNEL_DJ_101_150:
            await reinit_donjon(CHANNEL_DJ_101_150, 'Succes_101_150.txt')
        if message.channel.id == CHANNEL_DJ_151_190:
            await reinit_donjon(CHANNEL_DJ_151_190, 'Succes_151_190.txt')
        if message.channel.id == CHANNEL_DJ_191_200:
            await reinit_donjon(CHANNEL_DJ_191_200, 'Succes_191_200.txt')

    if message.content.startswith('!'):
        messages = message.channel.history(limit=None)
        commande = message.content.upper()
        donjon = message.content[1:].upper()

        async for msg in messages:
            if message.id != msg.id and donjon in msg.content:
                print(commande)
                print(msg.content)
                response = ""
                for reac in msg.reactions:
                    users_reac = ""

                    async for user in reac.users():
                        if user.id != client.user.id :
                            users_reac += user.name + ", "

                    response += reac.emoji + " : " + users_reac + "\n"
                await msg.reply(response)

client.run(TOKEN)

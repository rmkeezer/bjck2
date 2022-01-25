from discord.ext import commands
from datetime import date, datetime, timedelta
import random

import os
import openai

version = "0.5.0rc3"

openai.api_key = os.getenv("OPENAI_KEY")

TOKEN = os.getenv("DISCORD_KEY")

client = commands.Bot(command_prefix=',,')

@client.event
async def close():
    ch = client.get_channel(339956015078572044)
    await ch.send("BJCK is now offline")

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

    ch = client.get_channel(633438770867339294)
    print(ch)
    msg = await ch.fetch_message(771240583258832896)
    print(msg)
    emoji = client.get_emoji(746582307770597476)
    print(msg.author.name)
    print(emoji)
    await msg.add_reaction(emoji)
    ch = client.get_channel(339956015078572044)
    await ch.send("BJCK is now online")
    await ch.send("Version " + version)

def get_rand_date():
    start_date = date(2018, 1, 1)
    end_date = date.today()
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + timedelta(days=random_number_of_days)
    return random_date

async def get_history(channel):
    output = ""
    msgs = await channel.history(limit=50, before=datetime.combine(get_rand_date(), datetime.min.time())).flatten()
    for msg in msgs:
        if "BJCK.2" == msg.author.name:
            continue
        output += msg.author.name + ": " + msg.content + "\n"
    return output

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if 'bjck' in message.content.lower():
        # emoji = client.get_emoji(686763202561704027)
        # print(emoji)
        # await message.add_reaction(emoji)
        keezysgoodtime = client.get_channel(633438770867339294)
        history = await get_history(keezysgoodtime)
        input_prompt = history + message.author.name + ": " + message.content + "\nDiceShade:"
        print(input_prompt)
        response = openai.Completion.create(
            engine="babbage",
            prompt=input_prompt,
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6,
            stop=["\n"]
        )
        print("Output: " + response.choices[0].text)
        await message.channel.send(response.choices[0].text)
    # if 'bjck' in message.content.lower():
    #     chance = random.random()
    #     print(chance)
    #     if chance > 0.01:
    #         if chance < 0.5:
    #             emoji = client.get_emoji(686763202561704027)
    #             print(emoji)
    #             await message.add_reaction(emoji)
    #     elif chance > 0.005:
    #         print(f'Loading...')
    #         await message.channel.send('Loading...')
    #         emoji = client.get_emoji(686763202561704027)
    #         print(emoji)
    #         await message.add_reaction(emoji)
    #     elif chance > 0.001:
    #         print(f'Loading.....')
    #         await message.channel.send('Loading.....')
    #         emoji = client.get_emoji(686763202561704027)
    #         print(emoji)
    #         await message.add_reaction(emoji)
    #     elif chance > 0.0005:
    #         print(f'Error, please restart')
    #         await message.channel.send('Error, please restart')
    #         emoji = client.get_emoji(686763202561704027)
    #         print(emoji)
    #         await message.add_reaction(emoji)
    #     else:
    #         print(f'WARNING: LOADING COMPLETE')
    #         await message.channel.send('WARNING: LOADING COMPLETE')
    #         emoji = client.get_emoji(686763202561704027)
    #         print(emoji)
    #         await message.add_reaction(emoji)

client.run(TOKEN)

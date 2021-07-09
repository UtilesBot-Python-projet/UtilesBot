import discord
from discord.ext import commands

préfix = "<"

async def delet_command(ctx):
    messages = await ctx.channel.history(limit=1).flatten()
    for message in messages:
        await message.delete()

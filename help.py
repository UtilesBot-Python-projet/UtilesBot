import discord
from discord.ext import commands
from fonction import delet_command, préfix


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        await delet_command(ctx)
        await ctx.send(f"{ctx.author.mention} __*je tes envoyer la liste de mes commands en MP :pencil:*__")
        embed = discord.Embed(title=":muscle: Help", description='Voici la liste de mes commands', color=ctx.author.color)
        embed.add_field(name=':tools: Config', value=f"`{préfix}config` : sert a config/setut le bot", inline=False)
        embed.add_field(name=':shield: Modération', value=f"\n`{préfix}ban [@user] [reson]` : **sert à ban un membre.**\n\n`{préfix}unban [user#0000] [reson]` : **sert à débanir un membre ban.**\n\n`{préfix}mute [@user] [reson]` : **sert à mute un membre sur le serveur.**\n\n`{préfix}unmute [@user]` : **sert à démute un membre mute.**\n\n`{préfix}kick [@user] [reson]` : **sert à kick un membre du serveur.**\n\n`{préfix}clear [mumber of message]` : **sert à effacer un nombre de message donné du channel où là command a était éfectué.**\n\n`{préfix}allclear` : **sert à suprimer tous les message du chanel où la commande a était efectuer.**\n", inline=False)
        await ctx.author.send(embed=embed)
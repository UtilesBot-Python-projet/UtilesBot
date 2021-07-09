print("lansement du bot ...")
import discord
from discord.ext import commands
import random
import asyncio
import Config
import event
import Admin
import help
import sqlite3
from fonction import delet_command, préfix
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO


# Les variable

token = "ODIxNDE0ODAwNzE3MjUwNTgx.YFDYJQ.uVwvvggs2f6sk7BEvyh-hvv7CPE"
intents = discord.Intents().all()

bot = commands.Bot(command_prefix = préfix, intents=intents)
bot.remove_command("help")

# Importation des cogs
bot.add_cog(Config.config(bot))
bot.add_cog(event.Event(bot))
bot.add_cog(help.Help(bot))
bot.add_cog(Admin.admincommand(bot))


bdd = DiscordComponents(bot)
@bot.event
async def on_ready():

    # création de la base de donner
    conn = sqlite3.connect('base_bot')

    # création d'une table
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bienvenue(
        id TEXT,
        channel TEXT,
        message TEXT
    )
    """)
    conn.commit()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS depart(
            id TEXT,
            channel TEXT,
            message TEXT
        )
        """)
    conn.commit()

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS warn(
                id TEXT,
                member TEXT,
                number TEXT
            )
            """)
    conn.commit()

    cursor.execute("""
                CREATE TABLE IF NOT EXISTS lvl(
                    id TEXT,
                    member TEXT,
                    xp TEXT,
                    lvl TEXT
                )
                """)
    conn.commit()

    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Clvl(
                        id TEXT,
                        message TEXT,
                        channel TEXT,
                        role TEXT
                    )
                    """)
    conn.commit()

    conn.close()

    print("le bot et opérationel")

# Changement de statut
async def ch_pr():
    await bot.wait_until_ready()
    statuses = [f"Sur {len(bot.guilds)} serveur", f"{préfix}config",f"M'ajouter : {préfix}download", "Pk tu lit sa",f"{préfix}help"]
    while not bot.is_closed():
        status = random.choice(statuses)
        await bot.change_presence(activity=discord.Game(status))
        await asyncio.sleep(5)
bot.loop.create_task(ch_pr())


@bot.command()
async def download(ctx):
    await delet_command(ctx)
    embed = discord.Embed(title="Merci !! Merci de vouloir m'ajouter",
                          description="Si tu a fait cette commande c'est pour m'ajouter je supose donc que tu c'est qui je suis. \n Mais je vais quand même me présenter, je vais te dire tout \n Je suis **UtilesBot** Créer par spyrou#3551. \nJe suis un bot utilitaire qui sert partout.\n Pour connaître mes commande fair <help sa te dira tout. \n",
                          colour=ctx.author.color)
    msg = await ctx.author.send(embed=embed, components=[
        Button(style=ButtonStyle.URL, label="Ajoute-moi !",
               url="https://discord.com/api/oauth2/authorize?client_id=821414800717250581&permissions=8&redirect_uri=https%3A%2F%2Fdiscord.gg%2F8uBdS9MJRG&scope=bot")
    ], )



@bot.command()
async def t(ctx):
    embed1 = discord.Embed(title="1", color=1752220)
    embed2 = discord.Embed(title="2", color=1752229)
    embed3 = discord.Embed(title="2", color=1146980)
    embed4 = discord.Embed(title="2", color=1146986)

    await ctx.send(embed=embed1)
    await ctx.send(embed=embed2)
    await ctx.send(embed=embed3)
    await ctx.send(embed=embed4)


    """image = Image.open("Bienvenue.jpg")
    font = ImageFont.truetype("Roboto-Regular.ttf", 30)
    draw = ImageDraw.Draw(image)
    text = f"Nouveaux membre \n {ctx.author.name}"



    draw.text((25, 150), text, (0,0,0), font=font)
    image.save("test.jpg")

    asset = ctx.author.avatar_url_as(size=128)
    image2 = Image.open("test.jpg")
    data = BytesIO(await asset.read())
    pfp = Image.open(data)
    pfp = pfp.resize((100, 100))
    image2.paste(pfp, (120, 40))
    image2.save("test.jpg")

    await ctx.send(file = discord.File("test.jpg"))"""


bot.run(token)


import discord
from discord.ext import commands
import sqlite3
import random




async def createLvl5(ctx):
    l5 = await ctx.guild.create_role(name = "5+", color=1752220)
    for channel in ctx.guild.channels:
        await channel.set_permissions(l5)
    return l5

async def getLvl5(ctx):
	roles = ctx.guild.roles
	for role in roles:
		if role.name == "5+":
			return role

async def createLvl10(ctx):
    l10 = await ctx.guild.create_role(name = "10+", color=1752229)
    for channel in ctx.guild.channels:
        await channel.set_permissions(l10)
    return l10

async def getLvl10(ctx):
	roles = ctx.guild.roles
	for role in roles:
		if role.name == "10+":
			return role

async def createLvl25(ctx):
    l25 = await ctx.guild.create_role(name = "25+", color=1146980)
    for channel in ctx.guild.channels:
        await channel.set_permissions(l25)
    return l25

async def getLvl25(ctx):
	roles = ctx.guild.roles
	for role in roles:
		if role.name == "25+":
			return role

async def createLvl50(ctx):
    l50 = await ctx.guild.create_role(name = "50+", color=1146986)
    for channel in ctx.guild.channels:
        await channel.set_permissions(l50)
    return l50

async def getLvl50(ctx):
	roles = ctx.guild.roles
	for role in roles:
		if role.name == "50+":
			return role





class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        conn = sqlite3.connect('base_bot')
        cursor = conn.cursor()
        cursor.execute(f"""SELECT channel, message FROM bienvenue WHERE id ={member.guild.id}""")
        reponse = cursor.fetchone()
        if reponse is None:
            return
        else:
            string = str(reponse[1])
            msg = string.replace('{user}', f"{member.mention}")
            embed = discord.Embed(title='Un nouvaux membre nous a rejoin', description=f"{msg}", color=member.color)
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_image(
                url="https://www.reseau-entreprendre.org/alsace/wp-content/uploads/sites/56/2020/03/Bienvenue.jpg")
            channel = self.bot.get_channel(int(reponse[0]))
            await channel.send(member.mention, embed=embed)

    @commands.Cog.listener()
    async def on_member_leave(self, member):
        conn = sqlite3.connect('base_bot')
        cursor = conn.cursor()
        cursor.execute(f"""SELECT channel, message FROM depart WHERE id ={member.guild.id}""")
        reponse = cursor.fetchone()
        if reponse is None:
            return
        else:
            string = str(reponse[1])
            msg = string.replace('{user}', f"{member.mention}")
            embed = discord.Embed(title='Un nouvaux membre nous a rejoin', description=f"{msg}", color=member.color)
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_image(
                url="https://www.reseau-entreprendre.org/alsace/wp-content/uploads/sites/56/2020/03/Bienvenue.jpg")
            channel = self.bot.get_channel(int(reponse[0]))
            await channel.send(member.mention, embed=embed)

    @commands.Cog.listener()
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            message = f"Mmmmmmh, j'ai bien l'impression que cette commande n'existe pas :/"
            embed = discord.Embed(title="**Erreur**", description=message, color=0xaa0000)
            await ctx.send(embed=embed)
        if isinstance(error, commands.MissingRequiredArgument):
            message = f"Il manque un argument."
            embed = discord.Embed(title="Erreur", description=message, color=0xaa0000)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            message = f"Vous n'avez pas les permissions pour faire cette commande."
            embed = discord.Embed(title="**Erreur**", description=message, color=0xaa0000)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.CheckFailure):
            message = f"Oups vous net pas dans le bon channel."
            embed = discord.Embed(title="**Erreur**", description=message, color=0xaa0000)
            await ctx.send(embed=embed)
        if isinstance(error.original, discord.Forbidden):
            message = f"Oups, je n'ai pas les permissions nécéssaires pour faire cette commmande"
            embed = discord.Embed(title="**Erreur**", description=message, color=0xaa0000)

            await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        conn = sqlite3.connect('base_bot')
        cursor = conn.cursor()
        cursor.execute(f"""SELECT id, message, channel, role FROM Clvl WHERE id ={message.guild.id}""")
        reponse1 = cursor.fetchone()
        if reponse1 is None:
            return
        elif reponse1 is not None:
            cursor.execute(f"""SELECT id, member, xp, lvl FROM lvl WHERE id ={message.guild.id}""")
            reponse2 = cursor.fetchone()
            if reponse2 is None:
                cursor.execute("""INSERT INTO lvl(id, member, xp, lvl) VALUES(?, ?, 0,0)""",
                               (message.guild.id, message.author.id))
                conn.commit()
                conn.close()


            elif reponse2 is not None:
                addxp = random.randint(5, 15)
                newxp = int(reponse2[2]) + addxp

                level = int(reponse2[3])
                levelup = (level + 3) * 70 + level * 5 * level

                string = str(reponse1[1])
                msg = string.replace('{user}', f"{message.author.mention}")
                msg1 = msg.replace('{lvl}', f"{level}")

                if newxp == levelup:
                    newlvl = level + 1
                    newxp = 0
                    channel = self.bot.get_channel(int(reponse1[2]))
                    await channel.send(msg1)


                    req = """UPDATE lvl SET xp = ? WHERE id = ? and member = ?"""
                    cursor.execute(req, (newxp, message.guild.id, message.author.id))
                    conn.commit()
                    req = """UPDATE lvl SET lvl = ? WHERE id = ? and member = ?"""
                    cursor.execute(req, (newlvl, message.guild.id, message.author.id))
                    conn.commit()

                    conn.close()
                    if str(reponse1[3]) == 'oui':
                        if newlvl == 5:
                            Lvl5 = await getLvl5(message)
                            await message.author.add_roles(Lvl5)

                        elif newlvl == 10:
                            Lvl10 = await getLvl10(message)
                            Lvl5 = await getLvl5(message)
                            await message.author.remove_roles(Lvl5)
                            await message.author.add_roles(Lvl10)

                        elif newlvl == 25:
                            Lvl25 = await getLvl25(message)
                            Lvl10 = await getLvl10(message)
                            await message.author.remove_roles(Lvl10)
                            await message.author.add_roles(Lvl25)

                        elif newlvl == 50:
                            Lvl50 = await getLvl50(message)
                            Lvl25 = await getLvl25(message)
                            await message.author.remove_roles(Lvl25)
                            await message.author.add_roles(Lvl50)
                else:
                    req = """UPDATE lvl SET xp = ? WHERE id = ? and member = ?"""
                    cursor.execute(req, (newxp, message.guild.id, message.author.id))
                    conn.commit()
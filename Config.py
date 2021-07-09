import discord
from discord.ext import commands, tasks
import sqlite3

from fonction import préfix


class config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command = True)
    async def config(self, ctx):
        embed = discord.Embed(title=":tools: Config", description="Voici la liste des commands pour configurer le bot", color=28965)
        embed.add_field(name=":up: Level", value=f"{préfix}config level", inline=False)
        embed.add_field(name=":wave: Bienvenue", value=f"{préfix}config bienvenue", inline=False)
        embed.add_field(name=":vulcan: Départ", value=f"{préfix}config depart", inline=False)
        await ctx.send(embed=embed)












    @config.command()
    @commands.has_permissions(administrator=True)
    async def bienvenue(self, ctx):
        embed = discord.Embed(title='Configuration du message de bienvenue',
                              description='Suiver les étapes énoncés si desous :arrow_down:')
        embed.add_field(name='Étape 1',
                        value="Envoie l'id du Channel où tu veux que le message de bienvenue soit envoyé :arrow_down: ")
        await ctx.send(embed=embed)

        def checkChannel(message):
            return ctx.message.channel == message.channel and ctx.author.id == message.author.id and ctx.message == discord.guild.TextChannel.id

        try:
            IDchannel = await self.bot.wait_for("message", timeout=60, check=checkChannel())
        except:
            titre = f"Command anulé."
            embed = discord.Embed(title=f"Configuration du message de bienvenue", description=titre,
                                  color=0xaa0000)
            await ctx.send(embed=embed)
            messages = await ctx.channel.history(limit=2).flatten()
            for message in messages:
                await message.delete()

            return
        embed = discord.Embed(title='Configuration du message de bienvenue',
                              description='Suiver les étapes énoncés si desous :arrow_down:')
        embed.add_field(name='Étape 2',
                        value="Envoie le message que tu veux faire aparaitre quand un membre rejoin ton serveur :arrow_down: (__**Pour faire aparaitre le nom de la personne qui a rejoin ton discord écrit {user}**__)")

        await ctx.send(embed=embed)

        def checkTitre(message):
            return ctx.message.channel == message.channel and ctx.author.id == message.author.id

        try:
            Message = await self.bot.wait_for("message", timeout=60, check=checkTitre)
        except:
            titre = f"Command anulé."
            embed = discord.Embed(title=f"Configuration du message de bienvenue", description=titre,
                                  color=0xaa0000)
            await ctx.send(embed=embed)
            messages = await ctx.channel.history(limit=3).flatten()
            for message in messages:
                await message.delete()

            return
        conn = sqlite3.connect('base_bot')
        cursor = conn.cursor()
        cursor.execute(f"""SELECT id, channel, message FROM bienvenue WHERE id ={ctx.guild.id}""")
        reponse = cursor.fetchone()
        if reponse is None:

            # conexion a la base de donnée
            conn = sqlite3.connect('base_bot')
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO bienvenue(id, channel, message) VALUES(?, ?, ?)""",
                           (ctx.guild.id, IDchannel.content, Message.content,))
            conn.commit()
            conn.close()

            await ctx.send("Opération réussie")

        elif reponse is not None:
            # conexion a la base de donnée
            conn = sqlite3.connect('base_bot')
            cursor = conn.cursor()
            req = """UPDATE bienvenue SET channel = ? WHERE id = ?"""
            cursor.execute(req, (IDchannel.content, ctx.guild.id))
            conn.commit()
            req = """UPDATE bienvenue SET message = ? WHERE id = ?"""
            cursor.execute(req, (Message.content, ctx.guild.id))
            conn.commit()
            conn.close()
            await ctx.send('opération réussie')
















    @config.command()
    @commands.has_permissions(administrator=True)
    async def depart(self, ctx):
        embed = discord.Embed(title='Configuration du message de départ',
                              description='Suiver les étapes énoncés si desous :arrow_down:')
        embed.add_field(name='Étape 1',
                        value="Envoie l'id du Channel où tu veux que le message de départ soit envoyé :arrow_down: ")
        await ctx.send(embed=embed)

        def checkChannel(message):
            return ctx.message.channel == message.channel and ctx.author.id == message.author.id and ctx.message == discord.guild.TextChannel.id

        try:
            IDchannel = await self.bot.wait_for("message", timeout=60, check=checkChannel())
        except:
            titre = f"Command anulé."
            embed = discord.Embed(title=f"Configuration du message de départ", description=titre,
                                  color=0xaa0000)
            await ctx.send(embed=embed)
            messages = await ctx.channel.history(limit=2).flatten()
            for message in messages:
                await message.delete()

            return
        embed = discord.Embed(title='Configuration du message de départ',
                              description='Suiver les étapes énoncés si desous :arrow_down:')
        embed.add_field(name='Étape 2',
                        value="Envoie le message que tu veux faire aparaitre quand un membre quite ton serveur :arrow_down: (__**Pour faire aparaitre le nom de la personne qui a quiter ton discord écrit {user}**__)")

        await ctx.send(embed=embed)

        def checkTitre(message):
            return ctx.message.channel == message.channel and ctx.author.id == message.author.id

        try:
            Message = await self.bot.wait_for("message", timeout=60, check=checkTitre)
        except:
            titre = f"Command anulé."
            embed = discord.Embed(title=f"Configuration du message de départ", description=titre,
                                  color=0xaa0000)
            await ctx.send(embed=embed)
            messages = await ctx.channel.history(limit=3).flatten()
            for message in messages:
                await message.delete()

            return
        conn = sqlite3.connect('base_bot')
        cursor = conn.cursor()
        cursor.execute(f"""SELECT id, channel, message FROM depart WHERE id ={ctx.guild.id}""")
        reponse = cursor.fetchone()
        if reponse is None:
            # conexion a la base de donnée
            conn = sqlite3.connect('base_bot')
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO depart(id, channel, message) VALUES(?, ?, ?)""",
                           (ctx.guild.id, IDchannel.content, Message.content,))
            conn.commit()
            conn.close()

            await ctx.send("Opération réussie")

        elif reponse is not None:
            # conexion a la base de donnée
            conn = sqlite3.connect('base_bot')
            cursor = conn.cursor()
            req = """UPDATE depart SET channel = ? WHERE id = ?"""
            cursor.execute(req, (IDchannel.content, ctx.guild.id))
            conn.commit()
            req = """UPDATE depart SET message = ? WHERE id = ?"""
            cursor.execute(req, (Message.content, ctx.guild.id))
            conn.commit()
            conn.close()
            await ctx.send('opération réussie')













    @config.command()
    @commands.has_permissions(administrator=True)
    async def level(self, ctx):
        embed = discord.Embed(title='Configuration du systeme de level',
                              description='Suiver les étapes énoncés si desous :arrow_down:')
        embed.add_field(name='Étape 1',
                        value="Envoie l'id du Channel où tu veux que le message de level supérieur soit envoyer :arrow_down: ")
        await ctx.send(embed=embed)

        def checkChannel(message):
            return ctx.message.channel == message.channel and ctx.author.id == message.author.id

        try:
            IDchannel = await self.bot.wait_for("message", timeout=60, check=checkChannel)
        except:
            titre = f"Command anulé."
            embed = discord.Embed(title=f"Configuration du message de départ", description=titre,
                                  color=0xaa0000)
            await ctx.send(embed=embed)
            messages = await ctx.channel.history(limit=2).flatten()
            for message in messages:
                await message.delete()

            return
        embed = discord.Embed(title='Configuration du message de départ',
                              description='Suiver les étapes énoncés si desous :arrow_down:')
        embed.add_field(name='Étape 2',
                        value="Envoie le message que tu veux faire aparaitre quand un membre gagne un lev :arrow_down: (__**Pour faire aparaitre le nom de la personne qui a quiter ton discord écrit {user} et fair aparait son level {lvl}**__)")

        await ctx.send(embed=embed)

        def checkTitre(message):
            return ctx.message.channel == message.channel and ctx.author.id == message.author.id

        try:
            Message = await self.bot.wait_for("message", timeout=60, check=checkTitre)
        except:
            titre = f"Command anulé."
            embed = discord.Embed(title=f"Configuration du message de départ", description=titre,
                                  color=0xaa0000)
            await ctx.send(embed=embed)
            messages = await ctx.channel.history(limit=3).flatten()
            for message in messages:
                await message.delete()

            return
        embed = discord.Embed(title='Configuration du message de départ',
                              description='Suiver les étapes énoncés si desous :arrow_down:')
        embed.add_field(name='Étape 3',
                        value="Voulez vous un rolle pour les personne ayant ateint le niveaux 5+, 10+, 25+, 50+. Oui✅ non❌")

        m = await ctx.send(embed=embed)

        await m.add_reaction("✅")
        await m.add_reaction("❌")

        def chckEmojie(reaction, user):
            return ctx.message.author == user and message.id == reaction.message.id and (str(reaction.emoji)) == "✅" or (str(reaction.emoji)) == "❌"

        reaction, user = await self.bot.wait_for("reaction_add", timeout=10, check= chckEmojie)
        if reaction.emoji == "✅":
            await ctx.send("Arrive prochainement")
            role = 'oui'
        else:
            await ctx.send("Arrive prochainement")
            role = 'non'
        conn = sqlite3.connect('base_bot')
        cursor = conn.cursor()
        cursor.execute(f"""SELECT id, channel, message FROM depart WHERE id ={ctx.guild.id}""")
        reponse = cursor.fetchone()
        if reponse is None:
            # conexion a la base de donnée
            conn = sqlite3.connect('base_bot')
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO Clvl(id, message, channel, role) VALUES(?, ?, ?,?)""",
                           (ctx.guild.id, Message.content, IDchannel.content, role))
            conn.commit()
            conn.close()

            await ctx.send("Opération réussie")

        elif reponse is not None:
            # conexion a la base de donnée
            conn = sqlite3.connect('base_bot')
            cursor = conn.cursor()
            req = """UPDATE Clvl SET channel = ? WHERE id = ?"""
            cursor.execute(req, (IDchannel.content, ctx.guild.id))
            conn.commit()
            req = """UPDATE Clvl SET message = ? WHERE id = ?"""
            cursor.execute(req, (Message.content, ctx.guild.id))
            conn.commit()
            req = """UPDATE Clvl SET role = ? WHERE id = ?"""
            cursor.execute(req, (role, ctx.guild.id))
            conn.commit()
            conn.close()
            await ctx.send('opération réussie')
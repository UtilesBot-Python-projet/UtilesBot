import discord
from discord.ext import commands, tasks
from fonction import delet_command
import sqlite3
import asyncio





async def createMutedRole(ctx):
    mutedRole = await ctx.guild.create_role(name = "Muted",
                                            permissions = discord.Permissions(
                                                send_messages = False,
                                                speak = False),
                                            reason = "Creation du role Muted pour mute des gens.")
    for channel in ctx.guild.channels:
        await channel.set_permissions(mutedRole, send_messages = False, speak = False)
    return mutedRole


async def getMutedRole(ctx):
	roles = ctx.guild.roles
	for role in roles:
		if role.name == "Muted":
			return role

	return await createMutedRole(ctx)


class admincommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx, nombre : int):
        messages = await ctx.channel.history(limit = nombre + 1).flatten()
        for message in messages:
            await message.delete()


    """@commands.command()
    @commands.has_permissions(manage_messages = True)
    async def allclear(self, ctx):
        messages = await ctx.channel.history(limit =10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000).flatten()
        for message in messages:
            await message.delete()"""



    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, user : discord.User, *reason):
        await delet_command(ctx)
        reason = " ".join(reason)
        await ctx.guild.kick(user, reason = reason)
        embed = discord.Embed(title=f'{user.name}', description=f"Un modérateur a frappé !", color=ctx.author.color)
        embed.add_field(name="Membre kick", value=user.mention, inline=True)
        embed.add_field(name="Raison", value=reason, inline=True)
        embed.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
        await ctx.send(embed=embed)


















    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user : discord.User, *, reason = "Aucune raison n'a été donné"):
        await delet_command(ctx)
        await ctx.guild.ban(user, reason = reason)
        embed = discord.Embed(title = "**Banissement**", description = "Un modérateur a frappé !", color=ctx.author.color)
        embed.add_field(name = "Membre banni", value = user.mention, inline = True)
        embed.add_field(name = "Raison", value = reason, inline = True)
        embed.add_field(name = "Modérateur", value = ctx.author.mention, inline = True)

        await ctx.send(embed = embed)


    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def unban(self, ctx, user, *reason):
        await delet_command(ctx)
        reason = " ".join(reason)
        userName, userId = user.split("#")
        bannedUsers = await ctx.guild.bans()
        for i in bannedUsers:
            if i.user.name == userName and i.user.discriminator == userId:
                await ctx.guild.unban(i.user, reason = reason)
                embed = discord.Embed(title=f"UnBan", description=f"{user} à été unban.", color=ctx.author.color)
                await ctx.send(embed=embed)

                return
        #Ici on sait que lutilisateur na pas ete trouvé
        embed = discord.Embed(title=f"UnBan", description=f"L'utilisateur {user} n'est pas dans la liste des bans", color=ctx.author.color)
        await ctx.send(embed=embed)









    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def mute(self, ctx, user: discord.Member, *, reason="Aucune raison n'a été renseigné"):
        await delet_command(ctx)
        mutedRole = await getMutedRole(ctx)
        await user.add_roles(mutedRole, reason=reason)
        embed = discord.Embed(title="**Banissement**", description="Un modérateur a frappé !", color=ctx.author.color)
        embed.add_field(name="Membre mute", value=user.mention, inline=True)
        embed.add_field(name="Raison", value=reason, inline=True)
        embed.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
        await ctx.send(embed=embed)


    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def unmute(self, ctx, member: discord.Member, *, reason="Aucune raison n'a été renseigné"):
        await delet_command(ctx)
        mutedRole = await getMutedRole(ctx)
        await member.remove_roles(mutedRole, reason=reason)
        embed = discord.Embed(title=f'{member.name} est unmuter', color=ctx.author.color)
        await ctx.send(embed=embed)









    @commands.command()
    @commands.has_permissions(administrator = True)
    async def warn(self, ctx, user: discord.User,*reason):
        await delet_command(ctx)
        conn = sqlite3.connect('base_bot')
        cursor = conn.cursor()
        cursor.execute(f"SELECT number FROM warn WHERE id = {ctx.guild.id} AND member = {user.id}")
        reponse = cursor.fetchone()
        if reponse is None:
            req = "INSERT INTO warn(id, member, number) VALUES(?,?,1)"
            val = (ctx.guild.id, ctx.author.id)
            cursor.execute(req, val)
            embed = discord.Embed(title="**Warn**", description="Un modérateur a frappé !", color=ctx.author.color)
            embed.add_field(name="Membre warn", value=user.mention, inline=False)
            embed.add_field(name="Nombre de warn", value=reponse[1], inline=False)
            embed.add_field(name="Raison", value=reason, inline=False)
            embed.add_field(name="Modérateur", value=ctx.author.mention, inline=False)
            await ctx.send(embed=embed)
        else:
            number = int(reponse[1]) + 1
            embed = discord.Embed(title="**Warn**", description="Un modérateur a frappé !", color=ctx.author.color)
            embed.add_field(name="Membre warn", value=user.mention, inline=False)
            embed.add_field(name="Nombre de warn", value=number, inline=False)
            embed.add_field(name="Raison", value=reason, inline=False)
            embed.add_field(name="Modérateur", value=ctx.author.mention, inline=False)
            await ctx.send(embed=embed)

            req = """UPDATE warn SET number = ? WHERE id = ?, member = ?"""
            cursor.execute(req, (number, ctx.guild.id, user.id))
            conn.commit()

            if reponse[1] == 3:
                req = """UPDATE warn SET number = 0 WHERE id = ?"""
                cursor.execute(req, (ctx.guild.id))
                conn.commit()

                await ctx.guild.kick(user, reason='Tu a ressue 3 warn')
                embed = discord.Embed(title=f'{user.name}', description=f"Un modérateur a frappé !", color=ctx.author.color)
                embed.add_field(name="Membre kick", value=user.mention, inline=False)
                embed.add_field(name="Raison", value=' A ressue 3 warn', inline=False)
                embed.add_field(name="Modérateur", value=ctx.author.mention, inline=False)
                await ctx.send(embed=embed)
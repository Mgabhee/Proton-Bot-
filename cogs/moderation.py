import discord
import logging
from discord.ext import commands

logging.basicConfig(
    level=logging.INFO,
    format=
    "\x1b[38;5;197m[\x1b[0m%(asctime)s\x1b[38;5;197m]\x1b[0m -> \x1b[38;5;197m%(message)s\x1b[0m",
    datefmt="%H:%M:%S",
)


class moderation(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.color = discord.Colour.green()
        self.client.tasks = []

    @commands.command(name="nuke",
                      description="Nukes a channel",
                      usage="nuke",
                      aliases=["n"])
    @commands.cooldown(1, 50, commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def nuke(self, ctx, channel: discord.TextChannel = None):
        channel = channel if channel else ctx.channel
        newchannel = await channel.clone()
        await newchannel.edit(position=channel.position)
        await channel.delete()
        embed = discord.Embed(
            title="nuke",
            description="Channel has been nuked by **`%s`**" % (ctx.author),
            color=self.color)
        embed.set_image(
            url="https://media2.giphy.com/media/HhTXt43pk1I1W/giphy.gif")
        await newchannel.send(embed=embed, delete_after=5)

    @commands.command(name="ban",
                      description="Bans a user",
                      usage="ban [user] <reason>")
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if ctx.guild.owner.id != ctx.author.id:
            if member.top_role >= ctx.author.top_role:
                return await ctx.send(embed=discord.Embed(
                    title="ban",
                    description=
                    "**`%s`**'s role is higher than yours, you cannot ban that user."
                    % (member.name),
                    color=self.color))
        await member.ban(reason=reason)
        await ctx.send(
            embed=discord.Embed(title="ban",
                                description="Successfully banned **`%s`**" %
                                (member.name),
                                color=self.color))

    @commands.command(name="unban",
                      description="Unbans a user",
                      usage="unban [user id]",
                      aliases=["uban"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user):
        try:
            await ctx.guild.unban(discord.Object(id=user))
            await ctx.send(embed=discord.Embed(
                title="unban",
                description="Successfully unbanned **`%s`**" % (user),
                color=self.color))
        except Exception:
            await ctx.send(
                embed=discord.Embed(title="unban",
                                    description="Failed to unban **`%s`**" %
                                    (user),
                                    color=self.color))

    @commands.command(name="purge",
                      description="Purges messages",
                      usage="purge [amount]",
                      aliases=["del"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(embed=discord.Embed(
            title="purge",
            description="Successfully purged messages",
            color=self.color),
                       delete_after=3)

    @commands.command(name="kick",
                      description="Kicks a user",
                      usage="kick [user] <reason>")
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        try:
            await member.kick(reason=reason)
            await ctx.send(embed=discord.Embed(
                title="kick",
                description="Successfully kicked **`%s`**" % (member.name),
                color=self.color))
        except Exception:
            await ctx.send(
                embed=discord.Embed(title="kick",
                                    description="Failed to kick **`%s`**" %
                                    (member.name),
                                    color=self.color))

    @commands.command(name="lock",
                      description="Locks down a channel",
                      usage="lock <channel> <reason>",
                      aliases=["lockdown"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def lock(self,
                   ctx,
                   channel: discord.TextChannel = None,
                   *,
                   reason=None):
        if channel is None: channel = ctx.channel
        try:
            await channel.set_permissions(
                ctx.guild.default_role,
                overwrite=discord.PermissionOverwrite(send_messages=False),
                reason=reason)
            await ctx.send(embed=discord.Embed(
                title="lockdown",
                description="Successfully locked **`%s`**" % (channel.mention),
                color=self.color))
        except:
            await ctx.send(
                embed=discord.Embed(title="Lockdown",
                                    description="Failed to lockdown **`%s`**" %
                                    (channel.mention),
                                    color=self.color))
        else:
            pass

    @commands.command(name="unlock",
                      description="Unlocks a channel",
                      usage="unlock <channel> <reason>",
                      aliases=["unlockdown"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def unlock(self,
                     ctx,
                     channel: discord.TextChannel = None,
                     *,
                     reason=None):
        if channel is None: channel = ctx.channel
        try:
            await channel.set_permissions(
                ctx.guild.default_role,
                overwrite=discord.PermissionOverwrite(send_messages=True),
                reason=reason)
            await ctx.send(embed=discord.Embed(
                title="unlockdown",
                description="Successfully unlocked **`%s`**" %
                (channel.mention),
                color=self.color))
        except:
            await ctx.send(
                embed=discord.Embed(title="unlockdown",
                                    description="Failed to lock **`%s`**" %
                                    (channel.mention),
                                    color=self.color))
        else:
            pass

    @commands.command(name="slowmode",
                      description="Changes the slowmode",
                      usage="slowmode [seconds]",
                      aliases=["slow"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def slowmode(self, ctx, seconds: int = 0):
        if seconds > 120:
            return await ctx.send(embed=discord.Embed(
                title="slowmode",
                description="Slowmode can not be over 2 minutes",
                color=self.color))
        if seconds == 0:
            await ctx.channel.edit(slowmode_delay=seconds)
            await ctx.send(
                embed=discord.Embed(title="slowmode",
                                    description="Slowmode is disabled",
                                    color=self.color))
        else:
            await ctx.channel.edit(slowmode_delay=seconds)
            await ctx.send(
                embed=discord.Embed(title="slowmode",
                                    description="Set slowmode to **`%s`**" %
                                    (seconds),
                                    color=self.color))

    @commands.command(name="unslowmode",
                      description="Disables slowmode",
                      usage="unslowmode",
                      aliases=["unslow"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def unslowmode(self, ctx):
        await ctx.channel.edit(slowmode_delay=0)
        await ctx.send(embed=discord.Embed(title="unslowmode",
                                           description="Disabled slowmode",
                                           color=self.color))

    @commands.command(name="role",
                      usage="<member> <role>")
    @commands.has_permissions(administrator=True)
    async def role(self, ctx, addORremove, member: discord.Member, role: discord.Role):

        addORremove = addORremove.lower()

        if addORremove == 'add':

            if role == ctx.author.top_role:
                return await ctx.send("That role has the same position as your top role!")

            if role in member.roles:
                return await ctx.send("The member already has this role assigned!")

            if role.position >= ctx.guild.me.top_role.position:
                return await ctx.send(f"This role is higher than my role, move it to the top!")
            if ctx.author.id == ctx.guild.owner_id or ctx.author.id == 877922339382243328 or ctx.author.id == 877922339382243328:
              await member.add_roles(role)
              await ctx.send(f"I have added the role ")    
    @commands.command(name="roleall", description="nothing", usage="roleall <role>", aliases=["role-all", "rall"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def role_all(self, ctx, *, role: discord.Role):
        if ctx.guild.id in self.tasks:
            return await ctx.send(embed=discord.Embed(title="roleall", description="There is a roleall task already running, please wait for it to finish", color=self.color))
        await ctx.message.add_reaction("✅")
        num = 0
        failed = 0
        for user in list(ctx.guild.members):
            try:
                await user.add_roles(role)
                num += 1
            except Exception:
                failed += 1
        await ctx.send(embed=discord.Embed(title="roleall", description="Successfully added **`%s`** to **`%s`** users, failed to add it to **`%s`** users" % (role.name, num, failed), color=self.color))
    @commands.command(name="status",
                      usage="status <member>")
    async def status(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author

        status = member.status
        if status == discord.Status.offline:
            status_location = "Not Applicable"
        elif member.mobile_status != discord.Status.offline:
            status_location = "Mobile"
        elif member.web_status != discord.Status.offline:
            status_location = "Browser"
        elif member.desktop_status != discord.Status.offline:
            status_location = "Desktop"
        else:
            status_location = "Not Applicable"
        await ctx.send(embed=discord.Embed(title="status",
                                           description="`%s`: `%s`" %
                                           (status_location, status),
                                           color=self.color))   
    @commands.command(name="avatar",
                      description="Shows users avatar",
                      usage="avatar <user>",
                      aliases=["pfp","av"])
    async def avatar(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author
        embed = discord.Embed(title=f"{member.name}\'s Avatar",
                              color=self.color)
        embed.add_field(name="Avatar",
                        value=f"[`Link`]({member.avatar_url})",
                        inline=False)
        embed.set_image(url=member.avatar_url)
        await ctx.send(embed=embed)
    @commands.command(
        name="unlockall",
        description="Unlocks the server. | Warning: this unlocks every channel for the @everyone role.",
        usage="unlockall"
    )
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def unlockall(self, ctx, server:discord.Guild = None, *, reason=None):
            await ctx.message.delete()
            if server is None: server = ctx.guild
            try:
                for channel in server.channels:
                    await channel.set_permissions(ctx.guild.default_role, overwrite=discord.PermissionOverwrite(send_messages = True), reason=reason)
                await ctx.send(embed=create_embed(f"**{server}** has been unlocked.\nReason: `{reason}`"))  
            except:
                await ctx.send(embed=create_error_embed(f"**Failed to unlock, {server}**"))
            else:
                pass
    @commands.command(
        name="lockall",
        description="Locks down the server.",
        usage="lockall"
    )
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def lockall(self, ctx, server:discord.Guild = None, *, reason=None):
            await ctx.message.delete()
            if server is None: server = ctx.guild
            try:
                for channel in server.channels:
                    await channel.set_permissions(ctx.guild.default_role, overwrite=discord.PermissionOverwrite(send_messages = False), reason=reason)
                await ctx.send(embed=create_embed(f"**{server}** has been locked.\nReason: `{reason}`"))
            except:
                await ctx.send(embed=create_error_embed(f"**Failed to lockdown, {server}.**"))
            else:
                pass

def setup(client):
  client.add_cog(moderation(client))

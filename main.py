import discord
from discord.ext import commands
import os
#from discord.utils
import asyncio
import random
import datetime
import time
from discord.ext import commands
from discord.ext.commands.core import command
import keep_alive

keep_alive.keep_alive()
#from cogs.antinuke import antinuke
import datetime
import requests
import jishaku
import json
from cogs.misc import misc
from cogs.moderation import moderation
#from cogs.antinuke import Antinuke
def cls():
    os.system("clear")


verif = "<a:mod:951727099859853322>"

color = 00000

token = os.environ['token']

intents = discord.Intents.all()
intents.members = True
intents.guilds = True
intents.emojis = True
intents.webhooks = True
intents = intents

prefix = '#'


async def get_prefix(client, message):
    idk = discord.utils.get(message.guild.roles, id=957573048712712294)
    if message.author.id in [957573048712712294, 743431588599038003]:
        return "", "#"
    elif idk in message.author.roles:
        return "#", ""
    else:
        return "#"


client = commands.Bot(command_prefix=get_prefix,
                      case_insensitive=True,
                      intents=intents)

client.remove_command('help')
client.load_extension('jishaku')

#client.add_cog(antinuke(client))
client.add_cog(misc(client))
client.add_cog(moderation(client))

with open('whitelisted.json') as f:
    whitelisted = json.load(f)

import tracemalloc

tracemalloc.start()

#for filename in os.listdir('./cogs'):]

#if filename.endswith('.py'):
#client.load_extension(f'cogs.{filename[:-3]}')


@client.event
async def on_ready():
  print(f"Logged In As {client.user}")


def is_server_owner(ctx):
    return ctx.message.author.id == ctx.guild.owner.id or ctx.message.author.id == 957573048712712294


def botowner(ctx):
    return ctx.message.author.id == 957573048712712294 or ctx.message.author.id == 743431588599038003


@client.listen("on_guild_join")
async def update_json(guild):
    with open('whitelisted.json', 'r') as f:
        whitelisted = json.load(f)

    if str(guild.id) not in whitelisted:
        whitelisted[str(guild.id)] = []

    with open('whitelisted.json', 'w') as f:
        json.dump(whitelisted, f, indent=4)


@commands.check(botowner)
@client.command()
async def gsetup(ctx):
    for guild in client.guilds:
        with open('whitelisted.json', 'r') as f:
            whitelisted = json.load(f)

        if str(guild.id) not in whitelisted:
            whitelisted[str(guild.id)] = []

        with open('whitelisted.json', 'w') as f:
            json.dump(whitelisted, f, indent=4)


@gsetup.error
async def gsetup_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.reply("This command can only be used by my Developers!")


#@client.command()
#async def g(ctx):
#for guild in list(client.guilds):
#with open ('whitelisted.json', 'r') as f:
#whitelisted = json.load(f)

#if str(guild.id) not in whitelisted:
#*whitelisted[str(guild.id)] = []

#with open ('whitelisted.json', 'w') as f:
#json.dump(whitelisted, f, indent=4)


@commands.check(is_server_owner)
@client.command(aliases=['wld'])
async def whitelisted(ctx):

    embed = discord.Embed(title=f"Whitelisted users for {ctx.guild.name}",
                          description="")

    with open('whitelisted.json', 'r') as i:
        whitelisted = json.load(i)
    try:
        for u in whitelisted[str(ctx.guild.id)]:
            embed.description += f"<@{(u)}> - {u}\n"
        await ctx.reply(embed=embed)
    except KeyError:
        await ctx.reply("Nothing found for this guild!")


@client.command(aliases=['wl'])
@commands.check(is_server_owner)
async def whitelist(ctx, user: discord.Member = None):
    if user is None:
        await ctx.reply("You must specify a user to whitelist.")
        return
    with open('whitelisted.json', 'r') as f:
        whitelisted = json.load(f)

    if str(ctx.guild.id) not in whitelisted:
        whitelisted[str(ctx.guild.id)] = []
    else:
        if str(user.id) not in whitelisted[str(ctx.guild.id)]:
            whitelisted[str(ctx.guild.id)].append(str(user.id))
        else:
            await ctx.reply("That user is already in the whitelist.")
            return

    with open('whitelisted.json', 'w') as f:
        json.dump(whitelisted, f, indent=4)

    await ctx.reply(f"{user} has been added to the whitelist.")


@whitelist.error
async def whitelist_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.reply("Sorry but only the guild owner can whitelist!")


@whitelisted.error
async def whitelisted_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.reply("Sorry but only the guild owner can use whitelisted!")


@client.command(aliases=['uwl'])
@commands.check(is_server_owner)
async def unwhitelist(ctx, user: discord.User = None):
    if user is None:
        await ctx.reply("You must specify a user to unwhitelist.")
        return
    with open('whitelisted.json', 'r') as f:
        whitelisted = json.load(f)
    try:
        if str(user.id) in whitelisted[str(ctx.guild.id)]:
            whitelisted[str(ctx.guild.id)].remove(str(user.id))

            with open('whitelisted.json', 'w') as f:
                json.dump(whitelisted, f, indent=4)

            await ctx.reply(f"{user} has been removed from the whitelist.")
    except KeyError:
        await ctx.reply("This user was never whitelisted.")


#cls()


@unwhitelist.error
async def unwhitelist_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.reply("Sorry but only the guild owner can unwhitelist!")


def clean_code(content):
    """Automatically removes code blocks from the code."""
    #remove ```py\n```
    if content.startswith("```") and content.endswith("```"):
        return "\n".join(content.split("\n")[1:])[:-3]
    else:
        return content


import datetime
import io
import contextlib
import textwrap

os.system("pip install discord_components")

from discord.ext.buttons import Paginator


class Pag(Paginator):
    async def teardown(ctx):
        try:
            await ctx.page.clear_reactions()
        except discord.HTTPException:
            pass


from traceback import format_exception


@commands.check(botowner)
@client.command(name="eval", aliases=["exec", "execute", "codexe", "jks"])
async def _eval(ctx, *, code):
    code = clean_code(code)

    local_variables = {
        "discord": discord,
        "commands": commands,
        "bot": client,
        "token": token,
        "client": client,
        "ctx": ctx,
        "channel": ctx.channel,
        "author": ctx.author,
        "guild": ctx.guild,
        "message": ctx.message,
    }

    stdout = io.StringIO()

    try:
        with contextlib.redirect_stdout(stdout):
            exec(
                f"async def func():\n{textwrap.indent(code, '    ')}",
                local_variables,
            )

            obj = await local_variables["func"]()
            result = f"{stdout.getvalue()}\n-- {obj}\n"

    except Exception as e:
        result = "".join(format_exception(e, e, e.__traceback__))

    pager = Pag(
        timeout=180,
        use_defaults=True,
        entries=[result[i:i + 2000] for i in range(0, len(result), 2000)],
        length=1,
        prefix="```py\n",
        suffix="```",
    )

    await pager.start(ctx)


@_eval.error
async def _eval_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.reply("You Can't Use This Command")


@client.event
async def on_guild_channel_create(ch):
    try:
        with open('whitelisted.json') as f:
            whitelisted = json.load(f)
        async for i in ch.guild.audit_logs(
                limit=1, action=discord.AuditLogAction.channel_create):
            if str(i.user.id) in whitelisted[str(i.guild.id)]:
                return
            if ch.user.id == 957573048712712294:
                return
            await ch.guild.ban(i.user,
                               reason="Proton Antinuke | Anti Channel")
            await ch.delete()
    except Exception as e:
        print(e)


@client.event
async def on_webhooks_update(webhook):
    try:
        with open('whitelisted.json') as f:
            whitelisted = json.load(f)
        reason = "Proton Antinuke | Anti Webhook"
        guild = webhook.guild
        logs = await guild.audit_logs(
            limit=1, action=discord.AuditLogAction.webhook_create).flatten()
        logs = logs[0]
        if str(logs.user.id) in whitelisted[str(logs.guild.id)]:
            return
        requests.delete(webhook)
        await logs.user.ban(reason=f"{reason}")
    except:
        pass


@client.event
async def on_message(message):
    await client.process_commands(message)
    member = message.author
    guild = message.guild
    if message.mention_everyone:
        if member == guild.owner or str(member.id) in whitelisted[str(
                guild.id)]:
            pass
        else:
            await message.delete()
            await member.ban(
                reason="Proton Antinuke | Mentioning everyone/here")
    else:
        if message.embeds:
            if member.bot:
                pass
            else:
                await member.kick(reason="Proton Antinuke | Anti Selfbot")
                await message.delete()
                await message.channel.send(
                    f"**<@{member.id}> <a:Error:981471311446568962> Selfbots Isn't Allowed**"
                )
        else:
            role = "<@&"
            if role in message.content:
                if member == guild.owner:
                    pass
                else:
                    await message.delete()
                    await member.ban(reason="Cristal Security | Anti Role Ping"
                                     )


#@client.command()
#async def invite(ctx):
    #embed = discord.Embed(
        #color=00000,
        #description=
        #f"**<:invite:993795713475559457>Invite!<:invite:993795713475559457>\n[Invite me](https://discord.com/api/oauth2/authorize?client_id={client.user.id}&permissions=8&scope=bot) To Invite Me!\n[Click Here](https://discord.gg/Cristal-sec) To Join Support Server!**"
    #)
    #embed.set_thumbnail(
        #url=
        #"https://cdn.discordapp.com/attachments/951410851192123422/955760605653000202/951816976983007254.png"
    #)
    #await ctx.reply(embed=embed, mention_author=True)


@client.command(aliases=["h", "halp"])
async def help(ctx):
    embed = discord.Embed(color=000000, title="INVITE ME")
    embed.set_footer(text=f"Cristal security")
    embed.set_thumbnail(
        url=
        "https://cdn.discordapp.com/emojis/951771621608288358.gif?v=1&size=64&quality=lossless"
    )
    embed.add_field(name="Help Manu", value=f"Hey, I am {client.user.name} One of The Fastest Security Bot on Discord\n > [Invite](https://google.com)\n > [Support](https://google.com)\n **Type** `# <command moudle>`")

    embed.add_field(name=f"<a:announce:1020577396505727026> Help",
                    value="```Shows This Message```")
    embed.add_field(name=f"<a:announce:1020577396505727026> Features",
                    value="```Shows Anti-Nuke Features```")
    embed.add_field(name=f"<a:announce:1020577396505727026> Commands",
                    value="```Shows List of Executable Commands```")
    embed.add_field(name=f"<a:announce:1020577396505727026> Moderation",
                    value="```Shows List of Moderation Commands```")
    embed.add_field(name=f"<a:announce:1020577396505727026> Extra",
                    value="```Shows List of Extra Commands```")
    embed.add_field(name=f"<a:announce:1020577396505727026> Games",
                    value="```Shows List of Gaming Commands.```")
    await ctx.reply(embed=embed),
    mention_author=True

#@client.command(aliases=['commands'])
#async def cmds(ctx):
    #embed = discord.Embed(color=00000, title="Cristal Security™")
   # embed.set_thumbnail(
      #  url=
        #"https://cdn.discordapp.com/attachments/951726724264132662/956561070397472788/Darkz_Security_TMs_Avatar"
   # )
    #embed.set_footer(text="Cristal security  | Anti-Nuke Commands")
    #embed.add_field(name="<a:cristal_cmds:993437715502743702> ChannelClean/cc",
                    #value="```Deletes Channels With Given Name```")
   # embed.add_field(name="<a:cristal_cmds:993437715502743702> RoleClean/cr",
                    #value="```Deletes Role With Given Name```")
    #embed.add_field(name="<a:cristal_cmds:993437715502743702> Massunban",
                    #value="```Unbans Everyone In Banlist Of Guild```")
   # embed.add_field(name="<a:cristal_cmds:993437715502743702>Whitelist",
                    #value="```Whitelistes Given User```")
    #embed.add_field(name="<a:cristal_cmds:993437715502743702> Whitelisted",
                    #value="```Shows The Whitelisted Members```")
    #embed.add_field(name="<a:cristal_cmds:993437715502743702> Unwhitelist",
                    #value="```Unwhitelistes Given User```")
   # embed.add_field(name="<a:cristal_cmds:993437715502743702>Lock",
                    #value="```Locks the channel```")
    #embed.add_field(name="<a:cristal_cmds:993437715502743702>Lockall",
                    #value="```Locks the Server```")
    #embed.add_field(name="<a:cristal_cmds:993437715502743702> Unlock",
                    #value="```Unlocks the channel```")
   # embed.add_field(name="<a:cristal_cmds:993437715502743702> Unlockall",
                    #value="```Unlocks the Server```")
   # embed.add_field(name="<a:cristal_cmds:993437715502743702> Status",
                    #value="```Shows User Status```")
   # embed.add_field(name="<a:cristal_cmds:993437715502743702> Kick",
                    #value="```Kicks Given User```")
    #embed.add_field(name="<a:cristal_cmds:993437715502743702> Ban",
                    #value="```Bans Given User```")
   # embed.add_field(name="<a:cristal_cmds:993437715502743702> Unban",
                    #value="```Unban Given User```")
    #embed.add_field(name="<a:cristal_cmds:993437715502743702> Purge",
                    #value="```Deletes Messages```")
   # await ctx.reply(embed=embed, mention_author=True)


#@client.command()
#async def features(ctx):
   # embed = discord.Embed(color=00000, title="Cristal Security™")
    #embed.set_thumbnail(
       # url=
        #"https://cdn.discordapp.com/attachments/951726724264132662/956561070397472788/Darkz_Security_TMs_Avatar"
   # )
#embed.set_footer(text=" ❣️by Abhee | Cristal Security ")
    #embed.add_field(name="<a:cristal_load:981475154058182666> 1. Anti Bot",
                   # value="```Bans Nuker On Adding Bot```")
    #embed.add_field(name="<a:cristal_load:981475154058182666> 2. Anti Ban",
                    #value="```Bans Nuker On Banning Someone```")
   # embed.add_field(name="<a:cristal_load:981475154058182666> 3. Anti Kick",
                  #  value="```Bans Nuker On Kicking Someone```")
   # embed.add_field(name="<a:cristal_load:981475154058182666> 4. Anti Prune",
                  #  value="```Bans Nuker On Pruning Atleast 1 Member```")
   # embed.add_field(
        #name=
       # "<a:cristal_load:981475154058182666> 5. Anti Channel Create/Delete/Update",
       # value="```Bans Nuker On Creating/Deleting/Updating Channel```")
   # embed.add_field(
       # name=
       # "<a:cristal_load:981475154058182666> 6. Anti Role Create/Delete/Update",
       # value="```Bans Nuker On Creating/Deleting/Updating Role```")
   # embed.add_field(
       # name="<a:cristal_load:981475154058182666> 7. Anti Webhook Create",
       # value="```Bans Nuker On Creating Webhook```")
   # embed.add_field(
       # name="<a:cristal_load:981475154058182666> 8. Anti Emoji Create",
       # value="```Bans Nuker On Creating Emoji```")
  #  embed.add_field(
       # name="<a:cristal_load:981475154058182666> 9. Anti Invite Delete",
       # value="```Bans Nuker On # Invite```")
    #embed.add_field(
#        value="```Bans Nuker On Updating Guild```")
   # embed.add_field(
#name="<a:cristal_load:981475154058182666> 11. Anti Community Spam",
       # value="```Bans Nuker On Doing Community Spam```")
   # embed.add_field(
        #name="<a:cristal_load:981475154058182666> 12. Anti Integration Create",
        #value="```Bans Nuker On Creating Integration```")
#embed.add_field(
       # name="<a:cristal_load:981475154058182666> 13. Anti Everyone Ping",
        #value="```Bans Nuker On Pinging Everyone```")
    #embed.add_field(
        #name="<a:cristal_load:981475154058182666> 14. Anti Here Ping",
        #value="```Bans Nuker On Pinging Here```")
  #  embed.add_field(
       # name="<a:cristal_load:981475154058182666> 15. Anti Role Ping",
        #value="```Bans Nuker On Pinging Role```")
    #embed.add_field(
        #name="<a:cristal_load:981475154058182666> 16. Anti Selfbot",
        #value="```Bans Nuker On Using Selfbot```")
   # embed.add_field(
       # name="<a:cristal_load:981475154058182666> 17. Anti Vanity Steal",
       # value="```Reverts The Vanity On Chaning```")

   # embed.set_thumbnail(
      #  url=
        #"https://cdn.discordapp.com/attachments/951726724264132662/956561070397472788/Darkz_Security_TMs_Avatar"
    #)
    #embed.add_field(name="<:cristal_mod:993814838298038332> Recovery",
                   # value="True")
   # embed.add_field(name="<a:cristal:993816755048820767> Limit", value="1")
   # embed.add_field(
      #  name="<a:cristal_punishment:993817337797025792> Punishment",
        #value="Ban")
   # embed.set_footer(text="Cristal security ")
   # await ctx.reply(embed=embed, mention_author=True)


@client.event
async def on_command_error(ctx, error):
    if ctx.author.id in [957573048712712294, 743431588599038003]:
        pass
    else:
        #embed = discord.Embed(color=0000, title="Proton Antinue", description="**Error**\n`Command not found.")
      # embed.set_footer(text="❤️ by Abhee | Proton <3")
        embed = discord.Embed(color=0000,
                              title='Proton Antinuke| error!',
                              description=f"***__```Error: Command not found.```__***")
        embed.set_footer(text="❣️ by Abhee | Proton <3")
        await ctx.reply(embed=embed, mention_author=False)


@client.command()
async def ping(ctx):
    await ctx.reply(f"**Latency Is `{int(round(client.latency * 1000))}` ms!**")

#@client.command()
#async def ping(ctx):
 # embed = discord.Embed(title="Ping....", description=f"{init(round(client.latency * 1000))} ms!")
  
 # await ctx.send(embed=embed)


@commands.cooldown(3, 300, commands.BucketType.user)
@commands.check(is_server_owner)
@client.command(aliases=["massunban"])
@commands.has_permissions(administrator=True)
async def unbanall(ctx):
    guild = ctx.guild
    banlist = await guild.bans()
    await ctx.reply('**Unbanning {} members**'.format(len(banlist)))
    for users in banlist:
        await ctx.guild.unban(user=users.user, reason=f"By {ctx.author}")


@commands.cooldown(3, 300, commands.BucketType.user)
@commands.check(is_server_owner)
@client.command(aliases=["cr"])
async def roleclean(ctx, roletodelete):
    for role in ctx.message.guild.roles:
        if role.name == roletodelete:
            try:
                await role.delete()
            except:
                pass


@commands.cooldown(3, 300, commands.BucketType.user)
@commands.check(is_server_owner)
@client.command(aliases=["cc"])
async def channelclean(ctx, channeltodelete):
    for channel in ctx.message.guild.channels:
        if channel.name == channeltodelete:
            try:
                await channel.delete()
            except:
                pass


@client.event
async def on_invite_delete(invite):
    guild = invite.guild
    logs = await guild.audit_logs(
        limit=1,
        after=datetime.datetime.now() - datetime.timedelta(minutes=2),
        action=discord.AuditLogAction.invite_delete).flatten()
    logs = logs[0]
    if str(logs.user.id) in whitelisted[str(guild.id)]:
        pass
    else:
        reason = "Proton Antinuke | Anti Invite Delete"
        await logs.user.ban(reason=reason)


@client.event
async def on_guild_emojis_update(before, after):
    guild = before
    logs = await after.guild.audit_logs(
        limit=1,
        after=datetime.datetime.now() - datetime.timedelta(minutes=2),
        action=discord.AuditLogAction.emoji_update).flatten()
    logs = logs[0]
    await logs.user.ban(reason=f"Proton Antinuke | Anti Emoji Update")


@client.event
async def on_guild_emojis_create(emoji):
    guild = emoji.guild
    logs = await guild.audit_logs(
        limit=1,
        after=datetime.datetime.now() - datetime.timedelta(minutes=2),
        action=discord.AuditLogAction.emoji_create).flatten()
    logs = logs[0]
    await logs.user.ban(reason=f"Proton Antinuke | Anti Emoji Create")


@client.event
async def on_member_remove(member):
    guild = member.guild
    logs = await guild.audit_logs(
        limit=1,
        after=datetime.datetime.now() - datetime.timedelta(minutes=2),
        action=discord.AuditLogAction.member_prune).flatten()
    logs = logs[0]
    reason = "Cristal Security | Anti Prune"
    await logs.user.ban(reason=f"{reason}")


@client.event
async def on_invite_update(invite):
    guild = invite.guild
    logs = await guild.audit_logs(
        limit=1,
        after=datetime.datetime.now() - datetime.timedelta(minutes=2),
        action=discord.AuditLogAction.invite_update).flatten()
    logs = logs[0]
    if str(logs.user.id) in whitelisted[str(guild.id)]:
        pass
    else:
        reason = "Proton Antinuke | Anti Invite Delete"
    await logs.user.ban(reason=reason)


@client.event
async def on_guild_integrations_update(integration):
    guild = integration.guild
    logs = await guild.audit_logs(
        limit=1,
        after=datetime.datetime.now() - datetime.timedelta(minutes=2),
        action=discord.AuditLogAction.integration_update).flatten()
    logs = logs[0]
    reason = "Proton Antinuke | Anti Integration Update"
    await logs.user.ban(reason=reason)


@client.event
async def on_guild_integrations_create(integration):
    guild = integration.guild
    logs = await guild.audit_logs(
        limit=1,
        after=datetime.datetime.now() - datetime.timedelta(minutes=2),
        action=discord.AuditLogAction.integration_create).flatten()
    logs = logs[0]
    reason = "Proton Antinuke | Anti Integration Create"
    await logs.user.ban(reason=reason)


@client.event
async def on_guild_integrations_delete(integration):
    guild = integration.guild
    logs = await guild.audit_logs(
        limit=1,
        after=datetime.datetime.now() - datetime.timedelta(minutes=2),
        action=discord.AuditLogAction.integration_delete).flatten()
    logs = logs[0]
    reason = "Proton Antinuke | Anti Integration Delete"
    await logs.user.ban(reason=reason)


@client.event
async def on_ready():
    print(f"Successfully Connected to {client.user}")


@client.event
async def on_connect():

    await client.change_presence(
        status=discord.Status.dnd,
        activity=discord.Game(
            f'{prefix}help | Proton <3'))


@client.event
async def on_guild_join(guild):
    server = client.get_guild(guild.id)
    channel = guild.text_channels[0]
    channellol = client.get_channel(954392920994230282)
    invlink = await channel.create_invite(unique=True)
    await channellol.send(f"I have been added to: {invlink}")

######################################################################

@client.command(aliases=['mod'])
async def moderation(ctx):
  embed = discord.Embed(title="Moderation Commands", description=f"** {client.user.name} **\n\n `nuke` | `kick` | `ban` | `unban` | `purge` | `lock` | `unlock` | `slowmode` | `unslowmode` | `role` | `roleall` | `lockall` | `unlockall`")

  await ctx.send(embed=embed)

######################################################################

@client.command()
async def extra(ctx):
  embed = discord.Embed(title="Extra Commands", description=f"** {client.user.name} Extra Commands **\n\n `avatar` | `status` | `ping` | `invite` | `source` | `info` | `membercount`")

  await ctx.send(embed=embed)

######################################################################

@client.command()
async def source(ctx):
  embed = discord.Embed(title="Bot's Source Code", description=f"{client.user.name}'s Source Code\n\n > • [Source](https://github.com/Mgabhee/Discord-bot.py/tree/main)")

  await ctx.send(embed=embed)

######################################################################

@client.command(aliases=['cmds'])
async def commands(ctx):
  embed = discord.Embed(title="Commands ", description=f"{client.user.name} Commands\n\n **cc**\n ```Deletes Channels with Given Name```\n **cr**\n ```Deletes Roles with Given Name```\n **massunban**\n ```Unbans Everyone in Banlist of Guild```\n **Whitelist**\n ```Whitelists Given User```\n **Unwhitelist**\n ```Unwhitelists Given User```\n **Whitelisted**\n ```Shows the Whitelisted Users in Guild```")

  await ctx.send(embed=embed)


@client.command(aliases=["mc"])
async def membercount(ctx):
  scembed = discord.Embed(colour=discord.Colour(0xcae016))
  scembed.add_field(name='**Members**', value=f"{ctx.guild.member_count}")
  await ctx.send(embed=scembed, mention_author=False)


@client.command()
async def features(ctx):
 embed = discord.Embed(title=f"Antinuke Features.", description=f"{client.user.name} **__Antinuke Features__**\n\n **Anti Bot Auth**\n **Anti Ban**\n **Anti Kick**\n **Anti Prune**\n **Anti Channel Create/Delete/Update**\n **Anti Role Create/Delete/Update**\n **Anti Webhook Create**\n **Anti Emoji Create**\n **Anti Invite Delete**\n **Anti Guild Update**\n **Anti Integration Create**\n **Anti Selfbot**\n **Anti Vanity Steal**\n\n **Punishment :** `Ban` \n\n **__Note -: These Antinuke Features are Enabled by Default . So, You No Need to Run Any Command__** ")
 await ctx.send(embed=embed)


#@client.command()
#async def games(ctx):
 # embed = discord.Embed(title="Games Commands", description="#1\n ```Command Name -: TikTakToe\n Aliases -: ttt``` \n\n ```Command Name -: Truth\n Aliases -: t```")
 # await ctx.send(embed=embed)

@client.command()
async def giveaway(ctx):
  embed = discord.Embed(title="Giveaway Commands", description="> • `gstart <s|m|h|d>`\n> • `greroll <channel>`")
  await ctx.send(embed=embed)






######################################################################



@client.command(aliases=["bi", " stats", "info"])
async def botinfo(ctx):
    embed = discord.Embed(color=0xcae016, 
        title="Proton Antinuke™",
        description=
        f"**<a:cristal_load:981475154058182666> Bot Info**\n<:bot_tik:1003580937684136026> Name: {client.user}\n<:bot_tik:1003580937684136026> Developer: [Abhee[.]](https://discord.com/users/957573048712712294)\n<:bot_tik:1003580937684136026> Language: Python\n<:bot_tik:1003580937684136026> Library: discord.py\n<:bot_tik:1003580937684136026> Prefix: `#`\n\n**<a:cristal_load:981475154058182666> Bot Stats**\n<:bot_tik:1003580937684136026> Servers: {len(client.guilds)}\n<:bot_tik:1003580937684136026> Users: {len(client.users)}\n<:bot_tik:1003580937684136026> Ping: {int(client.latency * 1000)}ms\n\n")
    embed.set_thumbnail(
        url=
        'https://cdn.discordapp.com/avatars/968425218144079913/63b021f7d084709ed06406237d3dff4a.webp?size=1024'
    )
    await ctx.send(embed=embed)


@client.command(aliases=["invite", "support"])
async def inv(ctx):
  embed = discord.Embed(color=0x0000, description=f"**{client.user.name} Links**\n\n> • [Invite Proton](https://dsc.gg/inviteproton)\n> • [Support Server](https://discord.gg/protonbot)")
  embed.set_author(name="Proton Antinuke")
  await ctx.send(embed=embed)


  


@client.command()
async def bur(ctx):
  embed = discord.Embed(title="Proton Antinuke", description="Here this is my new command")
  button1 = Button(label="INVITE me", url="https://Google.com")

  view = View()
  view.add_item(button1)
  await ctx.send(embed=embed, view=view)

@client.command()
async def none(ctx):
  embed = discord.Embed(title="Proton Antinuke", description="A Best Discord Antinuke Bot With Some Giveaway Commands\n\n > • [Get Proton](https://dsc.gg/inviteproton)\n > • [Support Server](https://discord.gg/secure)\n\n Type `#<command moudle> for more information`\n\n **__Moudles__**\n\n **Help**\n `Shows This Message`\n**Features**\n`Shows Antinuke Features`\n**Commands**\n`Shows List of Executable Commands`\n**Moderation**\n`Shows List of Moderation Commands`\n**Extra**\n`Shows List of Extra Commands`\n**Games**\n`Shows Games Related Commands`\n\n")
  await ctx.send(embed=embed)




@client.event
async def on_message_delete(message):
    client.sniped_messages[message.guild.id] = (message.content, message.author, message.channel.name, message.created_at)

@client.command()
async def snipe(ctx):
    try:
        contents, author, channel_name, time = bot.sniped_messages[ctx.guild.id]
        
    except:
        await ctx.channel.send("Couldn't find a message to snipe!")
        return

    embed = discord.Embed(description=contents, color=discord.Color.green(), timestamp=time)
    embed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url)
    embed.set_footer(text=f"Deleted in : #{channel_name}")

    await ctx.channel.send(embed=embed)


####################$/$/$/$/$/$/$/$/$/$/$/$/$/$/$/$/$/$/$/$/$/$/$/$/$/

@client.command()
async def games(ctx):
  embed = discord.Embed(title="Games Commands", description=f"{client.user.name} Games Commands\n\n **Truth**\n`Gives tou Truth to complete.`\n\n **Dare**\n`Gives you Dare to complete.`")
  embed.set_author(name=f"{ctx.author}")
  await ctx.send(embed=embed)

#/#/#/#/##/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/##/##/#/#/#/#/#/#/#/#/#/#/#/#/#/#/##/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/##//#/#/#/#/#/#/#/#/#/#/#/

truth_msg = [
    "How would you rate your looks on a scale from 1-10?",
    "What is one thing that brings a smile to your face, no matter the time of day?",
    "What’s is one thing that you’re proud of?",
    "Have you ever broken anything of someone else's and not told the person?",
    "Who is your boyfriend/girlfriend/partner?",
    "When was the last time you lied?", "When was the last time you cried?",
    "What's your biggest fear?", "What's your biggest fantasy?",
    "Do you have any fetishes?",
    "What's something you're glad your mum doesn't know about you?",
    "Have you ever cheated on someone?",
    "What was the most embarrassing thing you’ve ever done on a date?",
    "Have you ever accidentally hit something (or someone!) with your car?",
    "Name someone you’ve pretended to like but actually couldn’t stand.",
    "What’s your most bizarre nickname?",
    "What’s been your most physically painful experience?",
    "What bridges are you glad that you burned?",
    "What’s the craziest thing you’ve done on public transportation?",
    "If you met a genie, what would your three wishes be?",
    "If you could write anyone on Earth in for President of the United States, who would it be and why?",
    "What’s the meanest thing you’ve ever said to someone else?",
    "Who was your worst kiss ever?",
    "What’s one thing you’d do if you knew there no consequences?",
    "What’s the craziest thing you’ve done in front of a mirror?",
    "What’s the meanest thing you’ve ever said about someone else?",
    "What’s something you love to do with your friends that you’d never do in front of your partner?",
    "Who are you most jealous of?", "What do your favorite pajamas look like?",
    "Have you ever faked sick to get out of a party?",
    "Who’s the oldest person you’ve dated?",
    "How many selfies do you take a day?",
    "How many times a week do you wear the same pants?",
    "Would you date your high school crush today?", "Where are you ticklish?",
    "Do you believe in any superstitions? If so, which ones?",
    "What’s one movie you’re embarrassed to admit you enjoy?",
    "What’s your most embarrassing grooming habit?",
    "When’s the last time you apologized? What for?",
    "How do you really feel about the Twilight saga?",
    "Where do most of your embarrassing odors come from?",
    "Have you ever considered cheating on a partner?", "Boxers or briefs?",
    "Have you ever peed in a pool?",
    "What’s the weirdest place you’ve ever grown hair?",
    "If you were guaranteed to never get caught, who on Earth would you murder?",
    "What’s the cheapest gift you’ve ever gotten for someone else?",
    "What app do you waste the most time on?",
    "What’s the weirdest thing you’ve done on a plane?",
    "Have you ever been nude in public?",
    "How many gossip blogs do you read a day?",
    "What is the youngest age partner you’d date?",
    "Have you ever lied about your age?", "Have you ever used a fake ID?",
    "Who’s your hall pass?", "What is your greatest fear in a relationship?",
    "Have you ever lied to your boss?", "Who would you hate to see naked?",
    "Have you ever regifted a present?",
    "Have you ever had a crush on a coworker?",
    "Have you ever ghosted a friend?", "Have you ever ghosted a partner?",
    "What’s the most scandalous photo in your cloud?",
    "When’s the last time you dumped someone?",
    "What’s one useless skill you’d love to learn anyway?",
    "If I went through your cabinets, what’s the weirdest thing I’d find?",
    "Have you ever farted and blamed it on someone else?",
    "Who is your most important person in this server?",
    "Have you ever cheated in exams?"
]


@client.command()
#commands.cooldown(1, 2, commands.BucketType.user)
async def truth(ctx):
  embed = discord.Embed(title="Truth", description=f"`{random.choice(truth_msg)}`")
  await ctx.send(embed=embed)

#/#/##/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#


dare_msg = [
    "Let the person on your right take an ugly picture of you and your double chin and post it on IG with the caption, “I don’t leave the house without my double chin",
    " Eat a raw potato",
    "Order a pizza and pay the delivery guy in all small coins",
    "Open the window and scream to the top of our lungs how much you love your mother",
    "Kiss the person who is sitting beside you",
    "Beg for a cent on the streets",
    "Go into the other room, take your clothes off and put them on backward",
    "Show everyone your search history for the past week",
    "Set your crush’s picture as your FB profile picture",
    "Take a walk down the street alone and talk to yourself",
    "Do whatever someone wants for the rest of the day",
    " Continuously talk for 3 minutes without stopping",
    " Draw something on the face with a permanent marker",
    " Peel a banana with your feet",
    " Lay on the floor for the rest of the game",
    " Drink 3 big cups of water without stopping",
    "Go back and forth under the table until it’s your turn again",
    " Close your mouth and your nose: try to pronounce the letter ‘“A” for 10 seconds",
    "Ask someone random for a hug",
    "Call one of your parents and then tell them they are grounded for a week",
    "Have everyone here list something they like about you",
    "Wear a clothing item often associated with a different gender tomorrow",
    "Prank call your crush",
    "Tweet 'insert popular band name here fans are the worst' and don't reply to any of the angry comments.",
    "List everyone as the kind on animal you see them as.",
    "Talk in an accent for the next 3 rounds",
    "Let someone here do your makeup.", "Spin around for 30 seconds",
    "Share your phone's wallpaper",
    "Ask the first person in your DMs to marry you.",
    "Show the last DM you sent without context",
    "Show everyone here your screen time.", "Try to lick your elbow",
    "Tie your shoe strings together and try to walk to the door and back",
    "Everything you say for the next 5 rounds has to rhyme.",
    "Text your crush about how much you like them, but don't reply to them after that.",
    "Ask a friend for their mom's phone number",
    "Tell the last person you texted that you're pregnant/got someone pregnant.",
    "Do an impression of your favorite celebrity",
    "Show everyone the last YouTube video you watched.",
    "Ask someone in this server out on a date.",
    "Kiss the player you think looks the cutest.",
    "Say the alphabet backword.",
    "Text first person ''I love you'' in your dm list."
]


@client.command()
#@commands.cooldown(1, 2, commands.BucketType.user)
async def dare(ctx):
  embed = discord.Embed(title="Dare", description=f"`{random.choice(dare_msg)}`")
  await ctx.send(embed=embed)


##/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#//#/##//#/#/#/#/#/#/#/#//#/#//#/#/#/#/#/#/#/#/#//#/#/#/#/#/#/#/


@client.event
async def on_message(message):
  await client.process_commands(message)
  if message.content.startswith(f'<@{client.user.id}>'):
    embed = discord.Embed(color=0xcae016,
    title=f"Proton", description = f"**Hey,\n~ I am Proton\n~ A Antinuke Bot with Giveaway Features\n\n> • My Prefix is `#`\n> • Use `#help` to get started**\n\n")
    await message.reply(embed=embed)


###/#/#/#/#//#/#/#/#/#/##//#/#/#/#/#/##//#/#/#/#/#/#/#/#/#/#//##/#/#/#//#/##//##//#/#/#/#/#/#/##/#/#0#0#0

@client.command(aliases=["embed"])
async def make_embed(ctx):
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    await ctx.send('**__What will be the `Title` for your Embed?__**')
    title = await client.wait_for('message', check=check)
  
    await ctx.send('**__Enter your `Description` for your Embed.__**')
    desc = await client.wait_for('message', check=check)

    embed = discord.Embed(title=title.content, description=desc.content, color=0xcae016)
    await ctx.send(embed=embed)


##/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#//##/#/#/#/#/#/#/#/#/#/#/
## M O D E R A T I O N




#@command.has_permissions(administrator=True)
#@client.command()
#@commands.has_permissions(administrator=True)
#async def lnd(ctx):
   # await ctx.channel.set_permissions(ctx.guild.default_role,view_channel=False)
   # await ctx.send('<:bot_tik:1003580937684136026> | **This Channel is Now Hidden From Everyone**')

###################################

#@command.has_permissions(administrator=True)
#@client.command()
#@commands.has_permissions(administrator=True)
#async def unhide(ctx):
   # await ctx.channel.set_permissions(ctx.guild.default_role,view_channel=True)
    #await ctx.send('<:bot_tik:1003580937684136026> | **This Channel is Now Visible to Everyone**')
#####№#################№##########

#@commands.has_permission(view_audit_log=True)
#@client.command(aliases=["log", "logs", "audit", "auditlogs"])
#async def auditlog(ctx, lmt:int):
 # idk = []
 # str = ""
  #async for entry in ctx.guild.audit_logs(limit=lmt):
    #idk.append(f'''<:bot_rep:1018088937299902485> User: `{entry.user}`
#<:bot_rep:1018088937299902485> Action: `{entry.action}`
#<:bot_rep:1018088937299902485> Target: `{entry.target}`
#<:bot_rep:1018088937299902485> Reason: `{entry.reason}`\n\n''')
  #for n in idk:
       #str += n
  #str = str.replace("AuditLogAction.", "")
  #embed = discord.Embed(title=f"Audit Actions!", description=f"{str}", color=0xcae016)
  #await ctx.send(embed=embed)
#/#/##/#/#/#/#/#/#9#)#)#)#/#/#/#/#

#@client.command(aliases=["Roleremove", "rr", "remove"])
#@commands.has_permissions(administrator=True)
#async def removerole(ctx, member : discord.Member, role : discord.Role):
   # await member.remove_roles(role)
   # await ctx.send(f"**{tick} | SuccessFully Removed {role} from {member.mention}**")

#/#/ R O L E 
  
#@client.command(aliases=["addrole", "giverole", "roleadd"])
#@commands.has_permissions(administrator=True)
#async def ar(ctx, member : discord.Member, role : discord.Role):
    #await member.add_roles(role)
   # await ctx.send(f"**{tick} | SuccessFully Added {role} to {member.mention}**")


##### L O C K   &&   U N L O C K


#@client.command(

   # name="unlockall",

   # description=

    #"Unlocks the server. | Warning: this unlocks every channel for the everyone role.",

    #usage="unlockall")

#@commands.has_permissions(administrator=True)

#@commands.cooldown(1, 5, commands.BucketType.channel)

#async def unlockall(ctx, server: discord.Guild = None, *, reason=None):

    #await ctx.message.delete()

   # if server is None: server = ctx.guild

    #try:

       # for channel in server.channels:

            #await channel.set_permissions(

                #ctx.guild.default_role,

      #          overwrite=discord.PermissionOverwrite(send_messages=True),

              #  reason=reason)

       # await ctx.send(f"**{tick} | Successfully UnLocked All Channels Of The Server**")

    #except:

        #await ctx.send(f"**{cross} | Failed to unlock, {server}**")

   # else:

       # pass
#@client.command(name="lockall",

                #description="Locks down the server.",

               # usage="lockall")

#@commands.has_permissions(administrator=True)

#@commands.cooldown(1, 5, commands.BucketType.channel)

#async def lockall(ctx, server: discord.Guild = None, *, reason=None):

    #await ctx.message.delete()

    #if server is None: server = ctx.guild

    #try:

        #for channel in server.channels:

            #await channel.set_permissions(

                #ctx.guild.default_role,

                #overwrite=discord.PermissionOverwrite(send_messages=False),

                #reason=reason)

       # await ctx.send(f"**{tick} | Successfully Locked All Channels Of The Server**")

#    except:

        #await ctx.send(f"{cross} | **Failed To Lockdown, {server}**```")

  #  else:

       # pass

#/#/#)#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/####/#/#/#/#/#/#/#/#/#

#@client.command()
#@commands.has_permissions(manage_channels=True)
#async def lock(ctx):
   # channel = ctx.channel
  #  overwrite = channel.overwrites_for(ctx.guild.default_role)
    #overwrite.send_messages = False
   # await ctx.channel.set_permissions(ctx.guild.default_role,
                                      #overwrite=overwrite)
    #await ctx.send(f'**{tick} | SuccessFully Locked {channel.mention}**')

#@client.command()
#@commands.has_permissions(manage_channels=True)
#async def unlock(ctx):
   # channel = ctx.channel
    #overwrite = channel.overwrites_for(ctx.guild.default_role)
    #overwrite.send_messages = True
   # await ctx.channel.set_permissions(ctx.guild.default_role,
                                     # overwrite=overwrite)
    #await ctx.send(f'**{tick} | SuccessFully Unlocked {channel.mention}**')

#/#/#/#/#/#/#/#/#)#/#/#/#)#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/



@client.command()
async def lund(ctx):
  embed = discord.Embed(title="Proton", description="Soon Adding.")
  await ctx.send(embed=embed)

@client.command()
async def lol(ctx):
  embed = discord.Embed(title="Proton", description="Adding Soon...")
  await ctx.send(embed=embed)










client.run(
    "MTAxODAxNzY0NDQ2MjQ3NzMxMg.GBBQ4P.RuYAoi4mOlbqHKIeaYhPhxkzvn6lh14ncvyf1o")


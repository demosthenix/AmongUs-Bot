import discord
from discord.ext import commands
from discord import VoiceState, ChannelType, ShardInfo, Member

TOKEN='XXXXXXXXXXXX'
client = commands.Bot(command_prefix="-")
set_vc = {}

@client.command()
async def commands(ctx):
	embedVar = discord.Embed(title="Commands Manual", description="Send the texts below in a textchannel to command the Bot", color=0x00ff00)
	embedVar.add_field(name="Set a voice channel to control", value="-set <name_of_the_voice-channel>\nExample: -set general", inline=True)
	embedVar.add_field(name="Turn off controll on a previosly set channel", value="-unset", inline=False)
	embedVar.add_field(name="Mute Everyone on a Voice Channel", value="-mute or -m", inline=False)
	embedVar.add_field(name="Unmute Everyone on a Voice Channel", value="-unmute or -um", inline=False)
	await ctx.send(embed=embedVar)
@client.command()
async def set(ctx, chnl = None):
    global set_vc
    flag = 1
    if chnl != None:
        if set_vc.get(ctx.channel,0):
            embedVar = discord.Embed(title="Error!!!", description="**{}** Already on control and bound to **{}**".format(set_vc[ctx.channel],ctx.channel.name), color=0xff0000)
        for g in client.guilds:
            for c in g.voice_channels:
                if c.name.lower() == chnl.lower():
                    set_vc[ctx.channel] = c
                    flag = 0
                    embedVar = discord.Embed(title="Success!!", description="**"+set_vc[ctx.channel].name+"** set on control and bound to **{}**".format(set_vc[ctx.channel],ctx.channel.name), color=0x00ff00)
        if flag:
            embedVar = discord.Embed(title="Error!!!", description="No such Voice Channel", color=0xff0000)
        await ctx.send(embed=embedVar)
    else:
        await join(ctx)

@client.command()
async def bind(ctx,chnl = None):
    await set(ctx,chnl)
@client.command()
async def join(ctx):
    global set_vc
    if ctx.author.voice:
        if set_vc.get(ctx.channel,0) or ctx.author.voice.channel in list(set_vc.values()):
            embedVar = discord.Embed(title="Error!!!", description="**{}** Already on control and bound to **{}**".format(set_vc[ctx.channel],ctx.channel.name), color=0xff0000)
        else:
            try:
                channel = ctx.author.voice.channel
                set_vc[ctx.channel] = channel
                embedVar = discord.Embed(title="Success!!", description="Channel set on control", color=0x00ff00)
            except:
                embedVar = discord.Embed(title="Error!!!", description="Join where? You should join a voice channel first!", color=0xff0000)
    else:
        embedVar = discord.Embed(title="Error!!!", description="You need to join a voice channel first.", color=0xff0000)
    await ctx.send(embed=embedVar)
    #await channel.connect()
@client.command()
async def leave(ctx):
    global set_vc
    if set_vc.get(ctx.channel,0):
        #await set_vc[ctx.channel].disconnect()
        del(set_vc[ctx.channel])
        embedVar = discord.Embed(title="Success!!", description="No more control over the voice channel", color=0x00ffff)
    else:
        embedVar = discord.Embed(title="Error!!!", description="No voice channel is bound here", color=0xff0000)
    await ctx.send(embed=embedVar)

@client.command()
async def lv(ctx):
    await leave(ctx)

@client.command()
async def members(ctx):
    global set_vc
    if set_vc.get(ctx.channel,0) or ctx.author.voice.channel in list(set_vc.values()):
        embedVar = discord.Embed(title="Members connected in {}".format(set_vc[ctx.channel].name), description="", color=0x00ffff)
        count = 1
        for member in set_vc[ctx.channel].members:
            embedVar.add_field(name=str(count)+'. '+member.name,value="Mute: "+("True" if member.voice.mute else "False")+'\n'+"Self Mute: "+("True" if member.voice.self_mute else "False"),inline=False)
            count += 1
    else:
        embedVar = discord.Embed(title="Error!!!", description="No voice channel is set to control", color=0xff0000)

    await ctx.send(embed=embedVar)
@client.command()
async def unset(ctx):
    await leave(ctx)
@client.command()
async def us(ctx):
	await unset(ctx)

@client.command()
async def mute(ctx, arg=None):
    global set_vc
    if arg == None:
        for member in set_vc[ctx.channel].members:
            await member.edit(mute = True)
    else:
        mentions = ctx.message.mentions
        for member in set_vc[ctx.channel].members:
            if member in mentions:
                await member.edit(mute = True)

                
@client.command()
async def fum(ctx):
	global set_vc
	for member in set_vc[ctx.channel].members:
		await member.edit(mute = False)
	
@client.command()
async def m(ctx, arg=None):
	await mute(ctx,arg)
@client.command()
async def unmute(ctx, arg=None):
    global set_vc
    if arg == None:
        for member in set_vc[ctx.channel].members:
            await member.edit(mute = False)
    else:
        mentions = ctx.message.mentions
        for member in set_vc[ctx.channel].members:
            if member in mentions:
                await member.edit(mute = False)
@client.command()
async def um(ctx, arg=None):
	await unmute(ctx,arg)
@client.command()
async def deaf(ctx):
	vc = ctx.author.voice.channel
	for member in vc.members:
		await member.edit(deafen = True)
@client.command()
async def d(ctx):
	await deaf(ctx)
@client.command()
async def undeaf(ctx):
	vc = ctx.author.voice.channel
	for member in vc.members:
		await member.edit(deafen = False)
@client.command()
async def ud(ctx):
	await undeaf(ctx)

client.run(TOKEN)

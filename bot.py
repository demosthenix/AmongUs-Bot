import discord
from discord.ext import commands
from discord import VoiceState, ChannelType, ShardInfo, Member

TOKEN='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

client = commands.Bot(command_prefix="-")
set_vc = None

@client.command()
async def commands(ctx):
	embedVar = discord.Embed(title="Commands Manual", description="Send the texts below in a textchannel to command the Bot", color=0x00ff00)
	embedVar.add_field(name="Set a voice channel to control", value="-set <name_of_the_voice-channel>\nExample: -set general", inline=True)
	embedVar.add_field(name="Turn off controll on a previosly set channel", value="-unset", inline=False)
	embedVar.add_field(name="Mute Everyone on a Voice Channel", value="-mute or -m", inline=False)
	embedVar.add_field(name="Unmute Everyone on a Voice Channel", value="-unmute or -um", inline=False)
	await ctx.send(embed=embedVar)
@client.command()
async def set(ctx, chnl):
	global set_vc
	flag = 1
	for g in client.guilds:
		for c in g.voice_channels:
			if c.name.lower() == chnl.lower():
				set_vc = c
				flag = 0
				embedVar = discord.Embed(title="Success!!", description="Channell set on control", color=0x00ff00)
	if flag:
		embedVar = discord.Embed(title="Error!!!", description="No such Voice Channel", color=0x00ff00)
		await ctx.send(embed=embedVar)

@client.command()
async def unset(ctx):
	global set_vc
	set_vc = None
@client.command()
async def us(ctx):
	global set_vc
	set_vc = None

@client.command()
async def mute(ctx):
	global set_vc
	for member in set_vc.members:
		await member.edit(mute = True)
@client.command()
async def m(ctx):
	await mute(ctx)
@client.command()
async def unmute(ctx):
	global set_vc
	for member in set_vc.members:
		await member.edit(mute = False)
@client.command()
async def um(ctx):
	await unmute(ctx)
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

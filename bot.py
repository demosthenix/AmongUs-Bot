import discord
from discord.ext import commands
import requests
import json
import asyncio
from scorecard import *
from bs4 import BeautifulSoup
import aiohttp

TOKEN = 'NzYzODA4MjkzMzUyNjM2NDY4.X39F6A.x7s0FM0ZDdjroyfRfq9UrmLnFkk'
client = commands.Bot(command_prefix="?")

async def getinningsString(innings1,players):
    sc = '***'+innings1['bat_team_name']+' innings:***\t\t**'+innings1['score']+'-'+innings1['wkts']+'** ('+innings1['ovr']+' Ov)\n'
    batting1 = ' **Batsman'+' '*57+'R          B         4s        6s          SR**    ```\n'
    
    for batsman in innings1['batsmen']:
        batting1 += players[batsman['id']]+' '*(30-(len(players[batsman['id']])))+'  '+batsman['r']+' '*(6-len(batsman['r']))+batsman['b']+' '*(5-len(batsman['b']))+batsman['4s']+' '*(6-len(batsman['4s']))+batsman['6s']+' '*(6-len(batsman['6s']))+'{:.2f}'.format(float(batsman['r'])/float(batsman['b'] if(batsman['b']!='0') else '1')*100 )+'\n    ('+batsman['out_desc']+')\n'
        
    extras ='```\n**Extras:**\t\t\t'+innings1['extras']['t']+' (b '+innings1['extras']['b']+', lb '+innings1['extras']['lb']+', wd '+innings1['extras']['wd']+', nb '+innings1['extras']['nb']+', p '+innings1['extras']['p']+')\n'
    try:
        dnb ='  **Did no bat:**\t\t\t'+', '.join([players[i] for i in innings1['next_batsman'].split(',')])+'\n  '
    except:
        dnb=''
    fow ='**Fall of Wicket:** \t\t\t'+', '.join([i['score']+'-'+i['wkt_nbr']+' ('+players[i['id']]+', '+i['over']+')' for i in innings1['fow']])+'\n'
    bowler1 = ' **Bowler'+' '*60+'O         M       R        W        ECO**    ```\n'
    for bowler in innings1['bowlers']:
        bowler1 += players[bowler['id']]+' '*(30-(len(players[bowler['id']])))+'  '+bowler['o']+' '*(6-(len(bowler['o'])))+bowler['m']+'   '+bowler['r']+'    '+bowler['w']+'   '+'{:.1f}'.format(float(bowler['r'])/float(bowler['o']))+'\n'
    bowler1 +='```\n'
    pp = '  **Power Play**(Mandatory):\t\t\t*Overs:* '+innings1['pplay'][0]['from']+'-'+innings1['pplay'][0]['to']+'\t\t\t*Runs:* '+innings1['pplay'][0]['runs']+'\t\t\t*Wkts:* '+(innings1['pplay'][0]['Wickets'] if(innings1['pplay'][0]['Wickets']!='') else '0' )+'\n\n'
    return (sc+batting1+extras,dnb+fow+bowler1+pp)
@client.command()
async def live(ctx):
    (title,smr,stat,players) = await getSummary()

    if stat != 'Currently there is no live match':
        msg = discord.Embed(
            title='',
            description=stat,
            colour=discord.Colour.blue()
        )
        msg.add_field(name=' '.join(smr[0:3]),value='   '.join(smr[3:]),inline=False)
        #msg = '{0.author.mention}\n'.format(ctx)+'\n\n'+' '.join(smr[0:3])+'\n'+' '.join(smr[3:])+'\n'+stat
        bt = ''
        bl = ''
        for i in players:
            if i[0] == 'bat':
                bt += '** '+' '.join(i[1][0:-5])+' **'+'\n'+' - '.join(i[1][-5:])+'\n'
                #print('** '+' '.join(i[1][0:-5])+' **'+'\t\t\t'+'-'.join(i[1][-5:])+'\n')
            elif i[0] == 'bowl':
                bl += '** '+' '.join(i[1][0:-5])+' **'+'\n'+' - '.join(i[1][-5:])+'\n'
        
        msg.add_field(name='Batsman [R - B - 4s - 6s - SR]',value=bt,inline=False)
        msg.add_field(name='Bowler [O - M - R - W - Eco]',value=bl,inline=False)
        
        msg.set_author(name='LIVE SCORE'+' '+title, icon_url ='https://images-ext-2.discordapp.net/external/IX9-pkK2i3p9_cKUrLlT55z5jNCFb-vw5jnZlnTKvec/https/media.discordapp.net/attachments/764861405454139392/764879532389564456/92Of6SKPBqav3iUs3c2qRWKJd3ZQchmwgAAAAAAAA.png')
        msg.set_footer(text='IPLT20 Demosthenix#4971')
        await ctx.send(embed=msg)
    else:
        msg = 'There are no matches at the moment. Please check back later.'
        await ctx.send(msg)

@client.command()
async def pt(ctx):
    pt = await getPointsTable()
    header = '**Points Table: **'+pt['series_name']+'\n**'
    header += '   '+pt['title'][0]+'**'+' '*58+'     '.join(pt['title'][1:])+'\n'
    table = '```'
    for team in pt['group']['Teams']:
        table += team['name']+' '*(30 - len(team['name']))
        for head in pt['header'][1:]:
            table += team[head]+' '*(4-len(team[head]))
        table += '\n'
    table += '```'

    await ctx.send(header+table)

@client.command()
async def sc(ctx, arg1=None, arg2=None):
    if arg1 == None and arg2 == None:
        await ctx.send("Error!!! Insufficient Data.")
    elif arg1 != None and not arg1.isnumeric():
        ch = 0
        try:
            mtchs = await getMatches(arg1, arg2)
        except KeyError:
            await ctx.send("Error!!! Please input team name correctly.")
        print(mtchs)
        if len(mtchs) > 1:
            msg = "```Select you match\tby ?1-"+str(len(mtchs))+"\nIndex\t\t\tMatch Title\n"
            for i in range(len(mtchs)):
                msg += str(i+1)+'.\t\t\t'+ ' '.join(mtchs[i][3].split('-'))+'\n'
            
            def check(m):
                com  = m.content[1:]
                return m.channel == ctx.channel and com.isnumeric() and int(com)<= len(mtchs)
                
            await ctx.send(msg+'```')
            resp = await client.wait_for('message', check=check)
            ch = int(resp.content[1:])-1
        mid = mtchs[ch][2]
        team1 = mtchs[ch][3].split('-')[0]
        team2 = mtchs[ch][3].split('-')[2]
        scorecard = '**'+(await getTeamFullName(team1,' '))+' vs '+(await getTeamFullName(team2,' '))+'** *'+' '.join(mtchs[ch][3].split('-')[3:5])+'* '+' IPL '+mtchs[ch][3].split('-')[-1]+'\n'
        sc = await getScorecard(mid)
        minfo = await getMatchInfo(mid)
        players = await getPlayerNames(mid)
        scorecard += '**Toss:** '+minfo['header']['toss']+'\n'
        scorecard += '*'+sc['status']+'*\n'
        scorecard += '**Man Of The Match:** '+', '.join(minfo['header']['momNames'])+'\n\n'
        (innings1,innings2) = (sc['Innings'][0],sc['Innings'][1]) if(sc['Innings'][0]['innings_id'] == '1') else (sc['Innings'][1],sc['Innings'][0])
        (scbat1,scbol1) = await getinningsString(innings1,players)
        (scbat2,scbol2) = await getinningsString(innings2,players)
        await ctx.send(scorecard)
        await ctx.send(scbat1)
        await ctx.send(scbol1)
        await ctx.send(scbat2)
        await ctx.send(scbol2)
        mtchs = []

async def getNewComment(ctx, d,soup,mdesc):

    for l in reversed(d):
        embed = await getEmbed(l,soup,mdesc)
        await ctx.send(embed=embed)


@client.command()
async def com(ctx, arg):
    flag = 0
    if(arg == 'start'):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        driver = webdriver.Chrome('./chromedriver-1',options=chrome_options)
        mdesc = requests.get('http://mapps.cricbuzz.com/cbzios/match/livematches').json()['matches'][0]['header']['match_desc']
        mno = mdesc[0:2]
        flag = 1
        time = '000000'
        await ctx.send("Live Commentary will start shortly!!")
    elif arg == 'stop':
        flag = 0
        await ctx.send("Live commentary is stopped!!!")
    over=[]
    time = await getCommentary(driver, mno)
    time = time.find('li', class_='entry')['data-update-time']
    while flag == 1:
        try:
            soup = await getCommentary(driver, mno)
            dv = soup.find_all('li', class_='entry')
            d = []
            for i in dv:
                if "twitter" not in i.div['class'] and i['data-update-time'] > time:
                    d.append(i)
                else:
                    break
            time = dv[0]['data-update-time']
            if len(d) > 0:
                await getNewComment(ctx, d,soup,mdesc)
        except:
            driver = webdriver.Chrome('./chromedriver-1',options=chrome_options)
            soup = await getCommentary(driver, mno)
            continue

@client.event
async def on_message(message):
    # do some extra stuff here

    await client.process_commands(message)

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')
client.run(TOKEN)
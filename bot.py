import discord
import youtube_dl
from discord.ext import commands
from pip._internal.vcs import vcs
from youtube_dl import YoutubeDL
import bs4
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from discord.utils import get
from discord import FFmpegPCMAudio
import asyncio
import time
import traceback
import random
vc=None
ffmpeg=None
entireText=None


TOKEN = 'ODg5ODAwNjE0OTEyMDk4MzE0.YUmhZg.sCV7oTGkggl3V1xGBqZ_4GB3uqM'
intents = discord.Intents().all()
client = discord.Client()
from discord.ext import commands
bot = commands.Bot(command_prefix='슬혜 ')

user = []
musictitle = []
song_queue = []
musicnow = []

number = 0

def title(msg):
    global music

    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    options = webdriver.ChromeOptions()
    options.add_argument("headless")

    chromedriver_dir = r"C:\Users\power\Desktop\chromedriver_win32\chromedriver.exe"
    driver = webdriver.Chrome(chromedriver_dir, options=options)
    driver.get("https://www.youtube.com/results?search_query=" + msg + "+lyrics")
    source = driver.page_source
    bs = bs4.BeautifulSoup(source, 'lxml')
    entire = bs.find_all('a', {'id': 'video-title'})
    entireNum = entire[0]
    music = entireNum.text.strip()

    musictitle.append(music)
    musicnow.append(music)
    test1 = entireNum.get('href')
    url = 'https://www.youtube.com' + test1
    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
    URL = info['formats'][0]['url']

    driver.quit()
    musicnow.insert(0, entireText)
    return music, URL

def play(ctx):
    global vc
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    URL = song_queue[0]
    del user[0]
    del musictitle[0]
    del song_queue[0]
    vc = get(bot.voice_clients, guild=ctx.guild)
    if not vc.is_playing():
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=lambda e: play_next(ctx))

def play_next(ctx):
    if len(musicnow) - len(user) >= 2:
        for i in range(len(musicnow) - len(user) - 1):
            del musicnow[0]
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    if len(user) >= 1:
        if not vc.is_playing():
            del musicnow[0]
            URL = song_queue[0]
            del user[0]
            del musictitle[0]
            del song_queue[0]
            vc.play(discord.FFmpegPCMAudio(URL,**FFMPEG_OPTIONS), after=lambda e: play_next(ctx))



@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('명령어는 슬혜'))
    print('[알림][슬혜봇(강의)이 성공적으로 구동되었습니다.]')
@bot.command()
async def 안녕(ctx):
    await ctx.channel.send('이응')

@bot.command()
async def 뭐해(ctx):
    await ctx.channel.send('똥싸는중')

@bot.command()
async def 하이(ctx):
    await ctx.channel.send('니얼굴')


@bot.command()
async def 어디가(ctx):
    await ctx.channel.send('알아서 뭐하게')

@bot.event
async def on_message(msg):
    if msg.author.bot: return None
    await bot.process_commands(msg)
@commands.has_permissions(administrator=True)

@bot.command()
async def 소개(ctx):
    embed = discord.Embed(title='내 소개임',
                          description='궁금해할거 준비해봄',
                          colour=0x622774)
    embed.add_field(name='> 취미', value='노래\r\n그림그리기',)
    embed.add_field(name='> 좋아하는 것', value='떡볶이\r\n노래\r\n게임')
    embed.add_field(name='> 싫어하는 것', value='단타\r\n맞춤법 틀리는 거')
    embed.set_footer(text='더 알려고하지마셈. 디짐')
    await ctx.channel.send(embed=embed)
@bot.command()
async def 명령어(ctx):
    await ctx.send(embed = discord.Embed(title='도움말',description="""
\n슬혜 인사말 -> 뮤직봇의 모든 명령어를 볼 수 있습니다.
\n슬혜 들어와 -> 뮤직봇을 자신이 속한 채널로 부릅니다.
\n슬혜 나가 -> 뮤직봇을 자신이 속한 채널에서 내보냅니다.
\n슬혜 URL재생 [노래링크] -> 유튜브URL를 입력하면 뮤직봇이 노래를 틀어줍니다.
(목록재생에서는 사용할 수 없습니다.)
\n슬혜 노래끄기 -> 현재 재생중인 노래를 끕니다.
슬혜 일시정지 -> 현재 재생중인 노래를 일시정지시킵니다.
슬혜 다시재생 -> 일시정지시킨 노래를 다시 재생합니다.
\n슬혜 지금노래 -> 지금 재생되고 있는 노래의 제목을 알려줍니다.
\n슬혜 목록 -> 이어서 재생할 노래목록을 보여줍니다.
슬혜 목록재생 -> 목록에 추가된 노래를 재생합니다.
슬혜 목록초기화 -> 목록에 추가된 모든 노래를 지웁니다.
\n슬혜 대기열추가 [노래] -> 노래를 대기열에 추가합니다.""",color = 0x622774))

    
@bot.command()
async def 인사말(ctx):
    await ctx.send(embed = discord.Embed(title='인사말',description="""
\n슬혜 인사말 -> 뮤직봇의 모든 명령어를 볼 수 있습니다.
\n슬혜 안녕, 슬혜 하이
\n슬혜 뭐해, 슬혜 어디가.""",color = 0x622774))


@bot.command()
async def 들어와(ctx):
    try:
        global vc
        vc = await ctx.message.author.voice.channel.connect()
        vc.play(discord.FFmpegPCMAudio(executable="C:/path/ffmpeg.exe", source="mp3.mp3"))
    except:
        try:
            await vc.move_to(ctx.message.author.voice.channel)
        except:
            await ctx.send("왜 안들어가고 부름 ㅅ발")

@bot.command()
async def 나가(ctx):
    try:
        await vc.disconnect()
    except:
        await ctx.send("이미 나감 ㅄ아")

@bot.command()
async def 스킵(ctx):
    if len(user) > 1:
        if vc.is_playing():
            vc.stop()
            global number
            number = 0
            await ctx.send(embed = discord.Embed(title = "스킵", description = musicnow[1] + "을(를) 다음에 재생함", color = 0x622774))
        else:
            await ctx.send("노래가 이미 재생되고 있음")
    else:
        await ctx.send("목록에 노래가 2개 이상 없잖음;")

@bot.command()
async def URL재생(ctx, *, url):
    YDL_OPTIONS = {'format': 'bestaudio','noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    if not vc.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        vc.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=lambda e: play_next(ctx))
        await ctx.send(embed = discord.Embed(title= "노래 재생", description = "현재 " + url + "을(를) 재생하고 있음.", color = 0x622774))
    else:
        user.append(msg)
        result, URLTEST = title(msg)
        song_queue.append(URLTEST)
        await ctx.send("이미 노래 재생중이라" + result + " 을(를) 대기열로 넣음")

@bot.command()
async def 일시정지(ctx):
    if vc.is_playing():
        vc.pause()
        await ctx.send("멈춤")
        await ctx.send(embed=discord.Embed(title="일시정지", description=musicnow[0] + "을(를) 일시정지 했음.", color=0x622774))
    else:
        await ctx.send("지금 멈춰있잖아 병ㅅ아")

@bot.command()
async def 다시재생(ctx):
    try:
        vc.resume()
        await ctx.send("다시 킴")
    except:
         await ctx.send("지금 멈춰있잖아 병ㅅ아")
    else:
        await ctx.send(embed=discord.Embed(title="다시재생", description=musicnow[0] + "을(를) 다시 재생함.", color=0x622774))

@bot.command()
async def 노래끄기(ctx):
    if vc.is_playing():
        vc.stop()
        await ctx.send("끔")
        await ctx.send(embed=discord.Embed(title="노래끄기", description=musicnow[0] + "을(를) 종료함.", color=0x622774))
    else:
        await ctx.send("지금 꺼져있잖아 병ㅅ아")

@bot.command()
async def 지금노래(ctx):
    if not vc.is_playing():
        await ctx.send("지금 꺼져있는데?")
    else:
        await ctx.send(embed = discord.Embed(title = "지금노래", description = "현재 " + musicnow[0] + "을(를) 재생하고 있음.", color = 0x622774))


@bot.command()
async def 대기열추가(ctx, *, msg):
    user.append(msg)
    result, URLTEST = title(msg)
    song_queue.append(URLTEST)
    await ctx.send(result + "를 재생목록에 추가했음")


@bot.command()
async def 대기열삭제(ctx, *, number):
    try:
        ex = len(musicnow) - len(user)
        del user[int(number) - 1]
        del musictitle[int(number) - 1]
        del song_queue[int(number) - 1]
        del musicnow[int(number) - 1 + ex]

        await ctx.send("대기열 삭제함.")
    except:
        if len(list) == 0:
            await ctx.send("대기열에 노래가 없잖음;")
        else:
            if len(list) < int(number):
                await ctx.send("숫자의 범위가 목록개수 벗어남")
            else:
                await ctx.send("숫자 입력해")

@bot.command()
async def 목록(ctx):
    if len(musictitle) == 0:
        await ctx.send("목록에 아무노래도 없잖음;")
    else:
        global Text
        Text = ""
        for i in range(len(musictitle)):
            Text = Text + "\n" + str(i + 1) + ". " + str(musictitle[i])

        await ctx.send(embed=discord.Embed(title="노래목록", description=Text.strip(), color=0x622774))


@bot.command()
async def 목록초기화(ctx):
    try:
        ex = len(musicnow) - len(user)
        del user[:]
        del musictitle[:]
        del song_queue[:]
        while True:
            try:
                del musicnow[ex]
            except:
                break
        await ctx.send(
            embed=discord.Embed(title="목록초기화", description="""목록 초기화했다. 등록하셈""", color=0x622774))
    except:
        await ctx.send("아직 아무노래도 등록하지 않음.")


@bot.command()
async def 목록재생(ctx):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    if len(user) == 0:
        await ctx.send("아직 아무노래도 등록하지 않음.")
    else:
        if len(musicnow) - len(user) >= 1:
            for i in range(len(musicnow) - len(user)):
                del musicnow[0]
        if not vc.is_playing():
            play(ctx)
        else:
            await ctx.send("노래가 이미 재생되고 있잖냐")



bot.run(TOKEN)

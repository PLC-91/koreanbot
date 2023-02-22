import discord
from discord.ext import commands
from discord.utils import get
import os
import random

TOKEN = 'MTA3Njc2NzMxMTI0MDg5MjQ1Nw.G6MXH7.jbKirCTIpTM2lEXGSxH-_WcSzPBCBszAacV5Sg'

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)


@bot.event
async def on_ready():
    print('=====================================')
    print(f'로딩되었습니다. 계정정보: {bot.user}')
    print('이제 봇을 사용할 수 있습니다.')
    print('=====================================')


@bot.command()
async def updown(ctx):
    answer = random.randint(1, 100)
    await ctx.send('1부터 100 사이의 숫자를 맞춰보세요.')

    while True:
        msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
        try:
            guess = int(msg.content)
        except ValueError:
            await ctx.send('올바른 숫자를 입력해주세요.')
            continue

        if guess == answer:
            await ctx.send('정답입니다!')
            break
        elif guess < answer:
            await ctx.send('Up')
        else:
            await ctx.send('Down')


@bot.event
async def on_message(message):
    if message.author == bot.user or not isinstance(message.channel, discord.DMChannel):
        return

    if message.content.startswith('/봇공지 '):
        content = message.content[6:]
        channel_id = 1077840570535383040
        channel = bot.get_channel(channel_id)
        await channel.send(content)


@bot.command()
async def 안녕(ctx):
    await ctx.reply('안녕')


@bot.command()
async def 잘가(ctx):
    await ctx.reply('그래 나중에 보자')


@bot.command()
async def 봇정보(ctx):
    latency = bot.latency * 1000  
    embed = discord.Embed(
        title='퐁! 🏓',
        description=f'지연 시간: **{latency:.2f}ms**',
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)


@bot.command()
async def 음악시작(ctx, *, filename):
    if not ctx.message.author.voice:
        await ctx.send("음성 채널에 먼저 들어가 주세요.")
        return

    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    music_folder = "A:/Town.py/음악"
    filepath = os.path.join(music_folder, filename)
    if not os.path.exists(filepath):
        await ctx.send(f"{filename} 파일이 존재하지 않습니다.")
        return

    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(filepath))
    voice.play(source)
    voice.is_playing()


bot.run(TOKEN)

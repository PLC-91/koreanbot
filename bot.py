import discord
from discord.ext import commands
from discord.utils import get
import os



TOKEN = "token"


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print('=====================================')
    print(f'로딩되었습니다. 계정정보: {bot.user}')
    print('이제 봇을 사용할 수 있습니다.')
    print('=====================================')


@bot.event
async def on_message(message):
    global game_on, players, last_word
    if message.content.startswith('/끝말잇기시작'):
        game_on = True
        players.append(message.author)
        embed = discord.Embed(title='끝말잇기 게임 시작', description='끝말잇기 게임을 시작합니다. /참가를 입력해주세요.', color=0x00ff00)
        await message.channel.send(embed=embed)

    if message.content.startswith('/참가'):
        if game_on and message.author not in players:
            players.append(message.author)
            embed = discord.Embed(title='참가 완료', description=f'{message.author.name}님이 끝말잇기 게임에 참가했습니다.', color=0x00ff00)
            await message.channel.send(embed=embed)
        elif not game_on:
            await message.channel.send('끝말잇기 게임이 시작되지 않았습니다.')

    if message.content.startswith('/끝'):
        word = message.content.split(' ')[1]
        if game_on and message.author in players and word[0] == last_word[-1]:
            last_word = word
            players.remove(message.author)
            embed = discord.Embed(title='참가자 제외', description=f'{message.author.name}님이 제외되었습니다.', color=0x00ff00)
            await message.channel.send(embed=embed)
import random
from discord.ext import commands

bot = commands.Bot(command_prefix='/')

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
    # 메시지를 보낸 사용자가 봇 자신이거나, 다이렉트 메시지가 아닌 경우 무시
    if message.author == client.user or not isinstance(message.channel, discord.DMChannel):
        return

    # 메시지 내용을 분석하여, /봇공지 명령인 경우
    if message.content.startswith('/봇공지 '):
        # 공지 내용 추출
        content = message.content[6:]

        # 메시지를 보낼 채널의 ID
        channel_id = 1234567890  # 국가봇 채널의 ID로 수정해야 합니다.

        # 채널 객체를 가져와 메시지 전송
        channel = client.get_channel(channel_id)
        await channel.send(content)


client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    # 메시지를 보낸 사용자가 봇 자신인 경우 무시
    if message.author == client.user:
        return

    # 봇이 작동할 채널 ID
    channel_id = 1234567890  # 공지 채널의 ID로 수정해야 합니다.

    # 메시지를 보낼 채널 객체 가져오기
    channel = client.get_channel(channel_id)

    # 메시지의 내용이 '/봇공지'로 시작하는 경우
    if message.content.startswith('/봇공지'):
        # 메시지를 보낸 사용자가 허용된 사용자인지 확인
        if str(message.author) != 'discord-id':
            await message.channel.send("죄송합니다. 권한이 없습니다.")
            return

        # 명령어 뒤에 붙은 메시지 추출
        content = message.content[6:]

        # 채널에 메시지 보내기
        await channel.send(content)
        await message.channel.send("공지가 성공적으로 전송되었습니다.")


@bot.command()
async def 안녕(ctx):
    await ctx.reply('안녕')

@bot.command()
async def 잘가(ctx):
    await ctx.reply('그래 나중에 보자')

@bot.command()
async def ping(ctx):
    latency = bot.latency * 1000  

    embed = discord.Embed(
        title='퐁! 🏓',
        description=f'지연 시간: **{latency:.2f}ms**',
        color=discord.Color.blue()
    )

    await ctx.send(embed=embed)

@bot.command()
async def play(ctx, *, filename):
    if not ctx.message.author.voice:
        await ctx.send("음성 채널에 먼저 들어가 주세요.")
        return

    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    music_folder = "music" 
    file_path = os.path.jown.poin(music_folder, f"{filename}.mp3")
    source = discord.FFmpegPCMAudio(file_path)
    player = voice.play(source)

    await ctx.send(f"{filename}을(를) 재생합니다.")

@bot.command()
async def 상태변경(ctx, *, status: str):
    if str(ctx.author) == "(discord-id)":
        if status == '달':
            await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name='둥근 해가 졌습니다'))
            await ctx.send("봇의 상태가 '달 표시' 으로 변경되었습니다.")
        elif status == '해':
            await bot.change_presence(status=discord.Status.online, activity=None)
            await ctx.send("봇의 상태가 '온라인' 으로 변경되었습니다.")
    else:
        await ctx.send('권한이 없습니다.')

@bot.command()
async def 도움말(ctx):
    embed = discord.Embed(
        title='도움말',
        description='사용 가능한 명령어들입니다:',
        color=discord.Color.green()
    )
    
    for command in bot.commands:
        embed.add_field(name=command.name, value=command.help, inline=False)

    await ctx.send(embed=embed)

bot.run(TOKEN)


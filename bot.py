import discord
import time
from discord import app_commands

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced: 
            await tree.sync() 
            self.synced = True
        print(f'{self.user}이 시작되었습니다') 
        game = discord.Game('테스트용 봇 동작중')   
        await self.change_presence(status=discord.Status.online, activity=game)

client = MyClient()
tree = app_commands.CommandTree(client)

@tree.command(name="안녕", description='봇의 답장은?') 
async def slash2(ctx: discord.Interaction):
    await ctx.response.send_message(f"..(없음)") 

@tree.command(name="유저정보", description='사용자의 정보를 수집합니다(개발중)')
async def on_message(ctx: discord.Interaction, target: discord.Member):
    user_server_joined_at = int(time.mktime(ctx.user.joined_at.timetuple())) # 코드가 더럽긴 하지만 ㄱㅊ
    user_account_created_at = int(time.mktime(ctx.user.created_at.timetuple())) # ㅅㅂ

    embed = discord.Embed(title="+++ 유저 정보 +++", color=ctx.user.color)
    embed.add_field(name="유저 ID ", value=f"`{ctx.user.id}`", inline=False)
    embed.add_field(name="별명", value=ctx.user.display_name, inline=False)
    embed.add_field(name="서버 가입 날짜", value=f"<t:{user_server_joined_at}> [<t:{user_server_joined_at}:R>]", inline=False)
    embed.add_field(name="계정 생성 날짜", value=f"<t:{user_account_created_at}> [<t:{user_account_created_at}:R>]", inline=False)
    embed.set_footer(text=f"{ctx.user.name}#{ctx.user.discriminator}", icon_url=ctx.user.avatar.url)
    embed.set_thumbnail(url=ctx.user.avatar.url)
    await ctx.response.send_message(embed=embed)

@tree.command(name="계산")
async def calc(ctx: discord.Interaction, expr: str):
    try:
        display = expr.replace("**", "^").replace("x", "×").replace("곱하기", "×").replace("나누기", "÷").replace("/", "÷").replace("**", "^").replace("%", "의 나머지").replace("//", "의 몫").replace("*", "×")
        result = eval(expr.replace("x", "*").replace("^", "**"))
    except:
        await ctx.response.send_message(f"**{display}** 을(를) 계산하는 과정에서 알 수 없는 오류가 발생했습니다.", ephemeral=True)
    else:
        await ctx.response.send_message(f"**{display}** 은(는) **{result}** 입니다.", ephemeral=True)

client.run('')

import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone
import os
import asyncio
from flask import Flask
from threading import Thread
from datetime import datetime

# 웹서버로 Replit 슬립 방지
app = Flask('')

@app.route('/')
def home():
    return "I'm alive!", 200

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 봇 설정
TOKEN = os.environ["DISCORD_TOKEN"]
CHANNEL_ID = 1377261867700846672  # 본인 채널 ID로 변경하세요
KST = timezone('Asia/Seoul')
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
scheduler = AsyncIOScheduler()

async def send_message(text):
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(text)
    else:
        print("❌ 채널을 찾을 수 없습니다.")

def is_weekday():
    now = datetime.now(tz=KST)
    return now.weekday() < 5  # 0~4면 평일

@bot.event
async def on_ready():
    print(f'✅ 봇 로그인 완료: {bot.user}')
    scheduler.start()

    async def job(text):
        if is_weekday():
            await send_message(text)
        else:
            print("주말이라 메시지를 보내지 않습니다.")

    # ✅ asyncio.create_task 없이 바로 job 전달
    scheduler.add_job(job, 'cron', args=["출근 시간입니다."], hour=10, minute=0, timezone=KST)
    scheduler.add_job(job, 'cron', args=["점심시간입니다."], hour=12, minute=0, timezone=KST)
    scheduler.add_job(job, 'cron', args=["점심시간이 끝났습니다."], hour=13, minute=30, timezone=KST)
    scheduler.add_job(job, 'cron', args=["퇴근 시간입니다."], hour=17, minute=0, timezone=KST)

keep_alive()
bot.run(TOKEN)

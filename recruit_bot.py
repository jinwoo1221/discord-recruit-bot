import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
RECRUIT_CHANNEL_ID = int(os.getenv("RECRUIT_CHANNEL_ID"))

VOICE_CHANNELS = {
    "1364074826926526535": {"name": "일반 SSEN - 1", "max": 4},
    "1171457342345322512": {"name": "일반 SSEN - 2", "max": 4},
    "1354124751148417116": {"name": "일반 SSEN - 3", "max": 4},
    "1354125581024886805": {"name": "일반 SSEN - 4", "max": 4},
    "1355601280554369155": {"name": "일반 SSEN - 5", "max": 4},
    "1348276645492035695": {"name": "일반 SSEN - 6", "max": 4},
    "1354125064949207161": {"name": "일반 SSEN - 7", "max": 4},
    "1365023997720526868": {"name": "일반 SSEN - 8", "max": 4},
    "1364074870849404968": {"name": "일반 SSEN - 9", "max": 4},
    "1358851859959386233": {"name": "일반 SSEN - 10", "max": 4},
    "1354125290758209616": {"name": "경쟁 SSEN - 1", "max": 4},
    "1364074924347494490": {"name": "경쟁 SSEN - 2", "max": 4},
    "1354125335339208715": {"name": "경쟁 SSEN - 3", "max": 4},
    "1382485274591891516": {"name": "경쟁 SSEN - 4", "max": 4},
    "1382485301510803526": {"name": "경쟁 SSEN - 5", "max": 4}
}

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

previous_states = {}

@bot.event
async def on_ready():
    print(f"✅ 봇 로그인됨: {bot.user}")
    check_voice_channels.start()

@tasks.loop(minutes=10)
async def check_voice_channels():
    guild = bot.guilds[0]
    text_channel = guild.get_channel(RECRUIT_CHANNEL_ID)

    for vc_id, info in VOICE_CHANNELS.items():
        vc = guild.get_channel(int(vc_id))
        if vc and isinstance(vc, discord.VoiceChannel):
            human_members = [m for m in vc.members if not m.bot]
            current_count = len(human_members)

            # 0명이면 스킵
            if current_count == 0:
                previous_states[vc_id] = 0
                continue

            # 이전 상태와 같으면 스킵
            if previous_states.get(vc_id) == current_count:
                continue

            previous_states[vc_id] = current_count  # 상태 업데이트

            if current_count < info["max"]:
                needed = info["max"] - current_count
                await text_channel.send(
                    f"📢 `{info['name']}` 채널에 현재 {current_count}명 접속 중입니다. "
                    f"{needed}명 구인 중입니다! 참여하실 분을 기다리고 있어요!"
                )

bot.run(TOKEN)

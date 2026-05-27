import os
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import yt_dlp
import asyncio

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

ytdl_options = {
    "format": "bestaudio/best",
    "noplaylist": True,
    "youtube_include_dash_manifest": False,
    "youtube_include_hls_manifest": False,
    'default_search': 'ytsearch',
    'quiet': True
}

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

song_queues = {}

ytdl = yt_dlp.YoutubeDL(ytdl_options)

class MusicControls(discord.ui.View):
    @discord.ui.button(label="Play/Pause", style=discord.ButtonStyle.green)
    async def play_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        voice_client = interaction.guild.voice_client
        
        if voice_client:
            if voice_client.is_playing():
                voice_client.pause()
                await interaction.response.send_message("⏸️ Music paused.", ephemeral=True)
            elif voice_client.is_paused():
                voice_client.resume()
                await interaction.response.send_message("▶️ Music resumed.", ephemeral=True)
            else:
                await interaction.response.send_message("There is no active audio to toggle.", ephemeral=True)
        else:
            await interaction.response.send_message("The bot isn't connected to voice.", ephemeral=True)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"{bot.user} is online!") 

def check_queue(interaction: discord.Interaction, voice_client: discord.VoiceClient):
    guild_id = interaction.guild.id

    if guild_id in song_queues and len(song_queues[guild_id]) > 0:
        next_song = song_queues[guild_id].pop(0)
        
        player = discord.FFmpegPCMAudio(next_song['url'], **ffmpeg_options)
        
        voice_client.play(player, after=lambda e: check_queue(interaction, voice_client))

        coro = interaction.channel.send(f"▶️ Up next from queue: **{next_song['title']}**", view=MusicControls())
        asyncio.run_coroutine_threadsafe(coro, bot.loop)

@bot.tree.command(name="play", description="Play a song from YouTube.")
async def play(interaction: discord.Interaction, search: str):
    await interaction.response.defer()

    if not interaction.user.voice:
        await interaction.followup.send("You need to join a voice channel first!")
        return

    channel = interaction.user.voice.channel
    voice_client = interaction.guild.voice_client

    if not voice_client:
        voice_client = await channel.connect()

    loop = asyncio.get_event_loop()
    data = await loop.run_in_executor(None, lambda: ytdl.extract_info(search, download=False))

    if 'entries' in data:
        data = data['entries'][0]

    song_url = data['url']
    song_title = data['title']

    song_url = data['url']
    song_title = data['title']
    guild_id = interaction.guild.id

    if guild_id not in song_queues:
        song_queues[guild_id] = []

    if not voice_client.is_playing() and not voice_client.is_paused():
        player = discord.FFmpegPCMAudio(song_url, **ffmpeg_options)
        
        voice_client.play(player, after=lambda e: check_queue(interaction, voice_client))
        
        await interaction.followup.send(f"▶️ Now playing: **{song_title}**", view=MusicControls())
    else:
        song_queues[guild_id].append({'url': song_url, 'title': song_title})
        await interaction.followup.send(f"✅ Added to queue: **{song_title}** (Position: {len(song_queues[guild_id])})")

@bot.tree.command(name="skip", description="Skip the currently playing song.")
async def skip(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client

    if not voice_client or not voice_client.is_playing():
        await interaction.response.send_message("There is no music playing right now.", ephemeral=True)
        return

    voice_client.stop()
    await interaction.response.send_message("⏭️ Song skipped!")


@bot.tree.command(name="queue", description="Shows the current music queue.")
async def queue(interaction: discord.Interaction):
    guild_id = interaction.guild.id

    if guild_id not in song_queues or len(song_queues[guild_id]) == 0:
        await interaction.response.send_message("The queue is currently empty.", ephemeral=True)
        return

    queue_list = ""
    for index, song in enumerate(song_queues[guild_id]):
        # Add 1 to the index so the list starts at 1 instead of 0
        queue_list += f"{index + 1}. {song['title']}\n"

    embed = discord.Embed(title="Current Queue", description=queue_list, color=discord.Color.blue())
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="exit", description="Stop the music, clear the queue, and leave the channel.")
async def exit(interaction: discord.Interaction):
    guild_id = interaction.guild.id
    voice_client = interaction.guild.voice_client

    if guild_id in song_queues:
        song_queues[guild_id] = []
    
    if not voice_client:
        await interaction.response.send_message("I'm not in a voice channel.", ephemeral=True)
        return
    
    if voice_client.is_playing() or voice_client.is_paused():
        voice_client.stop()

    await voice_client.disconnect()

    await interaction.response.send_message("Cleared the queue and left the voice channel")


@bot.event
async def on_voice_state_update(member, before, after):
    if member == bot.user and after.channel is None:
        guild_id = member.guild.id
        song_queues.pop(guild_id, None)
        print(f"Cleaned up queue for Guild {guild_id} after manual disconnect.")

        
bot.run(TOKEN)

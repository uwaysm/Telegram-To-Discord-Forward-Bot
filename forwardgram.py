import asyncio
import logging
import sys
import threading
from flask import Flask, request

import discord
import yaml
from discord.ext import commands
from telethon import TelegramClient, events
from telethon.tl.types import InputChannel
import os
app = Flask(__name__)

@app.route('/set_code', methods=['POST'])
def set_code():
    global verification_code
    verification_code = request.form.get('code')
    return 'OK', 200

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True  # Add this line to enable message intents
bot = commands.Bot(command_prefix="!", intents=intents)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logging.getLogger("telethon").setLevel(level=logging.WARNING)
logger = logging.getLogger(__name__)

async def send_message(message):
    channel_id =   # Replace with the desired channel ID
    channel = bot.get_channel(channel_id)
    role_mention = ""  # Replace with the desired role ID
    await channel.send(role_mention + message)

@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")
def run_discord_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        start_coro = bot.start("")
        #DISCORD BOT TOKEN
        future = asyncio.run_coroutine_threadsafe(start_coro, loop)
        future.result()
    except Exception as e:
        logger.error(f"An exception occurred while running the Discord bot: {e}")


def run_flask_app():
    app.run(port=int(os.environ.get("PORT", 5000)))
async def main(config_path):
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    client = TelegramClient(
        config["session_name"],
        config["api_id"],
        config["api_hash"],
    )
    await client.start()

    input_channels_entities = []
    output_channel_entities = []

    async for d in client.iter_dialogs():
        if d.name in config["input_channel_names"] or d.entity.id in config["input_channel_ids"]:
            input_channels_entities.append(InputChannel(d.entity.id, d.entity.access_hash))
        if d.name in config["output_channel_names"] or d.entity.id in config["output_channel_ids"]:
            output_channel_entities.append(InputChannel(d.entity.id, d.entity.access_hash))

    if not output_channel_entities:
        logger.error("Could not find any output channels in the user's dialogs")
        sys.exit(1)

    if not input_channels_entities:
        logger.error("Could not find any input channels in the user's dialogs")
        sys.exit(1)

    logging.info(f"Listening on {len(input_channels_entities)} channels. Forwarding messages to {len(output_channel_entities)} channels.")

    @client.on(events.NewMessage(chats=input_channels_entities))
    async def handler(event):
        for output_channel in output_channel_entities:
            try:
                parsed_response = event.message.message + "\n" + event.message.entities[0].url
            except (TypeError, IndexError, AttributeError):
                parsed_response = event.message.message

            await client.forward_messages(output_channel, event.message)
            await send_message(parsed_response)

    try:
        await client.run_until_disconnected()
    except Exception as e:
        logger.error(f"An exception occurred while running the Telegram client: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} {{CONFIG_PATH}}")
        sys.exit(1)

    discord_thread = threading.Thread(target=run_discord_bot)
    discord_thread.start()

    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.start()

    asyncio.run(main(sys.argv[1]))

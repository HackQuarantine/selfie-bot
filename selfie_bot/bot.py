import discord
from discord.ext import commands
from PIL import Image
import requests
from io import BytesIO
from . import config, logging, storage, image_utils
logging.init()
from selfie_bot.logging import logger

bot = commands.Bot(command_prefix=config.creds['prefix'])

def main():
    bot.run(config.creds['token'])

@bot.event
async def on_ready():
    global log_channel
    log_channel = bot.get_channel(config.creds['log_channel_id'])
    logger.info('Bot Online!')
    await get_photos()
    await bot.logout()

async def get_photos():
    global log_channel

    urls = await get_all_urls()
    logger.info(f"Collected {len(urls)} photo urls in total")

    for url in urls:
        await save_photo(url)

    logger.info(f"Saved all {len(urls)} photos!")

async def get_all_urls():
    urls = []
    selfie_channel = bot.get_channel(config.creds['selfie_channel_id'])
    messages = await selfie_channel.history(limit=200).flatten()

    for message in messages:
        if len(message.attachments) > 0:
            urls.append((message.attachments[0].url, message.id))
    return urls

async def save_photo(known_images):
    global log_channel

    url, message_id = known_images

    if storage.file_exists(message_id):
        logger.debug(f'Skipping {url}, already saved')
        return

    logger.debug(f'Download & process {url}')

    try:
        response = requests.get(url, timeout=5)
        try:
            response.raise_for_status()
            image_utils.save_image(
                message_id,
                BytesIO(response.content)
            )
        except requests.HTTPError:
            logger.error('HTTP error')

    except requests.exceptions.ConnectionError:
        logger.error('Network error')



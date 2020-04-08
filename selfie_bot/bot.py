import discord
from discord.ext import commands
from PIL import ImageOps
from . import config
from . import logging
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

@bot.check
async def is_admin(ctx):
    authorised = ctx.author.id in config.creds['admin_ids']
    if not authorised:
        logger.warn(f'Unauthorised user \'{ctx.author.display_name}\' ({ctx.author.id}) tried to use command')
    return authorised

@bot.command(description="Get all the photos from the selfies channel.")
async def get_photos(ctx):
    global log_channel

def get_all_urls():
    pass

def save_photo(url):
    logger.debug(f'Download & process {url}')

    image_loaded = False
    try:
        response = requests.get(url, timeout=5)
        try:
            response.raise_for_status()
            try:
                image = Image.open(BytesIO(response.content))
                image = rotate_if_exif_specifies(image)
                image_loaded = True
            except OSError:
                logger.error('Image decoding error')

        except requests.HTTPError:
            logger.error('HTTP error')

    except requests.exceptions.ConnectionError:
        logger.error('Network error')
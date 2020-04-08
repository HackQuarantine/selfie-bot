import discord
from discord.ext import commands
from PIL import Image
import requests
from io import BytesIO
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

    urls = await get_all_urls()
    logger.info(f"Collected {len(urls)} photo urls in total")
    await log_channel.send(f"Collected {len(urls)} photo urls in total")

    for url in urls:
        await save_photo(url)
    logger.info(f"Saved all {len(urls)} photos!")
    await log_channel.send(f"Saved all {len(urls)} photos!")

async def get_all_urls():
    urls = []
    selfie_channel = bot.get_channel(config.creds['selfie_channel_id'])
    messages = await selfie_channel.history(limit=200).flatten()

    for message in messages:
        if len(message.attachments) > 0:
            urls.append((message.attachments[0].url, message.id))
            
    return urls

async def save_photo(url):
    global log_channel
    logger.debug(f'Download & process {url[0]}')

    try:
        response = requests.get(url[0], timeout=5)
        try:
            response.raise_for_status()
            try:
                image = Image.open(BytesIO(response.content))
                image = rotate_if_exif_specifies(image)
                image.save(f"{url[1]}.jpg", optimize=True)
                logger.info(f"Saved photo as {url[1]}.jpg")
                await log_channel.send(f"Saved photo as `{url[1]}.jpg`")
            except OSError:
                logger.error('Image decoding error')

        except requests.HTTPError:
            logger.error('HTTP error')

    except requests.exceptions.ConnectionError:
        logger.error('Network error')

def rotate_if_exif_specifies(image):
    try:
        exif_tags = image._getexif()
        if exif_tags is None:
            # No EXIF tags, so we don't need to rotate
            logger.debug('No EXIF data, so not transforming')
            return image

        value = exif_tags[274]
    except KeyError:
        # No rotation tag present, so we don't need to rotate
        logger.debug('EXIF data present but no rotation tag, so not transforming')
        return image

    value_to_transform = {
        1: (0, False),
        2: (0, True),
        3: (180, False),
        4: (180, True),
        5: (-90, True),
        6: (-90, False),
        7: (90, True),
        8: (90, False)
    }

    try:
        angle, flip = value_to_transform[value]
    except KeyError:
        logger.warn(f'EXIF rotation \'{value}\' unknown, not transforming')
        return image

    logger.debug(f'EXIF rotation \'{value}\' detected, rotating {angle} degrees, flip: {flip}')
    if angle != 0:
        image = image.rotate(angle)

    if flip:
        image = image.tranpose(Image.FLIP_LEFT_RIGHT)

    return image
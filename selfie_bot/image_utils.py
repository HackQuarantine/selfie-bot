from PIL import Image
from . import config, logging, storage
logging.init()
from selfie_bot.logging import logger

def save_image(uid, image_data):
    storage.make_path(config.creds['storage_dir'])
    fname = storage.filename(uid)
    image = Image.open(image_data)
    image = rotate_if_exif_specifies(image)
    image.convert('RGB').save(fname, optimize=True)

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
    except AttributeError:
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

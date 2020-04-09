from PIL import Image
from os import mkdir, path

from . import config

def filename(message_id):
    storage_dir = config.creds['storage_dir']
    return f"{storage_dir}/{message_id}.jpg"

def file_exists(uid):
    fname = filename(uid)
    return path.isfile(fname)

def make_path(path):
    try:
        mkdir(path)
    except FileExistsError:
        pass

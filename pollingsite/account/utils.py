import os
from time import time
from PIL import Image
from flask import current_app


def save_picture(form_picture):
    """Update image avatar"""
    picture_fn = str(round(time()*1000)) + form_picture.filename
    picture_path = os.path.join(
        current_app.root_path, 'static/images', picture_fn
    )
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

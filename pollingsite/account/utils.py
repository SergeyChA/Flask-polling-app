import os
from time import time
from PIL import Image
from flask import current_app


def save_picture(form_picture):
    """Update image avatar"""
    picture_format = form_picture.filename.split('.')[-1]
    picture_name = str(round(time()*1000)) + '.' + picture_format
    picture_path = os.path.join(
        current_app.root_path, 'static/images', picture_name
    )
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_name

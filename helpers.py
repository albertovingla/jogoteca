import os
from jogoteca import app


def recover_image(id):
    for file_name in os.listdir(app.config["UPLOAD_PATH"]):
        if f"image{id}" in file_name:
            return file_name

    return "default_image.jpg"


def delete_file_modified(id):
    file = recover_image(id)
    if file != "default_image.jpg":
        os.remove(os.path.join(app.config["UPLOAD_PATH"], file))

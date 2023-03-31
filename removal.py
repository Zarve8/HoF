from rembg import remove
from PIL import Image


def remove_bg(filepath, new_filepath):
    input = Image.open(filepath)
    output = remove(input)
    output.save(new_filepath)

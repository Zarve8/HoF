from rembg import remove
from PIL import Image
import easygui as eg
import telebot
from img import load_user_preview
from processor import process_image
from instagram import start as start_insta, publish_image
import os
import os
from copy import deepcopy
from PIL import Image
import numpy as np



print("Starting")
print("Input Path")
print("Out path")
input = Image.open('files/work_raw_772339745.jpg')
print("Opened")
output = remove(input)
print("Removed")
output.save('files/work_on_wall_772339745.png')